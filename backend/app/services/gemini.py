import os
from typing import Literal, Dict, Any
from app.models.schemas import AIReport
from PIL import Image, ExifTags

try:
	import google.generativeai as genai  # type: ignore
except Exception:
	genai = None  # type: ignore


def _mock_ai_response() -> AIReport:
	# Deprecated: mocks disabled per user request
	raise RuntimeError("Mock AI disabled. Configure GEMINI_API_KEY and set USE_MOCK_AI=false")


def analyze_media_with_gemini(path: str, media_kind: Literal["image", "video"]) -> AIReport:
	use_mock = os.getenv("USE_MOCK_AI", "false").lower() in ("1", "true", "yes")
	api_key = os.getenv("GEMINI_API_KEY")
	if use_mock:
		return _mock_ai_response()
	if not api_key:
		raise RuntimeError("GEMINI_API_KEY is not set but USE_MOCK_AI=false")
	if genai is None:
		raise RuntimeError("google-generativeai is not installed")

	# Basic EXIF extraction to provide grounded metadata
	metadata: Dict[str, Any] = {}
	if media_kind == "image":
		try:
			with Image.open(path) as img:
				metadata["resolution"] = f"{img.width}x{img.height}"
				exif = img.getexif()
				if exif:
					exif_dict = {}
					for k, v in exif.items():
						name = ExifTags.TAGS.get(k, str(k))
						exif_dict[name] = v
					metadata.update({
						"camera": exif_dict.get("Model") or exif_dict.get("Make"),
						"datetime": exif_dict.get("DateTimeOriginal") or exif_dict.get("DateTime"),
					})
		except Exception:
			pass

	# Prepare Gemini request
	genai.configure(api_key=api_key)
	# Prefer valid defaults; allow override via GEMINI_MODEL
	default_image_model = "gemini-2.5-flash"
	default_video_model = "gemini-2.5-pro"
	configured = os.getenv("GEMINI_MODEL")
	model_name = configured or (default_video_model if media_kind == "video" else default_image_model)
	model = genai.GenerativeModel(model_name)
	with open(path, "rb") as f:
		data = f.read()
	mime = "image/jpeg" if media_kind == "image" else "video/mp4"
	prompt = (
		"You are an expert media forensics assistant. Analyze the provided media and return strictly JSON with keys: "
		"plagiarism_score (integer 0-100), metadata (object), edit_detection (object). "
		"metadata should include camera/model if known, file_type, resolution, and timestamps if present. "
		"edit_detection should include booleans like recompression, possible_screenshot, and a list manipulation_signals. "
		"Be concise, do not include any text outside JSON."
	)

	res = model.generate_content([prompt, {"mime_type": mime, "data": data}])
	text = (res.text or "{}").strip()
	import json
	start = text.find("{")
	end = text.rfind("}")
	if start == -1 or end == -1:
		raise RuntimeError("Gemini did not return JSON")
	parsed = json.loads(text[start:end+1])
	if not isinstance(parsed, dict):
		raise RuntimeError("Gemini JSON not an object")
	plag_score = int(parsed.get("plagiarism_score", 50))
	model_metadata = parsed.get("metadata", {})
	flags = parsed.get("edit_detection", {})
	# Merge extracted EXIF basics with model metadata when missing
	if isinstance(model_metadata, dict):
		for k, v in metadata.items():
			model_metadata.setdefault(k, v)
	else:
		model_metadata = metadata
	return AIReport(
		plagiarism_score=max(0, min(100, plag_score)),
		metadata=model_metadata,
		edit_detection=flags if isinstance(flags, dict) else {},
	)


def extract_tags_with_gemini(path: str, media_kind: Literal["image", "video"]) -> list[str]:
	"""Ask Gemini to output 3-6 concise visual tags as a JSON array of strings."""
	use_mock = os.getenv("USE_MOCK_AI", "false").lower() in ("1", "true", "yes")
	api_key = os.getenv("GEMINI_API_KEY")
	if use_mock:
		raise RuntimeError("Mock AI disabled; set USE_MOCK_AI=true to enable mocks")
	if not api_key or genai is None:
		raise RuntimeError("GEMINI_API_KEY missing or SDK not installed")
	try:
		genai.configure(api_key=api_key)
		default_image_model = "gemini-2.5-flash"
		default_video_model = "gemini-2.5-pro"
		configured = os.getenv("GEMINI_MODEL")
		model_name = configured or (default_video_model if media_kind == "video" else default_image_model)
		model = genai.GenerativeModel(model_name)
		with open(path, "rb") as f:
			data = f.read()
		mime = "image/jpeg" if media_kind == "image" else "video/mp4"
		prompt = (
			"Return strictly a JSON array of 3-6 short tags describing the dominant objects, scene, and style. "
			"No extra text."
		)
		res = model.generate_content([prompt, {"mime_type": mime, "data": data}])
		text = (res.text or "[]").strip()
		import json
		start = text.find("[")
		end = text.rfind("]")
		if start == -1 or end == -1:
			raise RuntimeError("Gemini did not return tags array")
		arr = json.loads(text[start:end+1])
		if not isinstance(arr, list):
			raise RuntimeError("Gemini tags not an array")
		return [str(x)[:32] for x in arr if isinstance(x, (str, int, float))][:6]
	except Exception as e:
		raise



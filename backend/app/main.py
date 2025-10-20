from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import uuid
from pathlib import Path
from dotenv import load_dotenv

from .services.gemini import analyze_media_with_gemini, extract_tags_with_gemini
from .services.reverse_search import reverse_image_search
from .models.schemas import AnalysisReport
from .utils.file_ops import save_temp_upload, delete_file_safely, sniff_media_kind, upload_to_r2


load_dotenv()

app = FastAPI(title="Visual Plagiarism Detector API", version="0.1.0")

origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


class AnalyzeResponse(BaseModel):
	report: AnalysisReport
	request_id: str


@app.get("/health")
def health_check():
	return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(media: UploadFile = File(...)):
	if media is None:
		raise HTTPException(status_code=400, detail="No file provided")

	request_id = str(uuid.uuid4())
	uploads_dir = Path(os.getenv("UPLOADS_DIR", "backend/uploads")).resolve()
	uploads_dir.mkdir(parents=True, exist_ok=True)

	# Save temp file
	temp_path = await save_temp_upload(media, uploads_dir, request_id)

	try:
		media_kind = sniff_media_kind(temp_path)
    	# AI analysis
		ai_report = analyze_media_with_gemini(temp_path, media_kind)
		# Try to get public URL (now optional); else derive keywords for search
		public_url = None  # R2 removed for prototype; keep None
		tags = extract_tags_with_gemini(temp_path, media_kind)
		# Reverse search uses public_url when available or falls back to keyword search
		reverse_results = reverse_image_search(temp_path, public_url, tags)

		report = AnalysisReport(
			ai_report=ai_report,
			reverse_search=reverse_results,
		)
		return JSONResponse(content={"report": report.model_dump(), "request_id": request_id})
	finally:
		delete_file_safely(temp_path)



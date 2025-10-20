from fastapi import UploadFile
from pathlib import Path
import os
import boto3
from botocore.config import Config


async def save_temp_upload(media: UploadFile, uploads_dir: Path, request_id: str) -> str:
	filename = f"{request_id}_{media.filename}"
	path = uploads_dir / filename
	with path.open("wb") as buffer:
		content = await media.read()
		buffer.write(content)
	return str(path)


def delete_file_safely(path_str: str) -> None:
	try:
		path = Path(path_str)
		if path.exists():
			path.unlink()
	except Exception:
		# Best-effort cleanup
		pass


def sniff_media_kind(path_str: str) -> str:
	lower = path_str.lower()
	if any(lower.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp", ".gif"]):
		return "image"
	if any(lower.endswith(ext) for ext in [".mp4", ".mov", ".avi", ".mkv", ".webm"]):
		return "video"
	return "unknown"


def upload_to_r2(path_str: str) -> str | None:
	"""Uploads the file to Cloudflare R2 if env vars exist and returns a public URL.
	Env required:
	- R2_ACCOUNT_ID
	- R2_ACCESS_KEY_ID
	- R2_SECRET_ACCESS_KEY
	- R2_BUCKET
	- R2_PUBLIC_BASE_URL (e.g., https://<custom-domain> or https://<accountid>.r2.cloudflarestorage.com/<bucket>)
	"""
	account_id = os.getenv("R2_ACCOUNT_ID")
	access_key = os.getenv("R2_ACCESS_KEY_ID")
	secret_key = os.getenv("R2_SECRET_ACCESS_KEY")
	bucket = os.getenv("R2_BUCKET")
	public_base = os.getenv("R2_PUBLIC_BASE_URL")
	if not all([account_id, access_key, secret_key, bucket, public_base]):
		return None

	endpoint_url = f"https://{account_id}.r2.cloudflarestorage.com"
	s3 = boto3.client(
		"s3",
		aws_access_key_id=access_key,
		aws_secret_access_key=secret_key,
		endpoint_url=endpoint_url,
		config=Config(signature_version="s3v4"),
	)

	path = Path(path_str)
	key = path.name
	s3.upload_file(str(path), bucket, key, ExtraArgs={"ACL": "public-read"})
	# Construct public URL
	if public_base.endswith("/"):
		return f"{public_base}{key}"
	return f"{public_base}/{key}"



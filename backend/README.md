# Visual Plagiarism Detector API (FastAPI)

## Quickstart

1. Create and activate a virtual environment
```bash
python -m venv .venv && .venv\\Scripts\\activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure environment (optional)
Create a `.env` file at `backend/.env`:
```bash
CORS_ORIGINS=*
UPLOADS_DIR=backend/uploads
USE_MOCK_AI=true
USE_MOCK_SEARCH=true
```

4. Run the API
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints
- `GET /health` health check
- `POST /analyze` multipart form-data with `media` file

Example cURL:
```bash
curl -X POST http://localhost:8000/analyze \
  -F "media=@/path/to/file.jpg"
```

## Notes
- Files are saved temporarily to `UPLOADS_DIR` and deleted after processing.
- By default, AI and reverse search are mocked. Set `USE_MOCK_AI=false` and `USE_MOCK_SEARCH=false` when you wire real APIs.

## Environment variables
Create `backend/.env` and set as needed:
```bash
# CORS and uploads
CORS_ORIGINS=*
UPLOADS_DIR=backend/uploads

# Toggle mocks
USE_MOCK_AI=false
USE_MOCK_SEARCH=false

# Google Gemini
GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=gemini-1.5-flash

# SerpAPI (Google Lens/Images)
SERPAPI_API_KEY=your_serpapi_key

# Cloudflare R2 (optional, for public URL uploads)
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET=your_bucket
# e.g. https://cdn.example.com or https://<accountid>.r2.cloudflarestorage.com/<bucket>
R2_PUBLIC_BASE_URL=https://your-public-base
```


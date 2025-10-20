# Video & Image Plagiarism Detector

## 1. Introduction

The **Video & Image Plagiarism Detector** is an AI-powered tool designed to identify whether an uploaded image or video is original, edited, or plagiarized from online sources.  
It leverages AI embeddings, metadata inspection, and reverse search to detect similarities and generate a plagiarism score.  

The goal is to assist creators, designers, and content platforms in verifying originality, detecting edits or screenshots, and tracing visual content ownership.

---

## 2. Tech Stack

- **Frontend:** React  
- **Styling:** Tailwind CSS  
- **Backend:** FastAPI (Python)  
- **AI Model:** Gemini API  
- **Search Engine:** SerpAPI (Google Image Search)  
- **Storage:** Local folder for temporary uploads (`/uploads`)

---

## 3. How It Works

### 1. User Uploads File

User selects an image or video from their computer.  
The React frontend sends it via a POST request to the FastAPI backend endpoint (e.g., `/analyze`).

<img width="2559" height="881" alt="Image" src="https://github.com/user-attachments/assets/a4f0aa32-e6a0-4b18-bfe2-1009255918f3" />

---

### 2. Temporary Storage

The backend temporarily stores the uploaded file in a local folder (`/uploads`) for processing.  
Once the analysis is complete, the file is deleted to prevent unnecessary storage usage.

---

### 3. AI Analysis (Gemini API)

The backend sends the uploaded file to the Gemini API, which performs:

- **Embedding generation:** Creates a unique vector representing the content.  
- **Metadata analysis:** Extracts EXIF data, timestamps, resolution, and compression artifacts.  
- **Edit detection:** Identifies signs of editing, screenshots, or manipulation.

<img width="1754" height="943" alt="Image" src="https://github.com/user-attachments/assets/142cf028-dd64-4dfd-9d3c-e50fd78823da" />

### 4. Reverse Image/Video Search (SerpAPI)

The backend sends the uploaded file to **SerpAPI** (Google Image Search).  
SerpAPI returns visually similar images or videos from the web.

Each match includes:
- URL of the similar file
- Similarity/confidence score

<img width="1425" height="1316" alt="Image" src="https://github.com/user-attachments/assets/e4e00b08-e2de-4d0b-846b-70fbc3ad4840" />

### 5. Report Generation

The backend combines results from both **Gemini API** and **SerpAPI** to generate a structured JSON report:

{
  "ai_report": {
    "plagiarism_score": 82,
    "metadata": {...},
    "edit_detection": {...}
  },
  "reverse_search": [
    {"url": "https://example.com/image.jpg", "similarity": 92},
    {"url": "https://example.com/video.mp4", "similarity": 85}
  ]
}

### 6. Frontend Display

The React frontend receives the JSON report from the backend and displays:

- Preview of the uploaded file  
- Plagiarism score (0–100%)  
- Metadata and edit detection results  
- List of similar files found online  

Optional (Future Feature): **“Prove Ownership”** button to authenticate original creators.

---

### 7. Conclusion

This project demonstrates how AI and reverse search can be combined to detect plagiarism in images and videos.  
While functional, the **current accuracy is low** and depends on model performance and search results.

---

### Future Implementations

1. **Database Integration (AWS / MongoDB)**  
   Store reports and user upload history securely for long-term tracking.

2. **Ownership Verification**  
   Add a feature to prove content ownership using digital signatures or watermark validation.

3. **Accuracy Enhancement**  
   Improve Gemini fine-tuning and SerpAPI result filtering to increase detection precision.



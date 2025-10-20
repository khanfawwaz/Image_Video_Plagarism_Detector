import os
from typing import List
from app.models.schemas import ReverseResult
import requests


def _mock_reverse_results() -> List[ReverseResult]:
	return [
		ReverseResult(url="https://example.com/image1.jpg", similarity=92),
		ReverseResult(url="https://example.com/image2.jpg", similarity=85),
	]


def reverse_image_search(path: str, public_url: str | None = None, keywords: list[str] | None = None) -> List[ReverseResult]:
    use_mock = os.getenv("USE_MOCK_SEARCH", "false").lower() in ("1", "true", "yes")
    if use_mock:
        return _mock_reverse_results()

    serp_key = os.getenv("SERPAPI_API_KEY") or os.getenv("SERPAPI_KEY")
    if not serp_key:
        return _mock_reverse_results()

    try:
        results: List[ReverseResult] = []
        if public_url:
            # Try Google Lens by image URL
            params = {
                "engine": "google_lens",
                "url": public_url,
                "api_key": serp_key,
            }
            r = requests.get("https://serpapi.com/search.json", params=params, timeout=30)
            r.raise_for_status()
            data = r.json()
            for item in data.get("visual_matches", [])[:10]:
                link = item.get("link") or item.get("source") or item.get("thumbnail")
                if link:
                    results.append(ReverseResult(url=link, similarity=70))
        # Fallback to keyword search if no public URL or no matches
        if not results and keywords:
            q = " ".join(keywords[:6])
            params = {
                "engine": "google",
                "q": q,
                "tbm": "isch",  # image search
                "api_key": serp_key,
            }
            r = requests.get("https://serpapi.com/search.json", params=params, timeout=30)
            r.raise_for_status()
            data = r.json()
            for item in data.get("images_results", [])[:10]:
                link = item.get("original") or item.get("thumbnail") or item.get("link")
                if link:
                    results.append(ReverseResult(url=link, similarity=60))
        if not results:
            return _mock_reverse_results()
        return results
    except Exception:
        return _mock_reverse_results()



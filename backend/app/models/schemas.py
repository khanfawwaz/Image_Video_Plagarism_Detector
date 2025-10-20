from typing import Dict, Any, List
from pydantic import BaseModel


class AIReport(BaseModel):
	plagiarism_score: int
	metadata: Dict[str, Any]
	edit_detection: Dict[str, Any]


class ReverseResult(BaseModel):
	url: str
	similarity: int


class AnalysisReport(BaseModel):
	ai_report: AIReport
	reverse_search: List[ReverseResult]



from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class ATSResponse(BaseModel):
    score: Dict[str, Any]
    missing_skills: List[str]
    optimized_resume: str

    # ---- metadata ----
    processing_time_ms: Optional[int] = None
    model_version: Optional[str] = "v1"

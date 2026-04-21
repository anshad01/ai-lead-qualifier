from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class Lead(BaseModel):
    name: str
    email: str
    company: str
    job_title: str
    message: str


class LeadResult(BaseModel):
    name: str
    email: str
    company: str
    job_title: str
    message: str
    lead_score: int
    tier: str
    industry: str
    business_need: str
    recommended_action: str
    reasoning: str
    processed_at: str = datetime.now().isoformat()
    error: bool = False
    error_message: Optional[str] = None
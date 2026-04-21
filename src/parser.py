import json
import re
from src.models import LeadResult, Lead
from src.logger import log_error
from datetime import datetime


def parse_response(raw: str, lead: Lead) -> LeadResult:
    try:
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON found in response")

        data = json.loads(json_match.group())

        return LeadResult(
            name=lead.name,
            email=lead.email,
            company=lead.company,
            job_title=lead.job_title,
            message=lead.message,
            lead_score=int(data["lead_score"]),
            tier="",
            industry=str(data["industry"]),
            business_need=str(data["business_need"]),
            recommended_action=str(data["recommended_action"]),
            reasoning=str(data["reasoning"]),
            processed_at=datetime.now().isoformat(),
            error=False,
        )

    except Exception as e:
        log_error(f"Failed to parse response for {lead.email}: {e}")
        return LeadResult(
            name=lead.name,
            email=lead.email,
            company=lead.company,
            job_title=lead.job_title,
            message=lead.message,
            lead_score=-1,
            tier="Unknown",
            industry="Unknown",
            business_need="Parse error",
            recommended_action="Manual review",
            reasoning="Failed to parse AI response",
            processed_at=datetime.now().isoformat(),
            error=True,
            error_message=str(e),
        )
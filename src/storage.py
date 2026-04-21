import csv
import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path
from src.models import LeadResult
from src.config import settings
from src.logger import log_info, log_error

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

HEADERS = [
    "Name", "Email", "Company", "Job Title", "Message",
    "Lead Score", "Tier", "Industry", "Business Need",
    "Recommended Action", "Reasoning", "Processed At", "Error"
]


def _get_sheet():
    creds = Credentials.from_service_account_file(
        settings.GOOGLE_CREDENTIALS_PATH,
        scopes=SCOPES
    )
    client = gspread.authorize(creds)
    sheet = client.open(settings.GOOGLE_SHEET_NAME).sheet1
    return sheet


def save_to_sheets(results: list[LeadResult]) -> None:
    try:
        sheet = _get_sheet()
        sheet.clear()
        sheet.append_row(HEADERS)

        for r in results:
            sheet.append_row([
                r.name, r.email, r.company, r.job_title, r.message,
                r.lead_score, r.tier, r.industry, r.business_need,
                r.recommended_action, r.reasoning, r.processed_at, r.error
            ])

        log_info(f"Saved {len(results)} results to Google Sheets")

    except Exception as e:
        log_error(f"Google Sheets save failed: {e}")
        raise


def save_to_csv(results: list[LeadResult], filepath: str = "output/results.csv") -> None:
    try:
        Path("output").mkdir(exist_ok=True)
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()
            for r in results:
                writer.writerow({
                    "Name": r.name, "Email": r.email, "Company": r.company,
                    "Job Title": r.job_title, "Message": r.message,
                    "Lead Score": r.lead_score, "Tier": r.tier,
                    "Industry": r.industry, "Business Need": r.business_need,
                    "Recommended Action": r.recommended_action,
                    "Reasoning": r.reasoning, "Processed At": r.processed_at,
                    "Error": r.error
                })

        log_info(f"Saved results to {filepath}")

    except Exception as e:
        log_error(f"CSV save failed: {e}")
        raise
import pandas as pd
from pathlib import Path
from src.models import Lead
from src.logger import log_info, log_error


REQUIRED_COLUMNS = {"name", "email", "company", "job_title", "message"}


def load_leads(filepath: str) -> list[Lead]:
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {filepath}")

    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower()

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.dropna(subset=["email"])
    df = df.drop_duplicates(subset=["email"], keep="first")
    df = df.fillna("")

    leads = []
    for _, row in df.iterrows():
        try:
            lead = Lead(
                name=str(row["name"]).strip(),
                email=str(row["email"]).strip(),
                company=str(row["company"]).strip(),
                job_title=str(row["job_title"]).strip(),
                message=str(row["message"]).strip(),
            )
            leads.append(lead)
        except Exception as e:
            log_error(f"Skipping invalid row: {e}")

    log_info(f"Loaded {len(leads)} valid leads")
    return leads
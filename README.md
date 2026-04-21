# AI Lead Qualifier

An AI-powered lead qualification system that automatically analyzes and scores sales leads using Groq LLM and saves results to Google Sheets.

## What it does

- Reads leads from a CSV file (name, email, company, job title, message)
- Sends each lead to Groq AI (Llama 3.3 70B) for analysis
- Returns a lead score (0-100), industry, business need, and recommended action
- Classifies leads as Hot / Warm / Cold
- Saves results to Google Sheets and a local CSV file

## Tech Stack

- Python 3.11+
- Groq API (free) — Llama 3.3 70B
- Google Sheets API — gspread
- Pydantic — data validation
- Tenacity — retry logic
- Rich — terminal UI

## Setup

1. Clone the repo:
```bash
git clone https://github.com/anshad01/ai-lead-qualifier.git
cd ai-lead-qualifier
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Create `.env` file:
```env
GROQ_API_KEY=your_groq_key_here
GOOGLE_SHEET_NAME=AI Lead Qualifier
GOOGLE_CREDENTIALS_PATH=credentials.json
MODEL_NAME=llama-3.3-70b-versatile
```

4. Add your `credentials.json` from Google Cloud Console

5. Run:
```bash
python main.py
```

## Output

Results are saved to:
- Google Sheets (live)
- `output/results.csv` (local)

## Project Structure

```
src/
├── config.py       # settings
├── models.py       # Pydantic models
├── loader.py       # CSV ingestion
├── prompt.py       # AI prompt template
├── llm_client.py   # Groq API + retry
├── parser.py       # JSON parser
├── scorer.py       # tier logic
├── storage.py      # Google Sheets + CSV
└── logger.py       # Rich logging
```
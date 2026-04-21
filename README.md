# AI Lead Qualifier

An AI-powered lead qualification system that automatically analyzes, scores, and visualizes sales leads using Groq LLM with a Streamlit web interface.

## Demo Screenshots

<img width="1919" height="893" alt="Screenshot 2026-04-21 152242" src="https://github.com/user-attachments/assets/bc663ec2-65a7-499d-8582-b8e524cb964c" />

<img width="1874" height="908" alt="Screenshot 2026-04-21 152324" src="https://github.com/user-attachments/assets/453140b2-5234-4741-a2c0-8baee80d537b" />

<img width="1883" height="907" alt="Screenshot 2026-04-21 152337" src="https://github.com/user-attachments/assets/55e6adca-ea8e-461a-ae16-fc21289fa61b" />

<img width="1870" height="907" alt="Screenshot 2026-04-21 152354" src="https://github.com/user-attachments/assets/b26ec4af-be67-41c4-bef6-02f719f66443" />


## What it does

- Upload any CSV file of leads via web interface
- AI analyzes each lead using Llama 3.3 70B (Groq)
- Returns lead score (0–100), industry, business need, recommended action
- Classifies leads as Hot / Warm / Cold automatically
- Beautiful visual results with expandable cards
- Download results as CSV
- Saves to Google Sheets automatically

## Tech Stack

- Python 3.11+
- Streamlit — web UI
- Groq API (free) — Llama 3.3 70B
- Google Sheets API — gspread
- Pydantic — data validation
- Tenacity — retry logic with exponential backoff
- Rich — terminal logging

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/anshad01/ai-lead-qualifier.git
cd ai-lead-qualifier
```

### 2. Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install streamlit
```

### 4. Get your free Groq API key

- Go to https://console.groq.com
- Sign up free
- Create an API key

### 5. Set up Google Sheets

- Go to https://console.cloud.google.com
- Create a project
- Enable Google Sheets API and Google Drive API
- Create a Service Account and download credentials.json
- Create a blank Google Sheet named `AI Lead Qualifier`
- Share the sheet with the service account email as Editor

### 6. Create .env file

```env
GROQ_API_KEY=your_groq_key_here
GOOGLE_SHEET_NAME=AI Lead Qualifier
GOOGLE_CREDENTIALS_PATH=credentials.json
MODEL_NAME=llama-3.3-70b-versatile
```

### 7. Run the web app

```bash
streamlit run app.py
```

### Or run via terminal only

```bash
python main.py
```

## Input CSV Format

Your CSV can use any of these column names:

| Field | Accepted column names |
|-------|----------------------|
| Name | name, full_name |
| Email | email, email_address |
| Company | company, company_name, organization |
| Job Title | job_title, title, position, role |
| Message | message, message_from_lead, notes |

## Output

| Field | Description |
|-------|-------------|
| Lead Score | 0–100 |
| Tier | Hot / Warm / Cold |
| Industry | Detected industry |
| Business Need | One sentence summary |
| Recommended Action | Schedule demo / Send case study / Nurture / Disqualify |
| Reasoning | AI explanation of the score |

## Scoring Logic

- Job seniority: C-level +25, VP/Director +20, Manager +15, IC +5
- Message quality: Specific pain point +25, vague +5
- Company fit: Tech/SaaS +20, mid-size +15, unclear +5
- Urgency signals: Strong +15, mild +8, none +0
- Budget/authority: Clear +15, implied +8, none +0

## Project Structure

```
ai-lead-qualifier/
├── app.py              # Streamlit web UI
├── main.py             # Terminal entry point
├── data/
│   └── leads_sample.csv
├── output/
│   └── results.csv
└── src/
    ├── config.py       # Environment settings
    ├── models.py       # Pydantic data models
    ├── loader.py       # CSV ingestion
    ├── prompt.py       # AI prompt template
    ├── llm_client.py   # Groq API + retry logic
    ├── parser.py       # JSON response parser
    ├── scorer.py       # Tier classification
    ├── storage.py      # Google Sheets + CSV output
    └── logger.py       # Rich terminal logging
```

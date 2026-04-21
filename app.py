import streamlit as st
import pandas as pd
import io
from src.config import settings
from src.loader import load_leads
from src.prompt import SYSTEM_PROMPT, format_prompt
from src.llm_client import call_llm
from src.parser import parse_response
from src.scorer import assign_tier, sort_by_score
from src.storage import save_to_sheets, save_to_csv

st.set_page_config(
    page_title="AI Lead Qualifier",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Lead Qualifier")
st.markdown("Upload a CSV of leads and get instant AI-powered scoring.")

with st.sidebar:
    st.header("How it works")
    st.markdown("""
    1. Upload your CSV file
    2. Click **Run Analysis**
    3. AI scores each lead 0–100
    4. Download results
    
    **Required columns:**
    - name
    - email
    - company
    - job_title
    - message
    """)
    st.divider()
    st.markdown("**Scoring tiers:**")
    st.success("Hot — score 75+")
    st.warning("Warm — score 45–74")
    st.error("Cold — score below 45")

uploaded_file = st.file_uploader("Upload leads CSV", type=["csv"])

if uploaded_file:
    df_preview = pd.read_csv(uploaded_file)
    st.subheader("Preview")
    st.dataframe(df_preview, use_container_width=True)
    st.caption(f"{len(df_preview)} leads loaded")

    if st.button("Run AI Analysis", type="primary", use_container_width=True):
        uploaded_file.seek(0)
        with open("data/temp_upload.csv", "wb") as f:
            f.write(uploaded_file.read())

        progress = st.progress(0, text="Starting analysis...")
        status = st.empty()
        leads_container = st.empty()

        from src.models import Lead
        import pandas as pd_internal

        df = pd_internal.read_csv("data/temp_upload.csv")
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        df = df.dropna(subset=["email"]).drop_duplicates(subset=["email"]).fillna("")

        leads = []
        for _, row in df.iterrows():
            # handle any column name variation
            def get_col(row, *options):
                for opt in options:
                    if opt in df.columns:
                        return str(row[opt]).strip()
                return ""

            leads.append(Lead(
                name=get_col(row, "name", "full_name", "lead_name"),
                email=get_col(row, "email", "email_address", "mail"),
                company=get_col(row, "company", "company_name", "organization", "org"),
                job_title=get_col(row, "job_title", "title", "position", "role", "designation"),
                message=get_col(row, "message", "message_from_lead", "notes", "description", "inquiry", "comment"),
            ))

        results = []
        for i, lead in enumerate(leads):
            status.text(f"Processing {lead.name}...")
            progress.progress((i + 1) / len(leads), text=f"Analyzing {i+1}/{len(leads)} leads...")
            try:
                prompt = f"{SYSTEM_PROMPT}\n{format_prompt(lead)}"
                raw = call_llm(prompt)
                result = parse_response(raw, lead)
                result = assign_tier(result)
                results.append(result)
            except Exception as e:
                st.warning(f"Failed to process {lead.name}: {e}")

        results = sort_by_score(results)
        progress.progress(1.0, text="Analysis complete!")
        status.empty()

        st.subheader("Results")

        col1, col2, col3, col4 = st.columns(4)
        hot = sum(1 for r in results if r.tier == "Hot")
        warm = sum(1 for r in results if r.tier == "Warm")
        cold = sum(1 for r in results if r.tier == "Cold")
        col1.metric("Total Leads", len(results))
        col2.metric("Hot", hot)
        col3.metric("Warm", warm)
        col4.metric("Cold", cold)

        st.divider()

        for r in results:
            if r.tier == "Hot":
                color = "🔴"
                badge = st.success
            elif r.tier == "Warm":
                color = "🟡"
                badge = st.warning
            else:
                color = "🔵"
                badge = st.info

            with st.expander(f"{color} {r.name} — {r.company} — Score: {r.lead_score} — {r.tier}"):
                c1, c2 = st.columns(2)
                c1.markdown(f"**Email:** {r.email}")
                c1.markdown(f"**Job Title:** {r.job_title}")
                c1.markdown(f"**Industry:** {r.industry}")
                c2.markdown(f"**Business Need:** {r.business_need}")
                c2.markdown(f"**Recommended Action:** {r.recommended_action}")
                st.markdown(f"**AI Reasoning:** {r.reasoning}")

        st.divider()

        rows = []
        for r in results:
            rows.append({
                "Name": r.name, "Email": r.email, "Company": r.company,
                "Job Title": r.job_title, "Score": r.lead_score,
                "Tier": r.tier, "Industry": r.industry,
                "Business Need": r.business_need,
                "Recommended Action": r.recommended_action,
                "Reasoning": r.reasoning
            })
        df_results = pd.DataFrame(rows)

        csv_buffer = io.StringIO()
        df_results.to_csv(csv_buffer, index=False)

        st.download_button(
            label="Download Results CSV",
            data=csv_buffer.getvalue(),
            file_name="lead_results.csv",
            mime="text/csv",
            use_container_width=True
        )

        try:
            save_to_sheets(results)
            st.success("Results also saved to Google Sheets")
        except Exception as e:
            st.warning(f"Google Sheets save failed: {e}")
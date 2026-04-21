import sys
from src.config import settings
from src.loader import load_leads
from src.prompt import SYSTEM_PROMPT, format_prompt
from src.llm_client import call_llm
from src.parser import parse_response
from src.scorer import assign_tier, sort_by_score
from src.storage import save_to_sheets, save_to_csv
from src.logger import log_info, log_error, get_progress, print_summary_table, console

CSV_PATH = "data/leads_sample.csv"


def main():
    console.rule("[bold blue]AI Lead Qualifier[/bold blue]")

    try:
        leads = load_leads(CSV_PATH)
    except Exception as e:
        log_error(f"Failed to load leads: {e}")
        sys.exit(1)

    results = []

    with get_progress() as progress:
        task = progress.add_task("Processing leads...", total=len(leads))

        for lead in leads:
            try:
                prompt = f"{SYSTEM_PROMPT}\n{format_prompt(lead)}"
                raw = call_llm(prompt)
                result = parse_response(raw, lead)
                result = assign_tier(result)
                results.append(result)
                log_info(f"{lead.name} — Score: {result.lead_score} — Tier: {result.tier}")

            except Exception as e:
                log_error(f"Failed to process {lead.name}: {e}")

            progress.advance(task)

    results = sort_by_score(results)

    console.rule("[bold green]Saving Results[/bold green]")

    save_to_csv(results)

    try:
        save_to_sheets(results)
    except Exception as e:
        log_error(f"Sheets upload failed, CSV still saved: {e}")

    console.rule("[bold magenta]Summary[/bold magenta]")
    print_summary_table(results)

    hot = sum(1 for r in results if r.tier == "Hot")
    warm = sum(1 for r in results if r.tier == "Warm")
    cold = sum(1 for r in results if r.tier == "Cold")

    log_info(f"Total: {len(results)} | Hot: {hot} | Warm: {warm} | Cold: {cold}")
    console.rule("[bold blue]Done[/bold blue]")


if __name__ == "__main__":
    main()
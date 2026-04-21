from src.models import LeadResult


def assign_tier(result: LeadResult) -> LeadResult:
    score = result.lead_score

    if score >= 75:
        tier = "Hot"
    elif score >= 45:
        tier = "Warm"
    else:
        tier = "Cold"

    result.tier = tier
    return result


def sort_by_score(results: list[LeadResult]) -> list[LeadResult]:
    return sorted(results, key=lambda r: r.lead_score, reverse=True)
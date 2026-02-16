from utils import validate_positive, safe_tool


@safe_tool
def calculate_emergency_fund(
    monthly_expenses: float,
    months: int = 6
):
    validate_positive(monthly_expenses, "monthly_expenses")
    validate_positive(months, "months")

    required_fund = monthly_expenses * months

    return {
        "recommended_emergency_fund": round(required_fund, 2),
        "months_covered": months
    }

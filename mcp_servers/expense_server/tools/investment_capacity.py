from utils import validate_positive, safe_tool


@safe_tool
def estimate_investment_capacity(
    monthly_income: float,
    monthly_expenses: float,
    emergency_fund_goal: float = 0,
    current_emergency_savings: float = 0
):
    validate_positive(monthly_income, "monthly_income")
    validate_positive(monthly_expenses, "monthly_expenses")

    savings = monthly_income - monthly_expenses

    if savings <= 0:
        raise ValueError("No surplus available for investment.")

    remaining_emergency_gap = max(
        0,
        emergency_fund_goal - current_emergency_savings
    )

    return {
        "monthly_surplus": round(savings, 2),
        "emergency_gap": round(remaining_emergency_gap, 2),
        "available_for_investment": round(savings, 2)
    }

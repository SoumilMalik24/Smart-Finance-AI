from utils import validate_positive, safe_tool


@safe_tool
def calculate_savings_rate(
    monthly_income: float,
    monthly_expenses: float
):
    validate_positive(monthly_income, "monthly_income")
    validate_positive(monthly_expenses, "monthly_expenses")

    if monthly_expenses > monthly_income:
        raise ValueError("Expenses cannot exceed income.")

    savings = monthly_income - monthly_expenses
    savings_rate = (savings / monthly_income) * 100

    return {
        "monthly_savings": round(savings, 2),
        "savings_rate_percent": round(savings_rate, 2)
    }

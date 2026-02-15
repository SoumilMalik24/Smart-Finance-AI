from utils import validate_positive, safe_tool

@safe_tool
def calculate_sip_future_value(
    monthly_investment: float,
    annual_return: float,
    years: int
):
    validate_positive(monthly_investment, "monthly_investment")
    validate_positive(annual_return, "annual_return")
    validate_positive(years, "years")

    r = annual_return / 100 / 12
    n = years * 12

    if r == 0:
        future_value = monthly_investment * n
    else:
        future_value = monthly_investment * (((1 + r)**n - 1) / r) * (1 + r)

    total_invested = monthly_investment * n
    total_gain = future_value - total_invested

    return {
        "total_invested": round(total_invested, 2),
        "future_value": round(future_value, 2),
        "total_gain": round(total_gain, 2)
    }
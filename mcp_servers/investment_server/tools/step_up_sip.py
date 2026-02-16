from utils import validate_positive, safe_tool

@safe_tool
def simulate_step_up_sip(
    monthly_investment: float,
    annual_step_up_percent: float,
    annual_return: float,
    years: int
):
    validate_positive(monthly_investment, "monthly_investment")
    validate_positive(years, "years")

    r = annual_return / 100
    total_invested = 0
    portfolio_value = 0

    yearly_data = []

    for year in range(1, years + 1):
        yearly_investment = monthly_investment * 12
        total_invested += yearly_investment
        portfolio_value = (portfolio_value + yearly_investment) * (1 + r)

        yearly_data.append({
            "year": year,
            "invested": round(total_invested, 2),
            "value": round(portfolio_value, 2)
        })

        monthly_investment *= (1 + annual_step_up_percent / 100)

    return {"yearly_data": yearly_data}

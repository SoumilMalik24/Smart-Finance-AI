from utils import validate_positive, safe_tool

@safe_tool
def simulate_lump_sum_growth(
    initial_investment: float,
    annual_return: float,
    years: int
):
    validate_positive(initial_investment, "initial_investment")
    validate_positive(annual_return, "annual_return")
    validate_positive(years, "years")

    portfolio_value = initial_investment
    yearly_data = []

    for year in range(1, years + 1):
        portfolio_value *= (1 + annual_return / 100)

        yearly_data.append({
            "year": year,
            "value": round(portfolio_value, 2)
        })

    return {
        "initial_investment": initial_investment,
        "yearly_data": yearly_data
    }

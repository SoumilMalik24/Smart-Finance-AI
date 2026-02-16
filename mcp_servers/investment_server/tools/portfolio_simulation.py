from utils import validate_positive, safe_tool

@safe_tool
def simulate_portfolio_allocation(
    initial_investment: float,
    equity_percent: float,
    equity_return: float,
    debt_return: float,
    years: int
):
    validate_positive(initial_investment, "initial_investment")

    equity = initial_investment * (equity_percent / 100)
    debt = initial_investment * (1 - equity_percent / 100)

    yearly_data = []

    for year in range(1, years + 1):
        equity *= (1 + equity_return / 100)
        debt *= (1 + debt_return / 100)

        total_value = equity + debt

        yearly_data.append({
            "year": year,
            "portfolio_value": round(total_value, 2)
        })

    return {"yearly_data": yearly_data}

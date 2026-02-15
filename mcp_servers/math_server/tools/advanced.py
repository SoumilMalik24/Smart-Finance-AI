import random
from utils import validate_positive, safe_tool

@safe_tool
def calculate_cagr(
    initial_value: float,
    final_value: float,
    years: int
):
    validate_positive(initial_value, "initial_value")
    validate_positive(final_value, "final_value")
    validate_positive(years, "years")

    cagr = ((final_value / initial_value) ** (1 / years) - 1) * 100
    return {"cagr_percent": round(cagr, 2)}


@safe_tool
def monte_carlo_simulation(
    initial_investment: float,
    annual_return: float,
    volatility: float,
    years: int,
    simulations: int = 1000
):
    validate_positive(initial_investment, "initial_investment")
    validate_positive(years, "years")

    results = []

    for _ in range(simulations):
        value = initial_investment
        for _ in range(years):
            simulated_return = random.gauss(annual_return, volatility) / 100
            value *= (1 + simulated_return)
        results.append(value)

    results.sort()

    return {
        "median": round(results[len(results)//2], 2),
        "p10": round(results[int(0.1*len(results))], 2),
        "p90": round(results[int(0.9*len(results))], 2)
    }

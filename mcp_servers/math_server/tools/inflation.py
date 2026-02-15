from utils import validate_positive, safe_tool

@safe_tool
def inflation_adjusted_value(
    present_value: float,
    inflation_rate: float,
    years: int
):
    validate_positive(present_value, "present_value")
    validate_positive(inflation_rate, "inflation_rate")
    validate_positive(years, "years")

    future_value = present_value * ((1 + inflation_rate / 100) ** years)

    return {"future_value": round(future_value, 2)}


@safe_tool
def real_rate_of_return(
    nominal_return: float,
    inflation_rate: float
):
    validate_positive(nominal_return, "nominal_return")
    validate_positive(inflation_rate, "inflation_rate")

    real_return = ((1 + nominal_return/100) / (1 + inflation_rate/100) - 1) * 100

    return {"real_return_percent": round(real_return, 2)}

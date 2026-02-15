from utils import validate_positive, safe_tool

@safe_tool
def retirement_corpus_required(
    annual_expense: float,
    years_after_retirement: int,
    annual_return: float
):
    validate_positive(annual_expense, "annual_expense")
    validate_positive(years_after_retirement, "years_after_retirement")
    validate_positive(annual_return, "annual_return")

    r = annual_return / 100
    corpus = annual_expense * ((1 - (1 + r) ** -years_after_retirement) / r)

    return {"required_corpus": round(corpus, 2)}


@safe_tool
def required_sip_for_goal(
    target_amount: float,
    annual_return: float,
    years: int
):
    validate_positive(target_amount, "target_amount")
    validate_positive(annual_return, "annual_return")
    validate_positive(years, "years")

    r = annual_return / 100 / 12
    n = years * 12

    sip = target_amount / ((((1 + r)**n - 1) / r) * (1 + r))

    return {"required_monthly_investment": round(sip, 2)}

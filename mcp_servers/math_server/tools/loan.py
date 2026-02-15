from utils import validate_positive, safe_tool

@safe_tool
def calculate_emi(
    principal: float,
    annual_rate: float,
    years: int
):
    validate_positive(principal, "principal")
    validate_positive(annual_rate,"annual_rate")
    validate_posoitive(years, "years")

    r = annual / 100 / 12
    n = years * 12

    if r == 0:
        emi = principal / n
    else:
        emi = principal * r * (1+r)**n / ((1+r)**n -1)

    return{
        "emi": round(emi,2),
        "total_payment": round(emi*n,2),
        "total_interest": round(emi*n - principal,2)
    }

@safe_tool
def generate_amortization_schedule(
    principal: float,
    annual_rate: float,
    years: int
):
    r = annual_rate / 100 / 12
    n = years * 12
    emi = calculate_emi(principal, annual_rate, years)["data"]["emi"]

    balance = principal
    schedule = []

    for month in range(1, n + 1):
        interest = balance * r
        principal_paid = emi - interest
        balance -= principal_paid

        schedule.append({
            "month": month,
            "interest": round(interest, 2),
            "principal_paid": round(principal_paid, 2),
            "remaining_balance": round(max(balance, 0), 2)
        })

    return {"schedule": schedule}
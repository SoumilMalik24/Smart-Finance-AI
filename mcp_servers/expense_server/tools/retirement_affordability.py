from utils import validate_positive, safe_tool


@safe_tool
def check_retirement_affordability(
    current_savings: float,
    required_corpus: float
):
    validate_positive(current_savings, "current_savings")
    validate_positive(required_corpus, "required_corpus")

    funded_percent = (current_savings / required_corpus) * 100

    return {
        "funded_percent": round(funded_percent, 2),
        "is_on_track": funded_percent >= 100
    }

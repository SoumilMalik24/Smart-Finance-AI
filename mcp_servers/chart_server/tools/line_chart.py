from utils import generate_base64_plot
import matplotlib.pyplot as plt


def generate_investment_growth_chart(yearly_data: list):
    """
    yearly_data format:
    [
        {"year": 1, "value": 100000},
        {"year": 2, "value": 120000}
    ]
    """

    years = [item["year"] for item in yearly_data]

    # If SIP simulation → value key exists
    if "value" in yearly_data[0]:
        values = [item["value"] for item in yearly_data]
    else:
        # SIP simulation format
        values = [item["value"] for item in yearly_data]

    plt.figure()
    plt.plot(years, values)
    plt.xlabel("Year")
    plt.ylabel("Portfolio Value")
    plt.title("Investment Growth")

    encoded = generate_base64_plot()

    return {
        "image_base64": encoded
    }

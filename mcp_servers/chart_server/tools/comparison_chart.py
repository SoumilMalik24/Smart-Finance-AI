from utils import generate_base64_plot
import matplotlib.pyplot as plt


def generate_comparison_chart(
    data_1: list,
    data_2: list,
    label_1: str,
    label_2: str
):
    years_1 = [item["year"] for item in data_1]
    values_1 = [item["value"] for item in data_1]

    years_2 = [item["year"] for item in data_2]
    values_2 = [item["value"] for item in data_2]

    plt.figure()
    plt.plot(years_1, values_1)
    plt.plot(years_2, values_2)

    plt.xlabel("Year")
    plt.ylabel("Portfolio Value")
    plt.title("Strategy Comparison")

    encoded = generate_base64_plot()

    return {
        "image_base64": encoded
    }

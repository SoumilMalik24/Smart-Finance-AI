import io
import base64
import matplotlib.pyplot as plt


def generate_base64_plot():
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    encoded = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()
    plt.close()
    return encoded

import sys
import os

# Ensure local modules are importable in cloud environment
# where working directory is /app (repo root), not /app/mcp_servers/chart_server_new
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastmcp import FastMCP
from logger import setup_logger
from tools import (
    generate_investment_growth_chart,
    generate_comparison_chart
)

logger = setup_logger()
mcp = FastMCP("Chart Server")


@mcp.tool()
def generate_growth_chart_tool(yearly_data: list):
    logger.info("Generating investment growth chart")
    result = generate_investment_growth_chart(yearly_data)
    logger.info("Chart generated successfully")
    return result


@mcp.tool()
def generate_comparison_chart_tool(
    data_1: list,
    data_2: list,
    label_1: str,
    label_2: str
):
    logger.info("Generating comparison chart")
    result = generate_comparison_chart(
        data_1,
        data_2,
        label_1,
        label_2
    )
    logger.info("Comparison chart generated successfully")
    return result


if __name__ == "__main__":
    logger.info("Starting Chart MCP Server...")
    mcp.run(
        transport="streamable_http",
        host="0.0.0.0",
        port=8003
    )

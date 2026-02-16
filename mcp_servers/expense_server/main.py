from fastmcp import FastMCP
from logger import setup_logger
from tools import (
    calculate_savings_rate,
    calculate_emergency_fund,
    estimate_investment_capacity,
    check_retirement_affordability
)

logger = setup_logger()
mcp = FastMCP("Expense & Budget Server")


@mcp.tool()
def calculate_savings_rate_tool(
    monthly_income: float,
    monthly_expenses: float
):
    logger.info("Savings rate calculation requested")
    return calculate_savings_rate(
        monthly_income,
        monthly_expenses
    )


@mcp.tool()
def calculate_emergency_fund_tool(
    monthly_expenses: float,
    months: int = 6
):
    logger.info("Emergency fund calculation requested")
    return calculate_emergency_fund(
        monthly_expenses,
        months
    )


@mcp.tool()
def estimate_investment_capacity_tool(
    monthly_income: float,
    monthly_expenses: float,
    emergency_fund_goal: float = 0,
    current_emergency_savings: float = 0
):
    logger.info("Investment capacity estimation requested")
    return estimate_investment_capacity(
        monthly_income,
        monthly_expenses,
        emergency_fund_goal,
        current_emergency_savings
    )


@mcp.tool()
def check_retirement_affordability_tool(
    current_savings: float,
    required_corpus: float
):
    logger.info("Retirement affordability check requested")
    return check_retirement_affordability(
        current_savings,
        required_corpus
    )


if __name__ == "__main__":
    logger.info("Starting Expense MCP Server...")
    mcp.run(
        transport="streamable_http",
        host="0.0.0.0",
        port=8004
    )

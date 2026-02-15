from fastmcp import FastMCP
from logger import setup_logger
from tools import (
    calculate_sip_future_value as sip_logic,
    calculate_emi as emi_logic,
    generate_amortization_schedule as amort_logic,
    inflation_adjusted_value as inflation_logic,
    real_rate_of_return as real_return_logic,
    retirement_corpus_required as retirement_logic,
    required_sip_for_goal as goal_sip_logic,
    calculate_cagr as cagr_logic,
    monte_carlo_simulation as mc_logic
)

logger = setup_logger()
mcp = FastMCP("Financial Math Server")


# =============================
# Tool Wrappers (Decorator Style)
# =============================

@mcp.tool()
def calculate_sip_future_value(
    monthly_investment: float,
    annual_return: float,
    years: int
):
    logger.info("SIP calculation requested")
    return sip_logic(
        monthly_investment,
        annual_return,
        years
    )


@mcp.tool()
def calculate_emi(
    principal: float,
    annual_rate: float,
    years: int
):
    logger.info("EMI calculation requested")
    return emi_logic(principal, annual_rate, years)


@mcp.tool()
def generate_amortization_schedule(
    principal: float,
    annual_rate: float,
    years: int
):
    logger.info("Amortization schedule requested")
    return amort_logic(principal, annual_rate, years)


@mcp.tool()
def inflation_adjusted_value(
    present_value: float,
    inflation_rate: float,
    years: int
):
    logger.info("Inflation adjustment requested")
    return inflation_logic(present_value, inflation_rate, years)


@mcp.tool()
def real_rate_of_return(
    nominal_return: float,
    inflation_rate: float
):
    logger.info("Real return calculation requested")
    return real_return_logic(nominal_return, inflation_rate)


@mcp.tool()
def retirement_corpus_required(
    annual_expense: float,
    years_after_retirement: int,
    annual_return: float
):
    logger.info("Retirement corpus calculation requested")
    return retirement_logic(
        annual_expense,
        years_after_retirement,
        annual_return
    )


@mcp.tool()
def required_sip_for_goal(
    target_amount: float,
    annual_return: float,
    years: int
):
    logger.info("Required SIP calculation requested")
    return goal_sip_logic(
        target_amount,
        annual_return,
        years
    )


@mcp.tool()
def calculate_cagr(
    initial_value: float,
    final_value: float,
    years: int
):
    logger.info("CAGR calculation requested")
    return cagr_logic(
        initial_value,
        final_value,
        years
    )


@mcp.tool()
def monte_carlo_simulation(
    initial_investment: float,
    annual_return: float,
    volatility: float,
    years: int,
    simulations: int = 1000
):
    logger.info("Monte Carlo simulation requested")
    return mc_logic(
        initial_investment,
        annual_return,
        volatility,
        years,
        simulations
    )


# =============================
# Health Check Endpoint
# =============================

@mcp.tool()
def health_check():
    return {
        "status": "healthy",
        "service": "financial-math-server"
    }


# =============================
# Server Start
# =============================

if __name__ == "__main__":
    logger.info("Starting Financial Math MCP Server...")
    mcp.run(
        transport="streamable_http",
        host="0.0.0.0",
        port=8001
    )

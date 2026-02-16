from fastmcp import FastMCP
from logger import setup_logger
from tools import (
    simulate_sip_growth,
    simulate_lump_sum_growth,
    simulate_step_up_sip,
    simulate_portfolio_allocation
)

logger = setup_logger()
mcp = FastMCP("Investment Simulation Server")


# ==========================
# Tool Wrappers With Logging
# ==========================

@mcp.tool()
def simulate_sip_growth_tool(
    monthly_investment: float,
    annual_return: float,
    years: int
):
    logger.info(
        f"SIP simulation requested | monthly={monthly_investment}, "
        f"return={annual_return}, years={years}"
    )

    result = simulate_sip_growth(
        monthly_investment,
        annual_return,
        years
    )

    logger.info("SIP simulation completed")
    return result


@mcp.tool()
def simulate_lump_sum_growth_tool(
    initial_investment: float,
    annual_return: float,
    years: int
):
    logger.info(
        f"Lump sum simulation requested | initial={initial_investment}, "
        f"return={annual_return}, years={years}"
    )

    result = simulate_lump_sum_growth(
        initial_investment,
        annual_return,
        years
    )

    logger.info("Lump sum simulation completed")
    return result


@mcp.tool()
def simulate_step_up_sip_tool(
    monthly_investment: float,
    annual_step_up_percent: float,
    annual_return: float,
    years: int
):
    logger.info(
        f"Step-up SIP requested | monthly={monthly_investment}, "
        f"step_up={annual_step_up_percent}, return={annual_return}, years={years}"
    )

    result = simulate_step_up_sip(
        monthly_investment,
        annual_step_up_percent,
        annual_return,
        years
    )

    logger.info("Step-up SIP simulation completed")
    return result


@mcp.tool()
def simulate_portfolio_allocation_tool(
    initial_investment: float,
    equity_percent: float,
    equity_return: float,
    debt_return: float,
    years: int
):
    logger.info(
        f"Portfolio simulation requested | initial={initial_investment}, "
        f"equity%={equity_percent}, equity_return={equity_return}, "
        f"debt_return={debt_return}, years={years}"
    )

    result = simulate_portfolio_allocation(
        initial_investment,
        equity_percent,
        equity_return,
        debt_return,
        years
    )

    logger.info("Portfolio simulation completed")
    return result


# ==========================
# Server Start
# ==========================

if __name__ == "__main__":
    logger.info("Starting Investment Simulation MCP Server...")
    mcp.run(
        transport="streamable_http",
        host="0.0.0.0",
        port=8002
    )

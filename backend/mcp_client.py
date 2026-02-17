import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

# FastMCP Cloud requires authentication
# Set FASTMCP_API_KEY in your .env file
FASTMCP_API_KEY = os.getenv("FASTMCP_API_KEY", "")

AUTH_HEADERS = {
    "Authorization": f"Bearer {FASTMCP_API_KEY}"
} if FASTMCP_API_KEY else {}

SERVERS = {
    "math": {
        "transport": "streamable_http",
        "url": "https://fin-math-serv.fastmcp.app/mcp",
        "headers": AUTH_HEADERS,
    },
    "investment": {
        "transport": "streamable_http",
        "url": "https://fin-invst-serv.fastmcp.app/mcp",
        "headers": AUTH_HEADERS,
    },
    "expense": {
        "transport": "streamable_http",
        "url": "https://fin-expn-serv.fastmcp.app/mcp",
        "headers": AUTH_HEADERS,
    },
    "chart": {
        "transport": "streamable_http",
        "url": "https://fin-chart-serv.fastmcp.app/mcp",
        "headers": AUTH_HEADERS,
    }
}

# Module-level client instance — used in FastAPI lifespan
client = MultiServerMCPClient(SERVERS)

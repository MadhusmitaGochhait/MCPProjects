from mcp.server.fastmcp import FastMCP
from weather_api import fetch_current_weather, fetch_weather_on_date, geocode_location
from datetime import datetime
import logging
import signal
import sys

# Handle SIGPIPE gracefully to prevent crashes on broken pipes
def handle_sigpipe(signum, frame):
    sys.exit(0)

signal.signal(signal.SIGPIPE, handle_sigpipe)

# Suppress FastMCP debug messages
logging.getLogger("mcp").setLevel(logging.ERROR)

# Initialize the MCP server
mcp = FastMCP("weather_server")

# -----------------------
# Tool 1: Get current weather
# -----------------------
@mcp.tool()
async def get_weather(location: str):
    weather = fetch_current_weather(location)
    return {"location": location, "weather": weather}

# -----------------------
# Tool 2: Get weather for a specific date
# -----------------------
@mcp.tool()
async def get_weather_on_date(location: str, date: str):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    weather = fetch_weather_on_date(location, date_obj)
    return {"location": location, "date": date, "weather": weather}

# Run the MCP server
if __name__ == "__main__":
    mcp.run(transport="stdio")
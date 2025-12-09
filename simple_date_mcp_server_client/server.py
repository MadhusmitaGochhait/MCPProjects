from mcp.server.fastmcp import FastMCP
from datetime import datetime
from zoneinfo import ZoneInfo
import logging

# Suppress FastMCP debug messages
logging.getLogger("mcp").setLevel(logging.WARNING)

# Initialize the MCP server
mcp = FastMCP("date_server")

# Define the tool
@mcp.tool()
async def get_localdate(
    format: str = "%Y-%m-%dT%H:%M:%SZ", 
    timezone: str = "UTC"
    ):
    # Validate timezone
    try:
        tz = ZoneInfo(timezone)
    except Exception:
        return {
            "error": f"Invalid timezone '{timezone}'. Use a valid IANA name like 'America/Los_Angeles'."
        }
        # Current time in requested timezone
    try:    
        now = datetime.now(tz).strftime(format)
    except Exception as e:
        return {
            "error": f"Invalid format '{e}'. Use a valid format like '%%Y-%%m-%%d %%H:%%M:%%S'."
        }

    return {
        "date": now, 
        "timezone": timezone
        }

# Run the MCP server
if __name__ == "__main__":
    mcp.run(transport="stdio")
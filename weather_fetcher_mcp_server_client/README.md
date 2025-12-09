# Weather Fetcher MCP Server & Client

A Model Context Protocol (MCP) server and client implementation for fetching weather information. This project provides an MCP server that exposes weather tools and a client application to interact with the server.

## Features

- **Current Weather**: Get real-time weather information for any location
- **Weather Forecast**: Get weather forecasts for specific dates
- **MCP Protocol**: Built using FastMCP for efficient tool registration and communication
- **Async Support**: Fully asynchronous implementation for better performance

## Project Structure

```
weather_fetcher_mcp_server_client/
├── weather_mcpserver.py    # MCP server with weather tools
├── weather_client.py        # MCP client for testing
├── weather_api.py          # Weather API integration (WeatherAPI.com)
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Project configuration
└── README.md              # This file
```

## Installation

1. **Clone or navigate to the project directory**

2. **Install dependencies using uv** (recommended):
   ```bash
   uv sync
   ```

   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up WeatherAPI key** (if needed):
   - The project uses WeatherAPI.com for weather data
   - Update the `API_KEY` in `weather_api.py` if you have your own API key

## Usage

### Running the MCP Server

The MCP server runs in stdio mode and can be started directly:

```bash
uv run weather_mcpserver.py
```

Or with Python:
```bash
python weather_mcpserver.py
```

The server will listen on stdin/stdout for MCP protocol messages.

### Running the Client

The client demonstrates how to interact with the MCP server:

```bash
uv run weather_client.py
```

Or with Python:
```bash
python weather_client.py
```

The client will:
1. List all available tools
2. Call `get_weather` for San Francisco
3. Call `get_weather_on_date` for Sydney on a specific date

### Available Tools

#### 1. `get_weather`

Get the current weather for a given location.

**Parameters:**
- `location` (str): The name of the location (e.g., "New York", "Tokyo", "London")

**Returns:**
- Dictionary with `location` and `weather` fields

**Example:**
```python
result = await session.call_tool("get_weather", arguments={"location": "New York"})
```

#### 2. `get_weather_on_date`

Get the weather forecast for a specific location and date.

**Parameters:**
- `location` (str): The name of the location
- `date` (str): The date in YYYY-MM-DD format (e.g., "2025-12-22")

**Returns:**
- Dictionary with `location`, `date`, and `weather` fields

**Example:**
```python
result = await session.call_tool("get_weather_on_date", arguments={
    "location": "Tokyo",
    "date": "2025-12-22"
})
```

## Client API

### `list_weather_tool()`

Lists all available tools from the MCP server.

```python
async def list_weather_tool():
    # Returns list of available tools with their descriptions
```

### `main_tool(tool_name, tool_args=None)`

Calls a specific MCP tool with the provided arguments.

**Parameters:**
- `tool_name` (str): Name of the tool to call
- `tool_args` (dict, optional): Arguments to pass to the tool

**Example:**
```python
await main_tool("get_weather", tool_args={"location": "London"})
```

## Implementation Details

### Server Architecture

- **FastMCP**: Uses FastMCP framework for MCP server implementation
- **Async Tools**: All tools are implemented as async functions
- **Signal Handling**: Includes SIGPIPE handling to prevent crashes on client disconnection
- **Error Handling**: Graceful error handling for invalid locations and dates

### Weather API Integration

The project uses WeatherAPI.com for weather data:
- **Current Weather**: Uses `/v1/current.json` endpoint
- **Forecast**: Uses `/v1/forecast.json` endpoint
- Supports location names directly (no separate geocoding required)

### MCP Protocol

The server implements the MCP protocol over stdio:
- Tool registration via `@mcp.tool()` decorator
- Tool discovery via `list_tools()` method
- Tool execution via `call_tool()` method

## Troubleshooting

### Tool Cache Miss Error

If you encounter "Tool cache miss" errors:
1. Ensure the client calls `list_tools()` before calling tools
2. Check that tool docstrings are properly formatted
3. Verify the server is running and accessible

### BrokenPipeError

The server includes SIGPIPE signal handling to prevent crashes. If you still see this error:
1. Ensure the client doesn't disconnect prematurely
2. Check that the server process is running correctly
3. Verify stdio communication is working

### Weather Data Not Available

If weather data is not returned:
1. Check your internet connection
2. Verify the location name is valid
3. Check the WeatherAPI service status
4. Review error messages in the console

## Dependencies

- `mcp`: Model Context Protocol library
- `requests`: HTTP library for API calls

See `requirements.txt` or `pyproject.toml` for complete dependency list.

## Development

### Adding New Tools

To add a new tool to the MCP server:

1. Create an async function in `weather_mcpserver.py`
2. Decorate it with `@mcp.tool()`
3. Add appropriate docstring for tool description
4. Implement the tool logic

Example:
```python
@mcp.tool()
async def my_new_tool(param: str):
    """Description of what the tool does."""
    # Tool implementation
    return {"result": "value"}
```

## License

This project is an example to learn MCP implementation 

## Notes

- The server runs in stdio mode for MCP communication
- All tools are async to support efficient I/O operations
- The client demonstrates proper MCP session management with tool caching


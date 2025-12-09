# Simple Date MCP Server & Client
This is a demonstration project for learning MCP server/client patterns.
A Model Context Protocol (MCP) server and client implementation that provides date and time functionality with timezone support.

## Overview

This project consists of:
- **Server (`server.py`)**: An MCP server that exposes a `get_localdate` tool for retrieving formatted dates/times in various timezones
- **Client (`client.py`)**: An MCP client that connects to the server and demonstrates direct usage of the date tool
- **Client LLM (`client_llm.py`)**: An advanced client that integrates OpenAI's API with the MCP server, allowing LLMs to automatically call MCP tools through function calling

## Features

- Get current date/time in any IANA timezone
- Customizable date/time format strings
- Error handling for invalid timezones and formats
- Clean output with suppressed debug messages
- **OpenAI Integration**: Use OpenAI models to intelligently call MCP tools via function calling

## Prerequisites

- Python 3.12 or higher
- `uv` package manager (for running the project)
- MCP Python SDK (`mcp` package)
- **For `client_llm.py`**: OpenAI API key (set in `.env` file or environment variable)

## Installation Steps

### Step 1: Install uv (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or on macOS with Homebrew:
```bash
brew install uv
```

### Step 2: Install Dependencies
uv sync
```
This will install the required MCP package and dependencies.

### Step 4: Setup OpenAI API Key (for client_llm.py)

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_api_key_here
```

Or export it as an environment variable:

```bash
export OPENAI_API_KEY=your_api_key_here
```

## Usage

### Running the Server

The server can be run directly:

```bash
uv run server.py
```

The server uses stdio transport and will wait for client connections.

### Running the Client

Run the basic client to test the server:

```bash
uv run client.py
```

The client will:
1. List available tools
2. Call the `get_localdate` tool with various formats and timezones
3. Display the results

### Running the LLM Client

Run the OpenAI-integrated client for intelligent tool calling:


```bash
uv run client_llm.py
```

The LLM client (`client_llm.py`) will:
1. Connect to the MCP server and retrieve available tools
2. Convert MCP tools to OpenAI function calling format
3. Send your message to OpenAI with the tools available
4. Automatically execute tool calls when the LLM determines they're needed
5. Return a natural language response based on tool results

**Example interaction:**
- User asks: "What's the current date and time in IST?"
- OpenAI model recognizes the need for date/time information
- Model calls `get_localdate` tool with appropriate timezone parameter
- Tool result is returned to the model
- Model provides a natural language answer

## Examples

### Example 1: Default Format (UTC)

```python
asyncio.run(main_tool("get_localdate"))
# Output: 2025-12-08T16:20:47Z
```

### Example 2: Custom Format

```python
asyncio.run(main_tool("get_localdate", tool_args={"format":"%A, %B %d %Y"}))
# Output: Tuesday, December 09 2025
```

### Example 3: Custom Format with Timezone

```python
asyncio.run(main_tool("get_localdate", tool_args={
    "format":"%A, %B %d %Y at %H:%M:%S",
    "timezone":"Asia/Kolkata"
}))
# Output: Tuesday, December 09 2025 at 06:31:05
```

### Example 4: Timezone Only (Default Format)

```python
asyncio.run(main_tool("get_localdate", tool_args={"timezone":"Europe/London"}))
# Output: 2025-12-09T01:01:05Z
```

### Example 5: Using the LLM Client

```python
# In client_llm.py
result = asyncio.run(chat_with_mcp_tools("What's the current date and time in IST?"))
print(result)
# Output: The current date and time in IST (Asia/Kolkata) is 2025-12-09T06:31:05+05:30
```

The LLM client allows natural language queries - the OpenAI model automatically determines when to use tools and how to call them based on your question.

## API Reference

### `get_localdate` Tool

**Parameters:**
- `format` (str, optional): Date/time format string. Defaults to `"%Y-%m-%dT%H:%M:%SZ"`
  - Uses Python's `strftime` format codes
  - Example: `"%Y-%m-%d %H:%M:%S"`, `"%A, %B %d %Y"`
- `timezone` (str, optional): IANA timezone name. Defaults to `"UTC"`
  - Examples: `"America/New_York"`, `"Europe/London"`, `"Asia/Kolkata"`, `"Europe/Paris"`

**Returns:**
- Dictionary with:
  - `date`: Formatted date/time string
  - `timezone`: The timezone used
- Or error dictionary if timezone or format is invalid

**Common Format Codes:**
- `%Y` - Year with century (e.g., 2025)
- `%m` - Month as number (01-12)
- `%d` - Day of month (01-31)
- `%H` - Hour (00-23)
- `%M` - Minute (00-59)
- `%S` - Second (00-59)
- `%A` - Full weekday name (e.g., Tuesday)
- `%B` - Full month name (e.g., December)

## Project Structure

```
simple_date_mcp_server_client/
├── server.py          # MCP server with get_localdate tool
├── client.py          # Basic MCP client demonstrating direct tool usage
├── client_llm.py      # Advanced client integrating OpenAI API with MCP tools
├── README.md          # This file
└── .env               # Environment variables (create this, add OPENAI_API_KEY)
```

## How client_llm.py Works

The `client_llm.py` file bridges OpenAI's function calling API with your MCP server:

1. **Tool Discovery**: Connects to MCP server and lists available tools
2. **Format Conversion**: Converts MCP tool schemas to OpenAI function calling format
3. **Intelligent Tool Selection**: OpenAI model decides when and which tools to call
4. **Tool Execution**: Executes tool calls via MCP client and feeds results back to the model
5. **Natural Responses**: Model generates natural language responses based on tool results

The process supports multi-turn conversations where the model can:
- Call tools as needed
- Process tool results
- Make follow-up tool calls if necessary
- Provide final answers in natural language

## Error Handling

The server validates:
- **Timezone**: Must be a valid IANA timezone name (e.g., `"Asia/Kolkata"`)
- **Format**: Must be a valid `strftime` format string

If validation fails, the server returns an error dictionary with a descriptive message.

## Troubleshooting

### Import Errors

If you encounter import errors:
1. Ensure `uv` is installed and in your PATH
2. Run `uv sync` to install dependencies
3. Always use `uv run` to execute Python scripts

### Timezone Errors

If you get timezone-related errors:
- Ensure you're using valid IANA timezone names
- Common timezones: `UTC`, `America/New_York`, `Europe/London`, `Asia/Kolkata`, `Europe/Paris`

### Format Errors

If format strings don't work:
- Remember to escape `%` as `%%` in format strings when passing through some interfaces
- Use Python `strftime` format codes
- Test simple formats first before complex ones

### OpenAI API Errors (client_llm.py)

If you encounter errors with `client_llm.py`:
1. Ensure your OpenAI API key is set correctly in `.env` file or environment variable
2. Verify you have API credits/quota available
3. Check that the `openai` package is installed: `uv sync`
4. Ensure the MCP server can start (test with `client.py` first)



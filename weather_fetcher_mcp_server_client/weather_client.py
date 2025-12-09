import mcp
from mcp.client.stdio import stdio_client
from mcp.client.stdio import StdioServerParameters
import asyncio

params = StdioServerParameters(command="uv", args=["run", "weather_mcpserver.py"], env=None)
async def list_weather_tool():
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")
            print() 
            return tools_result.tools

async def main_tool(tool_name,tool_args=None):
  async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            # List tools first to populate cache
            await session.list_tools()
            #call the  mcp tool
            tools_result = await session.call_tool(tool_name, arguments=tool_args or {})
            print(tools_result.content[0].text)
if __name__ == "__main__":
    asyncio.run(list_weather_tool())
    asyncio.run(main_tool("get_weather", tool_args={"location":"San Fransisco"}))
    asyncio.run(main_tool("get_weather_on_date", tool_args={"location":"sydney","date":"2025-12-22"}))

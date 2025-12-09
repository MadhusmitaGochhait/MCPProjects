import mcp
from mcp.client.stdio import stdio_client
from mcp.client.stdio import StdioServerParameters
import asyncio

params = StdioServerParameters(command="uv", args=["run", "server.py"], env=None)
async def list_date_tool():
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
            #call the date tool
            tools_result = await session.call_tool(tool_name, arguments=tool_args or {})
            print(tools_result.content[0].text)


if __name__ == "__main__":
    asyncio.run(list_date_tool())
    #call the date tool with default format
    asyncio.run(main_tool("get_localdate"))
    asyncio.run(main_tool("get_localdate", tool_args={"format":"%A, %B %d %Y"}))
  
    asyncio.run(main_tool("get_localdate", tool_args={"format":"%A, %B %d %Y at %H:%M:%S","timezone":"Asia/Kolkata"}))
    asyncio.run(main_tool("get_localdate", tool_args={"format":"%A, %B %d %Y at %H:%M:%S","timezone":"Europe/Paris"}))
    asyncio.run(main_tool("get_localdate", tool_args={"timezone":"Europe/london"}))
  

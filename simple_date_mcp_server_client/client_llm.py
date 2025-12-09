import mcp
from mcp.client.stdio import stdio_client
from mcp.client.stdio import StdioServerParameters
from openai import OpenAI
import asyncio
import json
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv(override=True)

params = StdioServerParameters(command="uv", args=["run", "server.py"], env=None)

async def chat_with_mcp_tools(user_message: str, model: str = "gpt-4o-mini") -> str:
    """
    Use OpenAI to call MCP server tools via the client.
    
    Args:
        user_message: The user's message
        model: OpenAI model to use (default: gpt-4o-mini)
    
    Returns:
        The final response from OpenAI
    """
    client = OpenAI()
    
    # Get MCP tools and convert to OpenAI format
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            tools_result = await session.list_tools()
            
            # Convert MCP tools to OpenAI format
            openai_tools = []
            for tool in tools_result.tools:
                properties = {}
                required = []
                if tool.inputSchema and "properties" in tool.inputSchema:
                    properties = tool.inputSchema["properties"]
                    required = tool.inputSchema.get("required", [])
                
                openai_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or f"Calls the {tool.name} tool",
                        "parameters": {
                            "type": "object",
                            "properties": properties,
                            "required": required
                        }
                    }
                })
    
    # Initialize conversation
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant with access to date and time tools. Use the get_localdate tool when users ask about dates, times, or timezones."
        },
        {
            "role": "user",
            "content": user_message
        }
    ]
    
    # Chat loop - continue until no more tool calls
    max_iterations = 10
    iteration = 0
    
    while iteration < max_iterations:
        # Make OpenAI API call
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=openai_tools,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        message_dict = {
            "role": message.role,
            "content": message.content
        }
        
        # Check if OpenAI wants to call a tool
        if message.tool_calls:
            message_dict["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in message.tool_calls
            ]
            
            messages.append(message_dict)
            
            # Execute tool calls via MCP client
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                # Execute tool via MCP client
                async with stdio_client(params) as streams:
                    async with mcp.ClientSession(*streams) as session:
                        await session.initialize()
                        tools_result = await session.call_tool(tool_name, arguments=tool_args)
                        
                        tool_result = tools_result.content[0].text if tools_result.content else json.dumps({"result": "No content returned"})
                
                # Add tool result to conversation
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": tool_result
                })
            
            iteration += 1
            continue
        else:
            messages.append(message_dict)
            return message.content or "No response generated"
    
    return "Maximum iterations reached. Please try again."


if __name__ == "__main__":
    # Example usage
    result = asyncio.run(chat_with_mcp_tools("What's the current date and time in ist and format as %H:%M:%S?"))
    print(result)


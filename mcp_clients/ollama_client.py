import asyncio
import json

from langchain_ollama.chat_models import ChatOllama
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


MODEL = "qwen3:8b"

QUERIES = [
    "Get customer information for customer having CUST123 as ID, and list their orders, then summarize it.",
    "Get customer information for customer named Alice Johnson, and get the name of the items she ordered.",
    "Get the name of items ordered by customer having CUST123 as ID",
    "Get the name of items ordered by customer having CUST123 as ID, check inventory for each of these items",
]
QNUM = 0


async def main():
    # Initialize the Ollama LLM (using a model that supports tool calling)
    # Other options: "llama3.1", "llama3.2", "qwen2.5", "mistral"
    llm = ChatOllama(model=MODEL, base_url="http://localhost:11434", reasoning=True)

    # Connect to the MCP server
    async with streamablehttp_client("http://localhost:8000/mcp") as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # Get available tools from MCP server
            tools_response = await session.list_tools()
            tools = tools_response.tools

            # Convert MCP tools to LangChain tool format
            langchain_tools = []
            for tool in tools:
                tool_schema = {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema,
                    },
                }
                langchain_tools.append(tool_schema)

            user_query = QUERIES[QNUM]

            # Initial LLM call with tools
            messages = [{"role": "user", "content": user_query}]
            response = llm.bind_tools(langchain_tools).invoke(messages)

            # Process tool calls
            messages.append({"role": "assistant", "content": response.content, "tool_calls": response.tool_calls})

            print(f"\nLLM decided to call {len(response.tool_calls)} tool(s):\n")

            # Execute each tool call
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                print(f"Calling tool: {tool_name}")
                print(f"Arguments: {json.dumps(tool_args, indent=2)}")

                # Call the MCP tool
                result = await session.call_tool(tool_name, arguments=tool_args)
                tool_result = result.content[0].text

                print(f"Result: {tool_result}\n")

                # Add tool result to messages
                messages.append({"role": "tool", "content": tool_result, "tool_call_id": tool_call["id"]})

            # Final LLM call to synthesize results
            final_response = llm.invoke(messages)

            print("\nFinal Response:")
            print(final_response.content)


if __name__ == "__main__":
    asyncio.run(main())

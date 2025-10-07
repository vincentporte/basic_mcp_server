
import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def main():
    #Connect to a streamable MCP server
    async with streamablehttp_client("http://localhost:8000/mcp") as (
            read_stream,
            write_stream,
            _,
        ):
            # Create a session using the client stream
            async with ClientSession(read_stream, write_stream) as session:
                # Init the connection
                await session.initialize()
                # List available tools

                response = await session.list_tools()
                tools = response.tools
                tool_names = [tool.name for tool in tools]
                tool_descriptions = [tool.description for tool in tools]

                print("\nYour server has the following tools:")
                for tool_name, tool_description in zip(tool_names, tool_descriptions):
                    print(f"{tool_name}: {tool_description}")

if __name__ == "__main__":
    asyncio.run(main())

import asyncio

from langchain_ollama.chat_models import ChatOllama
from mcp.client.streamable_http import streamablehttp_client
from mcp_use import MCPAgent, MCPClient


async def main():
    llm = ChatOllama(model="gemma3:4b", base_url="http://localhost:11434")


if __name__ ==  "__main__":
    asyncio.run(main())

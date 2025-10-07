# E-commerce MCP Server

A lightweight, asynchronous MCP server exposing essential e-commerce domain tools for customers, orders, and inventory management. Built with [FastMCP](https://github.com/ai-forever/fastmcp), this server demonstrates how to structure and deploy an MCP API accessible by large language models (LLMs) or other clients over stdio — ideal for local development and prototyping.

---

## Overview

This project implements an Model Context Protocol server with focused async tools that provide programmatic access to datas. MCP servers standardize the interface between clients (e.g., LLMs) and back-end resources by exposing **prompts**, **resources**, and **tools**.

- **Prompts:** User-facing templates guiding how LLMs interact with tools and data workflows.
- **Resources:** Data assets exposed to LLMs, such as databases or documents.
- **Tools:** Functions enabling LLMs to trigger real-world business logic and retrieve information.

This implementation follows the concepts from the [RealPython tutorial on Python MCP Servers](https://realpython.com/python-mcp/).

---

## Project Structure
- `mcp_servers/main.py`: MCP server definition with registered async tools
- `tests/test_server.py`: Pytest validating server startup and tool registration

## Key Implementation Details
### @mcp.tool() Decorator
- Marks functions as MCP tools exposed to clients.
- Converts tool signatures and docstrings into metadata for LLM consumption.
- Ensure all tools have clear, concise docstrings to enable descriptive automatic documentation and better prompting.

### `list_tools()`

- Automatically provided by the MCP framework.
- Lists all registered tools with their names and descriptions.
- No manual implementation needed.

---

## Usage
### Installation
Synchronize dependencies with:
`uv sync`

### Running the Server
Start the MCP server locally with unbuffered output to ensure stable stdio communication:
run `uv run python -u mcp_servers/main.py`
The `-u` flag ensures unbuffered output, which is necessary for proper stdio communication

### Running the Tests
Run the pytest suite to verify the server is working and exposes the expected tools:
`pytest -s` 
The `-s` command displays the output of `print()` calls in test.
The test script will launch the server as a subprocess communicating over stdio, then ensure all expected tools are registered and accessible.

---

## Notes

- This server uses stdio transport, which is suitable only for local testing with single client connections, lacking network accessibility and authentication. For production use, a different transport method should be used.
- The simulated latency (`asyncio.sleep(1)`) mimics asynchronous data retrieval and can be adjusted or removed as needed.

## License

This project is provided as-is with no explicit license.

# Links
* [Python MCP Server: Connect LLMs to Your Data](https://realpython.com/python-mcp/)
* [Build an MCP Server in Python with FastMCP](https://thepythoncode.com/article/fastmcp-mcp-client-server-todo-manager)
* [modelcontextprotocol.io - Build an MCP Server](https://modelcontextprotocol.io/docs/develop/build-serverhttps://modelcontextprotocol.io/docs/develop/build-server)
* [modelcontextprotocol.io - Build an MCP Client](https://modelcontextprotocol.io/docs/develop/build-client)
* [pypi - MCP lib](https://pypi.org/project/mcp/)
* [pypi - CLI for MCP Client for Ollama - An easy-to-use command for interacting with Ollama through MCP](https://pypi.org/project/ollmcp/)
* [Building a 100% Local MCP Client with Ollama: Secure and Private AI Tool Integration](https://atalupadhyay.wordpress.com/2025/05/21/building-a-100-local-mcp-client-with-ollama-secure-and-private-ai-tool-integration/)

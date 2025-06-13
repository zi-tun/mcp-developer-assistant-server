from server.server import mcp

# Import tools so they get registered via decorators
from server import server_tools
from agent import controller_tools

# Entry point to run the server
if __name__ == "__main__":
    print("Starting the MCP server...")
    mcp.run()

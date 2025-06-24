import argparse
from server.server import mcp

from server.tools import jira_tools

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", default="streamable-http")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--log", default="info")
    args = parser.parse_args()

    print(f"Starting the MCP server with transport={args.transport} on {args.host}:{args.port}...")
    mcp.run(transport=args.transport, host=args.host, port=args.port,log_level=args.log)
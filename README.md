<!-- mcp client repo prep -->
uv init mcp-jira-agent
cd mcp-jira-agent/
uv venv
source .venv/bin/activate
uv add "mcp[cli]"
create .vscode/mcp.json

<!-- mcp server build process -->
docker build -t mcp-jira-agent .
docker run -p 8080:8080 mcp-jira-agent

<!-- how to use this mcp tool locally -->
docker login containers.cisco.com
docker pull containers.cisco.com/zitun/mcp-jira-agent:jun_23_2025
docker run -p 8080:8080 containers.cisco.com/zitun/mcp-jira-agent:jun_23_2025

# 🧠 MCP tool to help speed up the development process for developer

A local AI assistant that helps developers understand JIRA tickets, suggest solutions, write code, generate tests, and create pull requests — all integrated with your workflow via VSCode.

---

## 🚀 Client Setup (VSCode + MCP CLI)

```bash
# Initialize MCP project
uv init your_mcp_client_project
cd your_mcp_client_project/

# Set up Python virtual environment
uv venv
source .venv/bin/activate


# Create MCP config (for VSCode extension to connect)
mkdir -p .vscode
touch .vscode/mcp.json
# .vscode/mcp.json
```{
  "servers": {
    "mcp-http-stream-server": {
      "type": "http",
      "url": "http://localhost:8080/mcp/stream"
    }
  }
}```

<!-- how to use this mcp tool locally -->
docker login containers.cisco.com
docker pull containers.cisco.com/zitun/mcp-jira-agent:jun_23_2025
docker run -p 8080:8080 containers.cisco.com/zitun/mcp-jira-agent:jun_23_2025



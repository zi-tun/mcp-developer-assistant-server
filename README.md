uv init mcp-jira-agent
 cd mcp-jira-agent/
 uv venv
 source .venv/bin/activate
 uv add "mcp[cli]"

docker build -t mcp-jira-agent .
docker run -p 8080:8080 mcp-jira-agent
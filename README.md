# 🤖 MCP Jira Agent

An AI-powered development assistant that integrates with JIRA and GitHub to help you understand tickets, generate implementation code, write tests, and create pull requests — all from within your VSCode workflow.

---

## 🚀 MCP Client Setup (VSCode)

Set up the MCP client project and CLI environment locally:

```bash
# Skip to "Create VSCode MCP Configuration" section if you already have a project setup.

# Initialize a new MCP client project
uv init your_mcp_client_project
cd your_mcp_client_project/

# Create a Python virtual environment
uv venv
source .venv/bin/activate
```

---

## 🛠️ Create VSCode MCP Configuration

Create the required VSCode config file:

```bash
mkdir -p .vscode
touch .vscode/mcp.json
```

Then edit `.vscode/mcp.json` with the following content:

```json
{
  "servers": {
    "mcp-http-stream-server": {
      "type": "http",
      "url": "http://localhost:8080/mcp/stream"
    }
  }
}
```

This tells your VSCode MCP extension to connect to your locally running MCP server.

---

## 🐳 Run the MCP Server via Docker (local only for now)

Each developer runs the MCP server locally in Docker. You don’t need to build the image yourself — a prebuilt image is available via Cisco Container Registry.

### Step 1: Authenticate with Cisco Container Registry

```bash
docker login containers.cisco.com
```

### Step 2: Pull the MCP Docker Image

```bash
docker pull containers.cisco.com/zitun/mcp-dev-assist-server:jun_23_2025
```
get the latest available tag

### Step 3: Run the MCP Server Locally

```bash
docker run -p 8080:8080 containers.cisco.com/zitun/mcp-dev-assist-server:jun_23_2025
```

The server will be available at [http://localhost:8080](http://localhost:8080).

---

## 💻 Using MCP in VSCode

Once the Docker container is running:

1. Open your project in VSCode (where `.vscode/mcp.json` exists).
2. The MCP extension will automatically connect to the local server at `http://localhost:8080/mcp/stream`.
3. You can now use the extension to:
   - Understand JIRA tickets
   - Generate implementation steps or code
   - Write unit tests
   - Create pull requests
4. In VSCode agent mode, type in
```bash
  process {YOUR_JIRA_TICKET_NUMBER}
```

---
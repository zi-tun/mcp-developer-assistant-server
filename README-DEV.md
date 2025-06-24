## 🚀 Build and Push a New Docker Image

If you want to build and push an updated MCP server image:

```bash
docker build -t mcp-dev-assist-server .
docker tag mcp-dev-assist-server containers.cisco.com/{YOUR_CECID}/mcp-dev-assist-server:{mon_dd_yyyy}
docker push containers.cisco.com/{YOUR_CECID}/mcp-dev-assist-server:{mon_dd_yyyy}
```

Replace `{mon_dd_yyyy}` with your version tag, e.g., `jun_23_2025`.

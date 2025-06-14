from server.server import mcp
from server.utils.prompt_builder import build_agentic_prompt
import mcp.types as types

@mcp.tool()
def agentic_prompting(ticket: dict) -> list:
    """Generate an agentic prompt based on the provided JIRA ticket."""
    prompt_md = build_agentic_prompt(ticket)
    return [types.TextContent(type="text", text=prompt_md)]
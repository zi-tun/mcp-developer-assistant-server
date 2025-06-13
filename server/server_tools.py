from server.server import mcp
from server.clients.jira_client import JiraClient
from server.utils.prompt_builder import build_agentic_prompt
import mcp.types as types

jira = JiraClient()

@mcp.tool()
def get_ticket(ticket_number: str) -> dict:
    ticket = jira.get_ticket(ticket_number)
    return {
        "key": ticket["key"],
        "summary": ticket["summary"],
        "description": ticket["description"],
        "labels": ticket.get("labels", [])
    }

@mcp.tool()
def agentic_prompting(ticket: dict) -> list:
    prompt_md = build_agentic_prompt(ticket)
    return [types.TextContent(type="text", text=prompt_md)]
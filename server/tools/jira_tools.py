from server.server import mcp
from server.clients.jira_client import JiraClient


jira = JiraClient()

@mcp.tool()
def get_ticket(ticket_number: str) -> dict:
    """Fetch a JIRA ticket detail by its number."""
    ticket = jira.get_ticket(ticket_number)
    return {
        "key": ticket["key"],
        "summary": ticket["summary"],
        "description": ticket["description"],
        "labels": ticket.get("labels", [])
    }
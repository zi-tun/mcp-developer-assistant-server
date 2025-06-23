from server.server import mcp
from server.clients.jira_client import JiraClient
from server.utils.prompt_builder import build_agentic_prompt
import mcp.types as types

jira = JiraClient()

@mcp.tool(
        name="process_jira_ticket_detail",
        description="""
        This tool fetches the JIRA ticket details and generates a markdown prompt
        that can be used for further processing or display in a user interface.
        Agent resecived the agentic prompt and interact with human in the loop approach.
        Args:
            ticket_number (str): The JIRA ticket number to fetch details for.
        Example:
            process_jira_ticket(ticket_number="DOD-4498")
        Returns:
            str: The rendered markdown prompt with placeholders replaced
            """)
def process_jira_ticket(ticket_number: str) -> dict:
    """Fetch a JIRA ticket detail by its number."""
    ticket = jira.get_ticket(ticket_number)
    prompt_md = build_agentic_prompt(ticket)
    return [types.TextContent(type="text", text=prompt_md)]

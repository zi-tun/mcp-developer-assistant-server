from fastmcp.server.dependencies import get_http_request
from starlette.requests import Request

from server.server import mcp
from server.clients.jira_client import JiraClient
from server.utils.prompt_builder import build_agentic_prompt
import mcp.types as types
import logging

jira = JiraClient()
logger = logging.getLogger(__name__)

def get_jira_credentails() -> tuple:
    # Get the HTTP request
    request: Request = get_http_request()
    jira_token = request.headers.get("jira_token", "")
    jira_username = request.headers.get("jira_username", "")


    # Access the client IP address 
    request: Request = get_http_request()
    client_ip = request.client.host if request.client else "Unknown"
    print("request....",request.json())

    return jira_token, jira_username

def build_error_msg() -> str:
    """Build an error message for missing fields."""
    # Get the HTTP request
    jira_token, jira_username = get_jira_credentails()

    missing_fields = []
    if not jira_token:
        missing_fields.append("jira_token")
    if not jira_username:
        missing_fields.append("jira_username")
    if missing_fields:
        error_msg = build_error_msg(", ".join(missing_fields))
    return (
        f"⚠️ **Missing required JIRA credentials.**\n\n"
        f"Please provide the missing headers: {','.join(missing_fields)}\n\n"
        "**Expected headers format: provided reference in .vscode/mcp.json**\n"
    )

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
    jira_token, jira_username = get_jira_credentails()
    if not jira_token or not jira_username:
        error_msg = build_error_msg()
        return [types.TextContent(type="text", text=error_msg)] 

    jira.set_credentials(jira_username, jira_token)
    ticket = jira.get_ticket(ticket_number)
    prompt_md = build_agentic_prompt(ticket)
    return [types.TextContent(type="text", text=prompt_md)]

import mcp.types as types
import logging
from fastmcp.server.dependencies import get_http_request
from fastmcp.server.dependencies import get_context
from starlette.requests import Request
from fastmcp import Context

from server.server import mcp
from server.clients.jira_client import JiraClient
from server.utils.prompt_builder import build_agentic_prompt

jira = JiraClient()
logger = logging.getLogger(__name__)


async def get_jira_credentials(request: Request) -> tuple[str, str]:
    """Fetch credentials from the request headers."""
    # Safely access headers
    jira_token = request.headers.get("jira_token", "").strip()
    jira_username = request.headers.get("jira_username", "").strip()

    return jira_token, jira_username


def build_error_msg(missing_fields: list[str]) -> str:
    """Builds a markdown error message for missing headers."""
    return (
        f"⚠️ **Missing required JIRA credentials.**\n\n"
        f"Please provide the following header(s): `{', '.join(missing_fields)}`\n\n"
        f"🔐 **Expected format** is set in `.vscode/mcp.json` headers.\n"
    )


@mcp.tool(
    name="process_jira_ticket_detail",
    description="""
    This tool fetches the JIRA ticket details and generates a markdown prompt
    that can be used for further processing or display in a user interface.
    Agent receives the agentic prompt and interacts with human-in-the-loop.

    Args:
        ticket_number (str): The JIRA ticket number to fetch details for.

    Example:
        process_jira_ticket(ticket_number="DOD-4498")

    Returns:
        str: Rendered markdown with JIRA ticket summary and guidance.
    """
)
async def process_jira_ticket(ticket_number: str, ctx: Context) -> list[types.TextContent]:
    request: Request = get_http_request()
    # TODO: logging user interaction end to end 
    # await ctx.info(f"Request client Details: {request.client}")
    # await ctx.info(f"Request headers Details: {request.headers}")
    try:
        jira_token, jira_username = await get_jira_credentials(request)

        missing = []
        if not jira_token:
            missing.append("jira_token")
        if not jira_username:
            missing.append("jira_username")

        if missing:
            error_msg = build_error_msg(missing)
            await ctx.error(f"ERROR: {error_msg}")
            return [types.TextContent(type="text", text=build_error_msg(missing))]

        jira.set_credentials(jira_username, jira_token)
        ticket = jira.get_ticket(ticket_number)
        prompt_md = build_agentic_prompt(ticket)

        return [types.TextContent(type="text", text=prompt_md)]
    except Exception as e:
        await ctx.error(f"Error processing JIRA ticket {ticket_number}: {repr(e)}")
        return [types.TextContent(type="text", text=f"Error: {repr(e)}")]
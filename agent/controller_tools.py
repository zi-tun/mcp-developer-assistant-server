from server.server import mcp

@mcp.tool()
async def handle_jira_ticket(ticket_id: str):
    await mcp.ui.show_message(f"Processing Ticket {ticket_id}")

    ticket = await mcp.call_tool("get_ticket", {"ticket_number": ticket_id})
    await mcp.ui.show_message(f"Loaded Jira ticket: {ticket['summary']}")

    result = await mcp.call_tool("agentic_prompting", {"ticket": ticket})
    await mcp.ui.show_message("Agentic prompting completed.")
    return result

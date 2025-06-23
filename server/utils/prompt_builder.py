import prompts as prompts
import importlib.resources as pkg_resources

def build_agentic_prompt(ticket):
    """
    Generate an agentic prompt based on the JIRA ticket details.
    
    Args:
        ticket: A dictionary containing JIRA ticket details with keys:
               'key', 'summary', 'description', and 'labels'
               
    Returns:
        str: The rendered markdown prompt with placeholders replaced
    """
    # Read the vscode agent template
    prompt_content = pkg_resources.read_text(prompts, "vscode_agent.md")
    
    # Replace all placeholders with actual values from the ticket
    rendered_md = prompt_content.replace("$ticketSummaryPlaceholder", ticket["summary"])
    rendered_md = rendered_md.replace("$branchNamePlaceholder", f"feature/{ticket['key']}")
    rendered_md = rendered_md.replace("$ticketDescriptionPlaceholder", ticket["description"] or "No description provided")
    rendered_md = rendered_md.replace("$jiraIdPlaceholder", ticket["key"])
    rendered_md = rendered_md.replace("$pullRequestCreationGuidePlaceholder", 
                                    "Create a PR using Github UI or the git command line. "
                                    "Include the ticket number in the PR title.")
    
    return rendered_md
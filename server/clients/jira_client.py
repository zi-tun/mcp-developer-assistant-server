from server.utils import credential_reader as reader
from jira import JIRA


class JiraClient:
    def __init__(self):
        config = reader.collect_property_file_contents('jira')
        self.base_url = config['url']

    def set_credentials(self, username, token):
        """Set the JIRA credentials."""
        self.username = username
        self.token = token
        self.jira = JIRA(server=self.base_url, basic_auth=(self.username, self.token))

    def get_ticket(self, ticket_number):
        issue = self.jira.issue(ticket_number)
        return {
            "key": issue.key,
            "summary": issue.fields.summary,
            "description": issue.fields.description,
            "labels": issue.fields.labels
        }
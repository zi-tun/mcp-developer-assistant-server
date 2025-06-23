import os
import requests
from server.utils import credential_reader as reader
from jira import JIRA


class JiraClient:
    def __init__(self):
        config = reader.collect_property_file_contents('jira')
        self.base_url = config['url']
        self.username = config['email']
        self.token = config['api_token']
        self.jira = JIRA(server=self.base_url, basic_auth=(self.username, self.token ))


    def get_ticket(self, ticket_number):
        issue = self.jira.issue(ticket_number)
        return {
            "key": issue.key,
            "summary": issue.fields.summary,
            "description": issue.fields.description,
            "labels": issue.fields.labels
        }

        # url = f"{self.base_url}/rest/api/3/issue/{ticket_number}"
        # auth = (self.username, self.token)
        # response = requests.get(url, auth=auth)
        # response.raise_for_status()
        # data = response.json()
        # return {
        #     "key": data["key"],
        #     "summary": data["fields"]["summary"],
        #     "description": data["fields"]["description"],
        #     "labels": data["fields"].get("labels", [])
        # }
        # return {'key': 'DOD-4498', 'summary': '[DD - DOD] Agentic MCP simple use case', 'description': 'learn about the AI tools and use case.', 'labels': []}

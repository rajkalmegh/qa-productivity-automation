import requests
import pandas as pd
import os
from requests.auth import HTTPBasicAuth
from urllib.parse import quote

ORG = os.getenv("DEVOPS_ORG")
PROJECT = quote(os.getenv("DEVOPS_PROJECT"))
PAT = os.getenv("DEVOPS_PAT")


def fetch_devops_data():

    wiql_url = f"https://dev.azure.com/{ORG}/{PROJECT}/_apis/wit/wiql?api-version=7.0"

    query = {
        "query": """
        SELECT [System.Id]
        FROM WorkItems
        WHERE
            [System.WorkItemType] = 'Bug'
            AND [System.State] NOT IN
                ('Rejected','Draft','Changes Required','Changes Done')
            AND [Custom.IssueSource] NOT IN
                ('CAT Audit','Employee Feedback')
            AND [System.CreatedDate] >= '2025-04-01'
            AND [System.CreatedDate] < @StartOfDay
        """
    }

    response = requests.post(
        wiql_url,
        json=query,
        auth=HTTPBasicAuth('', PAT)
    )

    data = response.json()

    ids = [item["id"] for item in data.get("workItems", [])]

    if not ids:
        raise Exception("No bugs returned from DevOps query")

    ids_string = ",".join(map(str, ids))

    details_url = f"https://dev.azure.com/{ORG}/_apis/wit/workitems?ids={ids_string}&api-version=7.0"

    work_items = requests.get(
        details_url,
        auth=HTTPBasicAuth('', PAT)
    ).json()

    bugs = []

    for item in work_items["value"]:
        fields = item["fields"]

        created_by = fields.get("System.CreatedBy", {})

        if isinstance(created_by, dict):
            name = created_by.get("displayName", "Unknown")
        else:
            name = str(created_by)

        bugs.append({
            "Name": name,
            "Severity": fields.get("Microsoft.VSTS.Common.Severity", "Normal"),
            "Product": fields.get("System.AreaPath", "Unknown")
        })

    df = pd.DataFrame(bugs)

    return df

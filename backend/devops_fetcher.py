import requests
import pandas as pd
import os
from requests.auth import HTTPBasicAuth

ORG = os.getenv("DEVOPS_ORG")
PROJECT = os.getenv("DEVOPS_PROJECT")
PAT = os.getenv("DEVOPS_PAT")


def fetch_devops_data():

    wiql_url = f"https://dev.azure.com/{ORG}/{PROJECT}/_apis/wit/wiql?api-version=7.0"

    query = {
        "query": "SELECT [System.Id] FROM WorkItems WHERE [System.WorkItemType] = 'Bug'"
    }

   response = requests.post(
    wiql_url,
    json=query,
    auth=HTTPBasicAuth('', PAT)
)

data = response.json()

print("DEVOPS RESPONSE:", data)

if "workItems" not in data:
    raise Exception(f"Azure DevOps API error: {data}")

ids = [item["id"] for item in data["workItems"]]

    ids = [item["id"] for item in response["workItems"]]

    ids_string = ",".join(map(str, ids))

    details_url = f"https://dev.azure.com/{ORG}/_apis/wit/workitems?ids={ids_string}&api-version=7.0"

    work_items = requests.get(
        details_url,
        auth=HTTPBasicAuth('', PAT)
    ).json()

    bugs = []

    for item in work_items["value"]:

        fields = item["fields"]

        bugs.append({
            "Name": fields.get("System.AssignedTo", {}).get("displayName", "Unknown"),
            "Severity": fields.get("Microsoft.VSTS.Common.Severity", "Normal"),
            "Product": fields.get("System.AreaPath", "Unknown")
        })

    df = pd.DataFrame(bugs)

    return df

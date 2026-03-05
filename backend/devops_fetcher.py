import requests
from requests.auth import HTTPBasicAuth

ORG = "your_org"
PROJECT = "your_project"
PAT = "your_devops_token"

WIQL_URL = f"https://dev.azure.com/{ORG}/{PROJECT}/_apis/wit/wiql?api-version=7.0"

query = {
    "query": "SELECT [System.Id] FROM WorkItems WHERE [System.WorkItemType] = 'Bug'"
}

response = requests.post(
    WIQL_URL,
    json=query,
    auth=HTTPBasicAuth('', PAT)
)

ids = [item['id'] for item in response.json()['workItems']]
print(ids)


IDS = ",".join(map(str, ids))

details_url = f"https://dev.azure.com/{ORG}/_apis/wit/workitems?ids={IDS}&api-version=7.0"

data = requests.get(details_url, auth=HTTPBasicAuth('', PAT)).json()

bugs = []

for item in data["value"]:
    bugs.append({
        "Name": item["fields"]["System.AssignedTo"]["displayName"],
        "Severity": item["fields"].get("Microsoft.VSTS.Common.Severity","Normal"),
        "Product": item["fields"]["System.AreaPath"]
    })

print(bugs)

import pandas as pd

df = pd.DataFrame(bugs)

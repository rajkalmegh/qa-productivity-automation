import requests
import pandas as pd
import os
from requests.auth import HTTPBasicAuth
from urllib.parse import quote

ORG = os.getenv("DEVOPS_ORG")
PROJECT = quote(os.getenv("DEVOPS_PROJECT"))
PAT = os.getenv("DEVOPS_PAT")

QUERY_ID = "a1c0e1c6-65ad-4fbb-b389-1a61d4eb4c9b"


def fetch_devops_data():

    url = f"https://dev.azure.com/{ORG}/{PROJECT}/_apis/wit/wiql/{QUERY_ID}?api-version=7.0"

    response = requests.get(
        url,
        auth=HTTPBasicAuth('', PAT)
    )

    if response.status_code != 200:
        raise Exception(f"DevOps API error: {response.text}")

    data = response.json()

    work_items = data.get("workItems", [])

    if not work_items:
        raise Exception("Saved query returned no bugs")

    ids = [item["id"] for item in work_items]

    ids_string = ",".join(map(str, ids))

    details_url = f"https://dev.azure.com/{ORG}/_apis/wit/workitems?ids={ids_string}&api-version=7.0"

    response = requests.get(
        details_url,
        auth=HTTPBasicAuth('', PAT)
    )

    work_items = response.json()
    print(response.text)
    

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

    return pd.DataFrame(bugs)

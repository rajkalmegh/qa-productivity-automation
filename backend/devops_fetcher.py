import requests
import pandas as pd
import os
from requests.auth import HTTPBasicAuth
from urllib.parse import quote

ORG = os.getenv("DEVOPS_ORG")
PROJECT = os.getenv("DEVOPS_PROJECT")

if PROJECT:
    PROJECT = quote(PROJECT)

PAT = os.getenv("DEVOPS_PAT")

QUERY_ID = "a1c0e1c6-65ad-4fbb-b389-1a61d4eb4c9b"


def fetch_devops_data():

    wiql_url = f"https://dev.azure.com/{ORG}/{PROJECT}/_apis/wit/wiql/{QUERY_ID}?api-version=7.0"

    response = requests.get(
        wiql_url,
        auth=HTTPBasicAuth('', PAT)
    )

    data = response.json()

    if "workItems" not in data:
        raise Exception(f"DevOps API error: {data}")

    ids = [item["id"] for item in data["workItems"]]

    if not ids:
        return pd.DataFrame()

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

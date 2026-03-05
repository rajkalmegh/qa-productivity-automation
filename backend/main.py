from fastapi import FastAPI
from backend.processor import process_data
from backend.report_generator import generate_report
from backend.devops_fetcher import fetch_devops_data
import time

app = FastAPI()


@app.get("/")
def home():
    return {"message": "QA Productivity Automation Running"}


@app.post("/generate-report")
def generate_report_api():

    start = time.time()

    # Fetch bugs directly from Azure DevOps
    df = fetch_devops_data()

    # Process productivity data
    tester_summary, severity_summary, product_summary = process_data(df)

    # Generate Excel report
    report_path = generate_report(
        tester_summary,
        severity_summary,
        product_summary
    )

    execution_time = round(time.time() - start, 2)

    return {
        "status": "success",
        "report": report_path,
        "execution_time_seconds": execution_time
    }

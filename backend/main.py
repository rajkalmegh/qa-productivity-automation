from fastapi import FastAPI
import time
from backend.devops_fetcher import fetch_devops_data
from backend.processor import process_data
from backend.report_generator import generate_report
from backend.pdf_generator import generate_pdf
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
def home():
    return {"message": "QA Productivity Automation Running"}

@app.post("/generate-report")
def generate_report_api():

    try:
        start = time.time()

        df = fetch_devops_data()

        tester_summary, severity_summary, product_summary = process_data(df)

        report_path = generate_pdf(
            tester_summary,
            severity_summary,
            product_summary
        )

        execution_time = round(time.time() - start, 2)

        print("Report generated in", execution_time, "seconds")

        return FileResponse(
            report_path,
            media_type="application/pdf",
            filename="daily_productivity_report.pdf"
        )

    except Exception as e:
        return {"error": str(e)}

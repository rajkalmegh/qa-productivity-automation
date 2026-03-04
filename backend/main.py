from fastapi import FastAPI, UploadFile, File
from backend.processor import process_data
from backend.report_generator import generate_report
import time

app = FastAPI()

@app.get("/")
def home():
    return {"message": "QA Productivity Automation Running"}

@app.post("/generate-report")
async def generate(file: UploadFile = File(...)):

    start = time.time()

    tester_summary, severity_summary, product_summary = process_data(file.file)

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

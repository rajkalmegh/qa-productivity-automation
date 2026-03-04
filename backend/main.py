from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from processor import process_data
from report_generator import generate_report
import time

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def dashboard():
    return FileResponse("frontend/index.html")


@app.post("/generate-report")
async def generate(file: UploadFile = File(...)):

    start = time.time()

    tester, severity, product = process_data(file.file)

    report = generate_report(tester, severity, product)

    execution_time = round(time.time() - start,2)

    return {
        "message":"Report Generated",
        "execution_time":execution_time,
        "report":report
    }

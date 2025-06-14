from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

class TaskRequest(BaseModel):
    task_id: str

def process_task(task_id: str):
    """Simple task processor"""
    logger.info(f"Processing task: {task_id}")
    # Simulate some work
    time.sleep(1)
    return f"Task {task_id} processed"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/start_task")
async def start_task(request: TaskRequest):
    try:
        logger.info(f"Received task request with ID: {request.task_id}")
        result = process_task(request.task_id)
        return {
            "status": "success",
            "task_id": request.task_id,
            "result": result
        }
    except Exception as e:
        logger.error(f"Error processing task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI
from pydantic import BaseModel
from tasks import long_task

app = FastAPI()

class TaskRequest(BaseModel):
    task_id: str

@app.post("/start_task")
def start_task(request: TaskRequest):
    long_task.delay(request.task_id)
    return {"status": "Task started", "task_id": request.task_id}
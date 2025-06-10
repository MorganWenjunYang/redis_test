from flask import Flask, request, jsonify
from tasks import long_task

app = Flask(__name__)

@app.route("/start_task", methods=["POST"])
def start_task():
    data = request.json or {}
    task_id = data.get("task_id", "default")
    long_task.delay(task_id)
    return jsonify({"status": "Task started", "task_id": task_id})

if __name__ == "__main__":
    app.run(debug=True)
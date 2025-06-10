from flask import Flask, request, jsonify, render_template_string
from tasks import long_task

app = Flask(__name__)

# HTML template with a button
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Task Trigger</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
        }
        #response {
            margin-top: 20px;
            padding: 10px;
            border-radius: 4px;
        }
        .success {
            background-color: #dff0d8;
            border: 1px solid #d6e9c6;
            color: #3c763d;
        }
        .error {
            background-color: #f2dede;
            border: 1px solid #ebccd1;
            color: #a94442;
        }
    </style>
</head>
<body>
    <h1>Task Trigger</h1>
    <button class="button" onclick="triggerTask()">Start Task</button>
    <div id="response"></div>

    <script>
        function triggerTask() {
            fetch('/start_task', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    task_id: new Date().getTime().toString()  // Use timestamp as task_id
                })
            })
            .then(response => response.json())
            .then(data => {
                const responseDiv = document.getElementById('response');
                responseDiv.className = 'success';
                responseDiv.innerHTML = `Task started successfully! Task ID: ${data.task_id}`;
            })
            .catch(error => {
                const responseDiv = document.getElementById('response');
                responseDiv.className = 'error';
                responseDiv.innerHTML = `Error: ${error.message}`;
            });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/start_task", methods=["POST"])
def start_task():
    data = request.json or {}
    task_id = data.get("task_id", "default")
    long_task.delay(task_id)
    return jsonify({"status": "Task started", "task_id": task_id})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
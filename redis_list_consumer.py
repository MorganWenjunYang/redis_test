import redis
import os
import json

r = redis.Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=6379,
    db=0
)

print("Consumer started. Waiting for tasks...")
while True:
    task = r.blpop('task_queue', timeout=0)
    if task:
        queue, data = task
        job = json.loads(data)
        print(f"Consumed: {job['task_id']} - {job['payload']}")
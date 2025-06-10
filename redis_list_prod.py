import redis
import os
import json
import time

r = redis.Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=6379,
    db=0
)

for i in range(5):
    data = {"task_id": f"task_{i}", "payload": f"payload_{i}"}
    r.rpush('task_queue', json.dumps(data))
    print("Produced:", data)
    time.sleep(1)
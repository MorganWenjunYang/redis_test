import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0)

print("Waiting for tasks in Redis stream...")
last_id = '0'
while True:
    # Fetch one new message
    messages = r.xread({'mystream': last_id}, block=0, count=1)
    if messages:
        _, entries = messages[0]
        for entry_id, data in entries:
            task_id = data[b'task_id'].decode()
            payload = data[b'payload'].decode()
            print(f"Got task from stream: {task_id} - {payload}")
            # Do some work
            time.sleep(2)
            print(f"Task {task_id} done")
            last_id = entry_id  # Advance stream position
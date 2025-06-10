import redis

r = redis.Redis(host='localhost', port=6379, db=0)

task_id = "stream_001"
payload = "Process with Redis Streams"

# Add an entry to the stream
r.xadd('mystream', {'task_id': task_id, 'payload': payload})
print(f"Task {task_id} pushed to Redis stream.")
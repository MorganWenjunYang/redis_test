import redis

r = redis.Redis(host='localhost', port=6379, db=0)
pubsub = r.pubsub()
pubsub.subscribe('task_notifications')

print("Subscribed to task_notifications. Waiting for messages...")
for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received notification: {message['data'].decode()}")
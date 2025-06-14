import os
from celery import Celery
import time
import redis

# Get Redis connection details from environment variables
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

# Set up Celery to use Redis as broker
celery_app = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/0')

# Connect to redis for pub/sub outside Celery
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

@celery_app.task
def long_task(task_id):
    print(f"Starting task {task_id}...")
    time.sleep(5)  # Simulate time-consuming work
    print(f"Task {task_id} done!")
    # Publish result to Redis channel
    redis_client.publish('task_notifications', f"Task {task_id} completed!")
    return f"Task {task_id} done"
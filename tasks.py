from celery import Celery
import time
import redis

# Set up Celery to use Redis as broker
celery_app = Celery('tasks', broker='redis://localhost:6379/0')

# Connect to redis for pub/sub outside Celery
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@celery_app.task
def long_task(task_id):
    print(f"Starting task {task_id}...")
    time.sleep(5)  # Simulate time-consuming work
    print(f"Task {task_id} done!")
    # Publish result to Redis channel
    redis_client.publish('task_notifications', f"Task {task_id} completed!")
    return f"Task {task_id} done"
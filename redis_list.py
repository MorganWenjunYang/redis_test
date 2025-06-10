import redis
import json
import threading
import time

r = redis.Redis(host='localhost', port=6379, db=0)

def producer():
    for i in range(3):
        task = {'task_id': f'list_{i}', 'payload': f'Payload {i}'}
        r.rpush('task_queue', json.dumps(task))
        print(f"Produced: {task}")
        time.sleep(1)  # simulate time between messages

def consumer():
    print("Consumer started. Waiting for tasks...")
    for _ in range(3):
        task = r.blpop('task_queue', timeout=0)
        if task:
            queue, data = task
            job = json.loads(data)
            print(f"Consumed: {job}")

if __name__ == "__main__":
    t_prod = threading.Thread(target=producer)
    t_cons = threading.Thread(target=consumer)
    t_cons.start()
    t_prod.start()
    t_prod.join()
    t_cons.join()
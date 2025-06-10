import redis
import threading
import time

r = redis.Redis(host='localhost', port=6379, db=0)

def producer():
    for i in range(3):
        task_id = f"stream_{i}"
        payload = f"Payload {i}"
        r.xadd('mystream', {'task_id': task_id, 'payload': payload})
        print(f"Produced: {task_id}")
        time.sleep(1)

def consumer():
    print("Consumer started. Waiting for tasks...")
    last_id = '0'
    for _ in range(3):
        messages = r.xread({'mystream': last_id}, block=0, count=1)
        if messages:
            _, entries = messages[0]
            for entry_id, data in entries:
                task_id = data[b'task_id'].decode()
                payload = data[b'payload'].decode()
                print(f"Consumed: {task_id} - {payload}")
                last_id = entry_id

if __name__ == "__main__":
    t_prod = threading.Thread(target=producer)
    t_cons = threading.Thread(target=consumer)
    t_cons.start()
    t_prod.start()
    t_prod.join()
    t_cons.join()
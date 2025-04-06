import requests
import time
import random
from datetime import datetime

header = {
    'authorization': 'auth'
}
url = 'url'

pesan_list = ["wh", "wb"]
index = 0
start_time = time.time()

count_wh = 0
count_wb = 0

def job():
    global index, count_wh, count_wb
    content = pesan_list[index]
    payload = {
        'content': content
    }
    r = requests.post(url, data=payload, headers=header)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] POST '{content}' - Status Code:", r.status_code)

    if content == "wh":
        count_wh += 1
    elif content == "wb":
        count_wb += 1

    index = (index + 1) % len(pesan_list)

while True:
    if time.time() - start_time > 900:
        print("billing 15 mnenit mu udah habis nder")
        print(f"\nTotal pesan terkirim:")
        print(f" - wh: {count_wh} kali")
        print(f" - wb: {count_wb} kali")
        break

    job()
    delay = random.randint(15, 25)
    time.sleep(delay)

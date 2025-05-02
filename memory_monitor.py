import psutil
import time
import json

def monitor_memory():
    while True:
        memory_data = {
            'total': psutil.virtual_memory().total,
            'used': psutil.virtual_memory().used,
            'free': psutil.virtual_memory().free,
            'swap_total': psutil.swap_memory().total,
            'swap_used': psutil.swap_memory().used
        }
        with open('reports/logs/memory_data.json', 'w') as f:
            json.dump(memory_data, f)
        time.sleep(1)
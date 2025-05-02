# app.py
from flask import Flask, render_template, jsonify
from threading import Thread
from memory_monitor import monitor_memory
import subprocess
import os
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data')
def get_data():
    file_path = os.path.join('reports', 'logs', 'memory_data.json')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    else:
        return jsonify({'error': 'Memory data not available'}), 404

def run_stress_test():
    subprocess.Popen(['python', 'stress_test.py'])

if __name__ == "__main__":
    Thread(target=monitor_memory, daemon=True).start()
    Thread(target=run_stress_test, daemon=True).start()
    app.run(debug=True)


# memory_monitor.py
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


# memory_manager.py
from simulator.paging import PagingSimulator
from simulator.segmentation import SegmentationSimulator

def run_paging_simulation(memory_size=1024, page_size=64, num_pages=16):
    paging_sim = PagingSimulator(memory_size, page_size, num_pages)
    for i in range(20):
        paging_sim.allocate_page(f"Process_{i}")

def run_segmentation_simulation(memory_size=1024):
    segment_sim = SegmentationSimulator(memory_size)
    for size in [100, 200, 150, 300, 50]:
        segment_sim.allocate_segment(size)


# simulator/paging.py
import random

class PagingSimulator:
    def __init__(self, memory_size, page_size, num_pages):
        self.memory_size = memory_size
        self.page_size = page_size
        self.num_pages = num_pages
        self.page_table = {}
        self.memory = [None] * memory_size

    def allocate_page(self, process_id):
        if len(self.page_table) >= self.num_pages:
            print("Page table is full. Performing replacement.")
            self.replace_page(process_id)
        else:
            page_number = len(self.page_table)
            frame_number = random.randint(0, self.memory_size - 1)
            self.page_table[process_id] = (page_number, frame_number)
            self.memory[frame_number] = process_id
            print(f"Allocated page {page_number} for Process {process_id} at Frame {frame_number}")

    def replace_page(self, process_id):
        victim = random.choice(list(self.page_table.keys()))
        frame_number = self.page_table[victim][1]
        del self.page_table[victim]
        self.memory[frame_number] = process_id
        print(f"Replaced Process {victim} with Process {process_id} at Frame {frame_number}")


# simulator/segmentation.py
class Segment:
    def __init__(self, base, limit):
        self.base = base
        self.limit = limit

class SegmentationSimulator:
    def __init__(self, memory_size):
        self.memory_size = memory_size
        self.segments = []

    def allocate_segment(self, size):
        if not self.segments:
            base = 0
        else:
            base = self.segments[-1].base + self.segments[-1].limit
        if base + size <= self.memory_size:
            segment = Segment(base, size)
            self.segments.append(segment)
            print(f"Allocated Segment - Base: {base}, Limit: {size}")
        else:
            print("Memory full. Cannot allocate segment.")


# visualizer.py
import matplotlib.pyplot as plt
import numpy as np
import json
import time

def plot_memory():
    plt.ion()
    fig, ax = plt.subplots()

    while True:
        try:
            with open('reports/logs/memory_data.json', 'r') as f:
                data = json.load(f)
            labels = ['Used', 'Free']
            values = [data['used'], data['free']]
            ax.clear()
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            plt.title('Real-Time Memory Usage')
            plt.draw()
            plt.pause(1)
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    plot_memory()
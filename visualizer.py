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

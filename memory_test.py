# Memory stress test to observe memory usage changes
import numpy as np
import time

print("Starting memory stress test...")
try:
    memory_blocks = []
    for _ in range(20):
        memory_blocks.append(np.random.rand(100, 100, 100))  # Allocate 80 MB each time
        print("Allocated memory")
        time.sleep(2)
except MemoryError:
    print("Memory allocation failed. Stopping.")

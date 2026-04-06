import time
import csv
import tracemalloc
from lightweight import lightweight_encrypt
from aes_compare import aes_encrypt

sizes = [100, 1000, 5000, 10000]
key = "iotkey123"
iterations = 100

results = []

for size in sizes:
    data = "Temperature=29.5;Humidity=60%" * (size // 30)

    # ------------------------
    # Lightweight Timing
    # ------------------------
    start = time.perf_counter()
    for _ in range(iterations):
        lightweight_encrypt(data, key)
    lw_time = (time.perf_counter() - start) / iterations

    # ------------------------
    # AES Timing
    # ------------------------
    start = time.perf_counter()
    for _ in range(iterations):
        aes_encrypt(data)
    aes_time = (time.perf_counter() - start) / iterations

    # ------------------------
    # Throughput Calculation
    # ------------------------
    lw_throughput = size / lw_time
    aes_throughput = size / aes_time

    # ------------------------
    # Memory Measurement
    # ------------------------
    tracemalloc.start()
    lightweight_encrypt(data, key)
    lw_memory = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    tracemalloc.start()
    aes_encrypt(data)
    aes_memory = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    # Save everything
    results.append([
        size,
        lw_time,
        aes_time,
        lw_throughput,
        aes_throughput,
        lw_memory,
        aes_memory
    ])

    # Print clean output
    print("\n=================================")
    print("Data Size:", size, "bytes")

    print("\nLightweight:")
    print("  Avg Time:", lw_time)
    print("  Throughput (bytes/sec):", lw_throughput)
    print("  Memory (bytes):", lw_memory)

    print("\nAES:")
    print("  Avg Time:", aes_time)
    print("  Throughput (bytes/sec):", aes_throughput)
    print("  Memory (bytes):", aes_memory)

# Save to CSV
with open("results.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "Data Size",
        "Lightweight Time",
        "AES Time",
        "Lightweight Throughput",
        "AES Throughput",
        "Lightweight Memory",
        "AES Memory"
    ])
    writer.writerows(results)

print("\nResults saved to results.csv")
import matplotlib.pyplot as plt
import csv
import os

# Base directory
base_dir = os.path.dirname(os.path.dirname(__file__))

# Input & output paths
input_path = os.path.join(base_dir, "results", "data", "c_vs_aes.csv")
output_path = os.path.join(base_dir, "results", "graphs", "c_vs_aes.png")

sizes = []
lightweight = []
aes = []

# Read CSV
with open(input_path, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        sizes.append(int(row["Data Size"]))
        lightweight.append(float(row["Lightweight Throughput"]))
        aes.append(float(row["AES Throughput"]))

# Plot
plt.figure()
plt.plot(sizes, lightweight, marker='o', label="Lightweight (C)")
plt.plot(sizes, aes, marker='o', label="AES (C)")

plt.xlabel("Data Size (bytes)")
plt.ylabel("Throughput (bytes/sec)")
plt.title("C Implementation: Lightweight vs AES")
plt.legend()
plt.grid(True)

# Save
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path)

plt.show()

print(f"Graph saved at: {output_path}")
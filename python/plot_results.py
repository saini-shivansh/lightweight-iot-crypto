import matplotlib.pyplot as plt
import csv
import os

# Get base directory (project root)
base_dir = os.path.dirname(os.path.dirname(__file__))

# Input CSV path
input_path = os.path.join(base_dir, "results", "data", "python_vs_aes.csv")

# Output image path
output_path = os.path.join(base_dir, "results", "graphs", "python_vs_aes.png")

sizes = []
lightweight_times = []
aes_times = []

# Read CSV
with open(input_path, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        sizes.append(int(row["Data Size"]))
        lightweight_times.append(float(row["Lightweight Time"]))
        aes_times.append(float(row["AES Time"]))

# Plot graph
plt.figure()
plt.plot(sizes, lightweight_times, marker='o', label="Lightweight")
plt.plot(sizes, aes_times, marker='o', label="AES")

plt.xlabel("Data Size (bytes)")
plt.ylabel("Average Time (seconds)")
plt.title("Python Prototype vs AES Performance")
plt.legend()
plt.grid(True)

# Save graph
plt.savefig(output_path)

# Show graph (optional)
plt.show()

print(f"Graph saved at: {output_path}")
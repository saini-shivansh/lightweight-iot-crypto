from lightweight import lightweight_encrypt
import math
from collections import Counter

key = "iotkey123"
data = "Temperature=29.5;Humidity=60%" * 100

cipher = lightweight_encrypt(data, key)

byte_counts = Counter(cipher)
total_bytes = len(cipher)

entropy = 0
for count in byte_counts.values():
    p = count / total_bytes
    entropy -= p * math.log2(p)

print("Entropy:", entropy)
print("Max possible entropy:", 8)
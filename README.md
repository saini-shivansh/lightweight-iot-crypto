# Lightweight SPN-Based Block Cipher for IoT

## Overview

This project implements a lightweight block cipher using a Substitution–Permutation Network (SPN), designed for resource-constrained IoT devices.

It includes:

* Python prototype for testing and analysis
* C implementation for performance benchmarking
* Comparison with AES
* Graph-based result visualization
* Arduino implementation for embedded testing

---

## Project Structure

```
c/        → C implementation and benchmarking  
python/   → Python prototype and plotting scripts  
arduino/  → Arduino implementation  
results/  → Data and generated graphs  
```

---

## How to Run

### C Benchmark

```
cd c
gcc main.c lightweight.c aes.c -o benchmark.exe
.\benchmark.exe
```

Generates:

```
results/data/c_vs_aes.csv
```

---

### Generate Graphs

```
python python/plot_results.py
python python/plot_c_results.py
```

Generates:

```
results/graphs/
```

---

## Arduino Implementation

Tested on Arduino Uno to evaluate performance in constrained environments.

File:

```
arduino/lightweight.ino
```

---

## Results

### Python (Prototype)

* Time-based comparison
* Slower due to interpreter overhead

### C Implementation

* Throughput-based comparison (bytes/sec)
* Lightweight cipher shows higher throughput than AES in software testing

---

## Key Observations

* ~2× higher throughput than AES (software evaluation)
* Stable performance across data sizes
* Suitable for constrained IoT environments

---

## Notes

* Block size: 64-bit
* Key size: 128-bit
* Experimental implementation (not production-ready)



import csv
import os
import statistics
import subprocess
import sys

LOADERS = [1, 2, 4]
WORKERS = [1, 2, 4, 8]    
QMAXES = [4, 32]
ULANG = 3            

if os.path.exists("hasil_b1.csv"):
    os.remove("hasil_b1.csv")

for qm in QMAXES:
    for lo in LOADERS:
        for wk in WORKERS:
            for _ in range(ULANG):
                subprocess.run([sys.executable, "hybrid_pipeline.py", "--loaders", str(lo),
                                "--workers", str(wk), "--qmax", str(qm)], check=True)

# ---- rangkum (median) ----
data = {}
with open("hasil_b1.csv") as f:
    for r in csv.DictReader(f):
        k = (int(r["qmax"]), int(r["loaders"]), int(r["workers"]))
        data.setdefault(k, []).append((float(r["total_s"]), float(r["throughput"]), float(r["avg_latency_ms"])))

with open("ringkasan_b1.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["qmax", "loaders", "workers", "total_s", "throughput", "avg_latency_ms"])
    for k in sorted(data):
        v = data[k]
        w.writerow([*k] + [round(statistics.median(x[i] for x in v), 3) for i in range(3)])
print("Ringkasan tersimpan di ringkasan_b1.csv")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
for ax, qm in zip(axes, QMAXES):
    for lo in LOADERS:
        ys = [statistics.median(x[1] for x in data[(qm, lo, wk)]) for wk in WORKERS]
        ax.plot(WORKERS, ys, marker="o", label=f"{lo} loader thread")
    ax.set_title(f"Q_MAX = {qm}")
    ax.set_xlabel("N_WORKERS")
    ax.set_xticks(WORKERS)
    ax.grid(alpha=0.3)
axes[0].set_ylabel("Throughput (file/detik)")
axes[0].legend()
plt.tight_layout()
plt.savefig("grafik_throughput.png", dpi=150)
print("Grafik tersimpan: grafik_throughput.png")

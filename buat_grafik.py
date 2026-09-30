import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

data = []
with open("ringkasan_b1.csv") as f:
    for r in csv.DictReader(f):
        data.append((int(r["qmax"]), int(r["loaders"]), int(r["workers"]), float(r["throughput"])))

QMAXES = sorted({d[0] for d in data})      # [4, 32]
LOADERS = sorted({d[1] for d in data})     # [1, 2, 4]
WORKERS = sorted({d[2] for d in data})     # [1, 2, 4, 8]


fig, axes = plt.subplots(1, len(QMAXES), figsize=(11, 4), sharey=True)
for ax, qm in zip(axes, QMAXES):
    for lo in LOADERS:
        ys = [t for (q, l, w, t) in sorted(data, key=lambda x: x[2]) if q == qm and l == lo]
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

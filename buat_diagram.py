import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(11, 7.6))
ax.set_xlim(0, 110); ax.set_ylim(0, 76); ax.axis("off")

def box(x, y, w, h, text, fc, ec="#333", fs=9, bold=False, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.2",
                                fc=fc, ec=ec, lw=1.3, ls=ls))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", wrap=True)

def arrow(x1, y1, x2, y2, label=None):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=14, lw=1.4, color="#222"))
    if label:
        ax.text((x1+x2)/2, (y1+y2)/2 + 1.3, label, ha="center", fontsize=8, style="italic")

# sumber & masuk
box(1, 55, 17, 14, "Aplikasi\ne-wallet\n(transaksi\nmasuk)", "#e8e8e8", bold=True)
box(24, 55, 19, 14, "Kafka\n(antrian event,\nbanyak partisi)", "#ffe0b2", bold=True)
arrow(18.5, 62, 23.5, 62)
ax.text(33.5, 71, "network-bound", ha="center", fontsize=8, color="#b35900", fontweight="bold")

# level 3 : inter-node
ax.add_patch(FancyBboxPatch((48, 3), 60, 70, boxstyle="round,pad=0.3,rounding_size=1.5",
                            fc="#e3f2fd", ec="#1565c0", lw=2))
ax.text(78, 70, "LEVEL 3 - INTER-NODE (cluster Spark Streaming)",
        ha="center", fontsize=8.5, fontweight="bold", color="#0d47a1")
arrow(43.5, 62, 48.5, 62, "partisi")

def node(x, nama):
    ax.add_patch(FancyBboxPatch((x, 8), 28, 58, boxstyle="round,pad=0.3,rounding_size=1.2",
                                fc="#e8f5e9", ec="#2e7d32", lw=1.8))
    ax.text(x+14, 64, nama, ha="center", fontsize=9, fontweight="bold", color="#1b5e20")
    ax.text(x+14, 59.8, "LEVEL 2 - INTRA-NODE\n(process pool, 1 process / core)", ha="center", fontsize=7.5, color="#1b5e20")
    # process boxes
    for i, px in enumerate([x+1.5, x+15]):
        ax.add_patch(FancyBboxPatch((px, 30), 11.5, 24, boxstyle="round,pad=0.2,rounding_size=1",
                                    fc="#fff9c4", ec="#f9a825", lw=1.3))
        ax.text(px+5.75, 52.8, f"Proses {i+1}\n(CPU-bound)", ha="center", fontsize=7.5, fontweight="bold")
        ax.text(px+5.75, 48.0, "hitung fitur\n+ skor model", ha="center", fontsize=7)
        ax.text(px+5.75, 44.5, "LEVEL 1\nTHREAD", ha="center", fontsize=7, color="#6a1b9a", fontweight="bold")
        for j in range(2):
            ax.add_patch(FancyBboxPatch((px+1+j*5.2, 32), 4.4, 9.5, boxstyle="round,pad=0.1,rounding_size=0.6",
                                        fc="#f3e5f5", ec="#6a1b9a", lw=1))
            ax.text(px+3.2+j*5.2, 36.7, "T", ha="center", fontsize=8, color="#6a1b9a")
    ax.text(x+14, 26.5, "Thread = ambil fitur dari Redis,\ntulis hasil ke DB (I/O-bound)", ha="center", fontsize=7, color="#6a1b9a")
    box(x+2, 10, 24, 12, "Feature store lokal\n(cache Redis)", "#fce4ec", ec="#c2185b", fs=8)

node(50.5, "NODE 1"); node(80, "NODE 2  ...  NODE N")

ax.text(79, 5, "Antar-node saling tukar data lewat jaringan (network-bound): agregasi, update model", ha="center", fontsize=7.5, style="italic")
# output
box(1, 28, 20, 12, "Keputusan:\nblokir / lolos\n(< 1 detik)", "#c8e6c9", ec="#2e7d32", bold=True)
box(1, 8, 20, 14, "Basis data +\ndashboard analis\n(I/O-bound)", "#ede7f6", ec="#4527a0")
arrow(50, 30, 21.5, 34, None)
arrow(50, 16, 21.5, 15, None)
ax.text(1, 45, "Level 1 = thread\nLevel 2 = intra-node (proses)\nLevel 3 = inter-node (cluster)", fontsize=8,
        bbox=dict(fc="white", ec="#888", boxstyle="round"))
plt.savefig("diagram_arsitektur.png", dpi=170, bbox_inches="tight")

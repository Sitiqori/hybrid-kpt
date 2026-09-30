import re
import subprocess

RANKS = [1, 2, 4]
WORKERS = [1, 2, 4]
ULANG = 3   

hasil = {}
for r in RANKS:
    for w in WORKERS:
        waktu = []
        for _ in range(ULANG):
            out = subprocess.run(["mpiexec", "-n", str(r), "python", "b2_mpi_processpool.py",
                                  "--workers", str(w)], capture_output=True, text=True).stdout
            m = re.search(r"makespan=([\d.]+)s", out)
            waktu.append(float(m.group(1)))
        hasil[(r, w)] = min(waktu)
        print(f"rank={r} worker={w} makespan={hasil[(r, w)]:.3f}s")

T1 = hasil[(1, 1)]
print("\nrank worker  n  makespan  speedup  efisiensi")
for (r, w), t in hasil.items():
    n = r * w
    S = T1 / t
    print(f"{r:>4} {w:>6} {n:>2} {t:>9.3f} {S:>8.2f} {S/n:>10.2%}")

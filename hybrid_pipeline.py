import argparse
import csv
import os
import queue
import re
import threading
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

DATA_DIR = "dataset_hybrid"
IO_DELAY = 0.005  
CPU_REPEAT = 3    
SENTINEL = None


def proses_teks(teks):
    """Dijalankan di PROCESS worker (CPU-bound)."""
    hitung = Counter()
    for _ in range(CPU_REPEAT):
        hitung = Counter(re.findall(r"\b\w+\b", teks.lower()))
    return len(hitung)


def loader(daftar_file, q, jumlah_loader, id_loader):
    """Dijalankan di THREAD. Ambil bagian file miliknya, lalu masukkan ke queue."""
    for path in daftar_file[id_loader::jumlah_loader]:
        with open(path, "r", encoding="utf-8") as f:
            teks = f.read()
        time.sleep(IO_DELAY)
        q.put((time.perf_counter(), teks))   


def dispatcher(q, pool, latensi, lock):
    """Thread penghubung: ambil dari queue, kirim ke process pool, catat latency."""
    while True:
        item = q.get()
        if item is SENTINEL:
            break
        waktu_masuk, teks = item
        pool.submit(proses_teks, teks).result()
        with lock:
            latensi.append(time.perf_counter() - waktu_masuk)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--loaders", type=int, default=2)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--qmax", type=int, default=32)
    ap.add_argument("--data", default=DATA_DIR)
    ap.add_argument("--csv", default="hasil_b1.csv")
    a = ap.parse_args()

    files = sorted(os.path.join(a.data, f) for f in os.listdir(a.data) if f.endswith(".txt"))
    q = queue.Queue(maxsize=a.qmax)
    latensi, lock = [], threading.Lock()

    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        list(pool.map(len, ["x"] * a.workers))

        t0 = time.perf_counter()
        loaders = [threading.Thread(target=loader, args=(files, q, a.loaders, i))
                   for i in range(a.loaders)]
        disp = [threading.Thread(target=dispatcher, args=(q, pool, latensi, lock))
                for _ in range(a.workers)]
        for t in loaders + disp:
            t.start()
        for t in loaders:
            t.join()
        for _ in disp:
            q.put(SENTINEL)
        for t in disp:
            t.join()
        total = time.perf_counter() - t0

    throughput = len(files) / total
    avg_lat = sum(latensi) / len(latensi)
    print(f"loaders={a.loaders} workers={a.workers} qmax={a.qmax} "
          f"| total={total:.2f}s throughput={throughput:.2f} file/s avg_latency={avg_lat*1000:.0f} ms")

    baru = not os.path.exists(a.csv)
    with open(a.csv, "a", newline="") as f:
        w = csv.writer(f)
        if baru:
            w.writerow(["loaders", "workers", "qmax", "total_s", "throughput", "avg_latency_ms"])
        w.writerow([a.loaders, a.workers, a.qmax, f"{total:.3f}", f"{throughput:.3f}", f"{avg_lat*1000:.1f}"])


if __name__ == "__main__":     
    main()

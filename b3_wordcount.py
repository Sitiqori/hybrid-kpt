import argparse
import glob
import os
import re
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

STOPWORDS = {"dan", "yang", "di", "the", "of", "and",      
             "to", "a", "in", "is", "it", "that", "was", "for", "with", "as", "he",
             "she", "his", "her", "i", "you", "but", "not", "be", "at", "on", "had",
             "have", "by", "this", "from", "or", "they", "we", "my", "me", "so"}


def hitung_file(path):
    """Satu tugas = baca file (I/O) + tokenisasi regex (CPU). Mengembalikan Counter."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        teks = f.read()                                
    kata = re.findall(r"[a-zA-Z']+", teks.lower())      
    return Counter(k for k in kata if k not in STOPWORDS)


def main():
    from mpi4py import MPI
    
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["thread", "process"], default="thread")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--data", default="teks_nyata")
    a = ap.parse_args()

    comm = MPI.COMM_WORLD
    rank, size = comm.Get_rank(), comm.Get_size()

    semua = sorted(glob.glob(os.path.join(a.data, "*.txt")))
    milik_saya = semua[rank::size]                      

    Executor = ThreadPoolExecutor if a.mode == "thread" else ProcessPoolExecutor
    with Executor(max_workers=a.workers) as ex:
        list(ex.map(len, ["x"] * a.workers))           
        comm.Barrier()
        t0 = MPI.Wtime()
        lokal = Counter()
        for c in ex.map(hitung_file, milik_saya):
            lokal.update(c)
        semua_counter = comm.gather(lokal, root=0)      
        comm.Barrier()
        waktu = MPI.Wtime() - t0

    if rank == 0:
        global_count = Counter()
        for c in semua_counter:
            global_count.update(c)
        print(f"\nMODE={a.mode} rank={size} workers={a.workers} "
              f"file={len(semua)} waktu={waktu:.3f}s")
        print("10 kata teratas (setelah stopwords dibuang):")
        for i, (kata, n) in enumerate(global_count.most_common(10), 1):
            print(f"{i:>2}. {kata:<12} {n}")


if __name__ == "__main__":
    main()

import argparse
import random
from concurrent.futures import ProcessPoolExecutor

SAMPLES_PER_TASK = 210_000
TOTAL_TASKS = 48   
def hitung_task(seed):
    rng = random.Random(seed)
    di_dalam = 0
    for _ in range(SAMPLES_PER_TASK):
        x, y = rng.random(), rng.random()
        if x * x + y * y <= 1.0:
            di_dalam += 1
    return di_dalam


def main():
    from mpi4py import MPI   

    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=1)
    a = ap.parse_args()

    comm = MPI.COMM_WORLD
    rank, size = comm.Get_rank(), comm.Get_size()

    tugas_saya = list(range(rank, TOTAL_TASKS, size))

    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        list(pool.map(abs, range(a.workers)))

        comm.Barrier()             
        t0 = MPI.Wtime()
        hasil_lokal = sum(pool.map(hitung_task, tugas_saya))
        total_dalam = comm.reduce(hasil_lokal, op=MPI.SUM, root=0)
        comm.Barrier()
        makespan = MPI.Wtime() - t0   

    if rank == 0:
        pi = 4.0 * total_dalam / (TOTAL_TASKS * SAMPLES_PER_TASK)
        print(f"HASIL ranks={size} workers={a.workers} makespan={makespan:.3f}s pi={pi:.5f}")


if __name__ == "__main__": 
    main()

Tugas Individu Hybrid Computing
Nama : Siti Qori'ah Muhafidloh
NIM  : 247006111141  (A = 1)

Urutan menjalankan (di terminal, folder ini):
 0. pip install mpi4py matplotlib        (MS-MPI harus sudah terpasang di Windows)
 1. python amdahl_a5.py                  -> hitungan A5
 2. python make_dataset.py               -> buat 110 file (B1)
    python run_semua_b1.py               -> 24 kombinasi B1 + grafik
 3. python run_semua_b2.py               -> 9 kombinasi B2 + speedup/efisiensi
    (atau manual: mpiexec -n 2 python b2_mpi_processpool.py --workers 4)
 4. python download_gutenberg.py         -> dataset B3 (>= 30 file)
    mpiexec -n 4 python b3_wordcount.py --mode thread  --workers 4
    mpiexec -n 4 python b3_wordcount.py --mode process --workers 4

Catatan: kalau kode asli dosen (slide 19 & 20) dipakai, ganti file yang sesuai
dan beri komentar pada bagian yang diubah.

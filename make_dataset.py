import os
import random

A = 1                
N_FILES = 100 + 10 * A     
OUT_DIR = "dataset_hybrid"
WORDS_PER_FILE = 60000  

kosakata = ("dan yang di ke dari untuk pada dengan adalah ini itu data "
            "komputer paralel proses thread memori jaringan cluster node "
            "program waktu hasil sistem the of and to in is for on").split()

os.makedirs(OUT_DIR, exist_ok=True)
random.seed(42)
for i in range(N_FILES):
    isi = " ".join(random.choice(kosakata) for _ in range(WORDS_PER_FILE))
    with open(os.path.join(OUT_DIR, f"file_{i:04d}.txt"), "w", encoding="utf-8") as f:
        f.write(isi)
print(f"Selesai: {N_FILES} file dibuat di folder '{OUT_DIR}'")

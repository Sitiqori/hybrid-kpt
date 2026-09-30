import os
import urllib.request

ID_BUKU = [1342, 11, 84, 1661, 2701, 98, 1232, 174, 345, 1400, 76, 74, 2591, 1952,
           5200, 46, 1260, 158, 161, 219, 2554, 2600, 1184, 135, 120, 16, 55, 35,
           36, 43, 829, 1497, 768, 514, 244, 215, 4300, 1399]
OUT = "teks_nyata"
os.makedirs(OUT, exist_ok=True)

ok = 0
for i in ID_BUKU:
    url = f"https://www.gutenberg.org/cache/epub/{i}/pg{i}.txt"
    try:
        teks = urllib.request.urlopen(url, timeout=30).read().decode("utf-8", errors="ignore")
        s = teks.find("*** START")
        e = teks.find("*** END")
        if s != -1 and e != -1:
            teks = teks[teks.find("\n", s):e]
        with open(os.path.join(OUT, f"buku_{i}.txt"), "w", encoding="utf-8") as f:
            f.write(teks)
        ok += 1
        print("OK  ", i)
    except Exception as err:
        print("GAGAL", i, err)
print(f"\nTotal berhasil: {ok} file (minimal harus 30)")

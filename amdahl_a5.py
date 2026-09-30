# NPM 247006111141 - A = 1 - bagian serial = 5 + A = 6% = 0.06
A = 1
f = (5 + A) / 100        

def speedup(n):
    return 1 / (f + (1 - f) / n)

for label, n in [("(a) 4 node x 8 core", 4 * 8), ("(b) 16 node x 8 core", 16 * 8)]:
    S = speedup(n)
    print(f"{label}: worker={n}  speedup={S:.2f}  efisiensi={S/n:.2%}")
print(f"Batas maksimum (n -> tak hingga): {1/f:.2f}")

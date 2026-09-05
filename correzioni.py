import numpy as np
import polars as pl
from collections import defaultdict

N_PERM = 5000
rng = np.random.default_rng(42)

archi = pl.read_parquet("processed/archi.parquet")
origini, destinazioni = [], []
for r in archi.iter_rows(named=True):
    origini += [r["origine"]] * r["peso"]
    destinazioni += [r["destinazione"]] * r["peso"]
origini = np.array(origini); destinazioni = np.array(destinazioni)

osservato = defaultdict(int)
for o, d in zip(origini, destinazioni):
    osservato[(o, d)] += 1

conta = defaultdict(int)
for _ in range(N_PERM):
    perm = rng.permutation(destinazioni)
    nullo = defaultdict(int)
    for o, d in zip(origini, perm):
        if o != d:
            nullo[(o, d)] += 1
    for c, oss in osservato.items():
        if nullo.get(c, 0) >= oss:
            conta[c] += 1

test = [(c, oss, (conta[c] + 1) / (N_PERM + 1))
        for c, oss in osservato.items() if oss >= 3]
test.sort(key=lambda x: x[2])
m = len(test)

# Benjamini-Hochberg
soglia = 0.01
k_max = 0
for i, (_, _, p) in enumerate(test, 1):
    if p <= i / m * soglia:
        k_max = i

print(f"test: {m}   significativi grezzi (p<{soglia}): "
      f"{sum(1 for _,_,p in test if p < soglia)}")
print(f"significativi dopo Benjamini-Hochberg: {k_max}\n")

for i, ((o, d), oss, p) in enumerate(test, 1):
    stato = "SI " if i <= k_max else "no "
    print(f"{stato} p={p:.4f}  bh={i/m*soglia:.4f}  peso={oss:3}   {o} -> {d}")

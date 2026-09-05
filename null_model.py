import numpy as np
import polars as pl
import networkx as nx
from collections import defaultdict

N_PERM = 5000
SEED = 42
rng = np.random.default_rng(SEED)

archi = pl.read_parquet("processed/archi.parquet")

# Sequenza di forward: ogni forward e' una coppia (origine, destinazione)
origini, destinazioni = [], []
for r in archi.iter_rows(named=True):
    origini += [r["origine"]] * r["peso"]
    destinazioni += [r["destinazione"]] * r["peso"]

origini = np.array(origini)
destinazioni = np.array(destinazioni)
M = len(origini)
print(f"forward totali: {M}")

osservato = defaultdict(int)
for o, d in zip(origini, destinazioni):
    osservato[(o, d)] += 1

# Permutazione: rimescola le destinazioni mantenendo
# le distribuzioni marginali di origine e destinazione
conta_maggiore = defaultdict(int)
for _ in range(N_PERM):
    perm = rng.permutation(destinazioni)
    nullo = defaultdict(int)
    for o, d in zip(origini, perm):
        if o != d:
            nullo[(o, d)] += 1
    for coppia, oss in osservato.items():
        if nullo.get(coppia, 0) >= oss:
            conta_maggiore[coppia] += 1

print(f"\n-- archi significativi (p < 0.01, peso >= 3) --")
ris = []
for coppia, oss in osservato.items():
    if oss < 3:
        continue
    p = (conta_maggiore[coppia] + 1) / (N_PERM + 1)
    ris.append((coppia, oss, p))

ris.sort(key=lambda x: x[2])
sig = [r for r in ris if r[2] < 0.01]
print(f"{len(sig)} su {len(ris)} archi testati\n")
for (o, d), oss, p in sig[:25]:
    print(f"p={p:.4f}  peso={oss:3}   {o} -> {d}")

print(f"\n-- archi NON significativi (p >= 0.05) --")
ns = [r for r in ris if r[2] >= 0.05]
for (o, d), oss, p in ns[:10]:
    print(f"p={p:.4f}  peso={oss:3}   {o} -> {d}")

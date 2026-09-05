import glob
from pathlib import Path
import polars as pl
import networkx as nx
import networkx.algorithms.community as nxcom

COPERTURA_MIN_GG = 60

msg = pl.read_parquet("processed/messaggi.parquet")
archi = pl.read_parquet("processed/archi.parquet")

cop = (msg.group_by("canale")
          .agg(pl.col("ts").min().alias("da"),
               pl.col("ts").max().alias("a"),
               pl.len().alias("n"))
          .with_columns(((pl.col("a") - pl.col("da")).dt.total_days()).alias("giorni")))

comparabili = set(cop.filter(pl.col("giorni") >= COPERTURA_MIN_GG)["canale"])
osservati = {Path(f).stem.lower() for f in glob.glob("raw/*.jsonl")}

print(f"osservati: {len(osservati)}  comparabili (>={COPERTURA_MIN_GG}gg): {len(comparabili)}")
print("esclusi:", sorted(osservati - comparabili))

G = nx.DiGraph()
for r in archi.iter_rows(named=True):
    G.add_edge(r["origine"], r["destinazione"], weight=r["peso"])
for n in G.nodes:
    G.nodes[n]["osservato"] = n in osservati
    G.nodes[n]["comparabile"] = n in comparabili

print("\n-- rapporto rilanciato/rilancia (solo comparabili) --")
rap = []
for n in G.nodes:
    if not G.nodes[n]["comparabile"]:
        continue
    o = G.out_degree(n, weight="weight")
    i = G.in_degree(n, weight="weight")
    if o + i >= 10:
        rap.append((n, o, i, o / max(i, 1)))
for n, o, i, r in sorted(rap, key=lambda x: -x[3]):
    print(f"{r:6.2f}  rilanciato:{o:4}  rilancia:{i:4}   {n}")

# Community detection su versione non diretta
U = G.to_undirected()
for u, v in U.edges:
    w = 0
    if G.has_edge(u, v): w += G[u][v]["weight"]
    if G.has_edge(v, u): w += G[v][u]["weight"]
    U[u][v]["weight"] = w

com = nxcom.louvain_communities(U, weight="weight", seed=42, resolution=1.0)
com = sorted(com, key=len, reverse=True)
mod = nxcom.modularity(U, com, weight="weight")

print(f"\n-- community (Louvain, seed=42) --")
print(f"numero: {len(com)}  modularita: {mod:.3f}")
for i, c in enumerate(com):
    oss = sum(1 for n in c if n in osservati)
    print(f"\ncommunity {i}  ({len(c)} nodi, {oss} osservati)")
    forza = sorted(c, key=lambda n: -(G.in_degree(n, weight='weight') + G.out_degree(n, weight='weight')))
    print("  " + ", ".join(forza[:10]))

for i, c in enumerate(com):
    for n in c:
        G.nodes[n]["community"] = i
nx.write_graphml(G, "output/grafo.graphml")

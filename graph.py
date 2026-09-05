import glob
from pathlib import Path
import polars as pl
import networkx as nx

archi = pl.read_parquet("processed/archi.parquet")
osservati = {Path(f).stem.lower() for f in glob.glob("raw/*.jsonl")}

# Arco: origine -> destinazione, dove destinazione e' il canale che rilancia.
# Quindi grado ENTRANTE = quanto un canale rilancia da altri
#       grado USCENTE  = quanto un canale viene rilanciato
G = nx.DiGraph()
for r in archi.iter_rows(named=True):
    G.add_edge(r["origine"], r["destinazione"], weight=r["peso"])

for n in G.nodes:
    G.nodes[n]["osservato"] = n in osservati

print(f"nodi: {G.number_of_nodes()}  archi: {G.number_of_edges()}")
print(f"osservati: {sum(1 for n in G if G.nodes[n]['osservato'])}")
print(f"densita: {nx.density(G):.4f}")
print(f"reciprocita: {nx.reciprocity(G):.3f}")

comp = sorted((len(c) for c in nx.weakly_connected_components(G)), reverse=True)
print(f"componenti deboli: {len(comp)}  dimensioni: {comp[:5]}")

print("\n-- quanto rilancia (grado entrante pesato, solo osservati) --")
inn = [(n, d) for n, d in G.in_degree(weight="weight") if G.nodes[n]["osservato"]]
for n, d in sorted(inn, key=lambda x: -x[1])[:12]:
    print(f"{d:5}   {n}")

print("\n-- quanto viene rilanciato (grado uscente pesato) --")
for n, d in sorted(G.out_degree(weight="weight"), key=lambda x: -x[1])[:12]:
    mark = "*" if G.nodes[n]["osservato"] else " "
    print(f"{d:5} {mark} {n}")

print("\n-- rapporto rilanciato/rilancia (solo osservati, min 10 archi) --")
rap = []
for n in G.nodes:
    if not G.nodes[n]["osservato"]:
        continue
    out = G.out_degree(n, weight="weight")
    inn_ = G.in_degree(n, weight="weight")
    if out + inn_ >= 10:
        rap.append((n, out, inn_, out / max(inn_, 1)))
for n, o, i, r in sorted(rap, key=lambda x: -x[3])[:15]:
    print(f"{r:6.2f}  rilanciato:{o:4}  rilancia:{i:4}   {n}")

print("\n-- archi reciproci --")
rec = [(u, v) for u, v in G.edges if G.has_edge(v, u) and u < v]
for u, v in rec:
    a, b = G[u][v]["weight"], G[v][u]["weight"]
    print(f"{u} <-> {v}  ({a}/{b})")

nx.write_graphml(G, "output/grafo.graphml")
print("\ngrafo salvato in output/grafo.graphml")

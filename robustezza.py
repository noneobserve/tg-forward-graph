import glob, json
from pathlib import Path
from collections import defaultdict
import numpy as np
import polars as pl
import networkx as nx
import networkx.algorithms.community as nxcom

FINESTRE = [30, 60, 90, 180, 365]
N_PERM = 2000

righe = []
for f in glob.glob("raw/*.jsonl"):
    canale = Path(f).stem.lower()
    for r in open(f):
        d = json.loads(r)
        righe.append({"canale": canale, "msg_id": d.get("msg_id"),
                      "data": d.get("data"),
                      "fwd_da": (d.get("fwd_da") or "").lower() or None})

df = (pl.DataFrame(righe)
        .with_columns(pl.col("data").str.to_datetime(
            format="%Y-%m-%dT%H:%M:%S%z", time_zone="UTC", strict=False).alias("ts"))
        .drop("data")
        .unique(subset=["canale", "msg_id"]))

tmax = df["ts"].max()
risultati = {}

for gg in FINESTRE:
    sub = df.filter(pl.col("ts") > tmax - pl.duration(days=gg))
    ar = (sub.filter(pl.col("fwd_da").is_not_null())
             .group_by(["fwd_da", "canale"]).agg(pl.len().alias("peso")))

    G = nx.Graph()
    for r in ar.iter_rows(named=True):
        w = G.get_edge_data(r["fwd_da"], r["canale"], {}).get("weight", 0)
        G.add_edge(r["fwd_da"], r["canale"], weight=w + r["peso"])

    mods, ncom = [], []
    for s in range(20):
        c = nxcom.louvain_communities(G, weight="weight", seed=s)
        mods.append(nxcom.modularity(G, c, weight="weight"))
        ncom.append(len(c))

    # significativita'
    o_, d_ = [], []
    for r in ar.iter_rows(named=True):
        o_ += [r["fwd_da"]] * r["peso"]
        d_ += [r["canale"]] * r["peso"]
    o_, d_ = np.array(o_), np.array(d_)
    oss = defaultdict(int)
    for a, b in zip(o_, d_): oss[(a, b)] += 1
    rng = np.random.default_rng(42)
    cnt = defaultdict(int)
    for _ in range(N_PERM):
        p = rng.permutation(d_)
        nu = defaultdict(int)
        for a, b in zip(o_, p):
            if a != b: nu[(a, b)] += 1
        for c, v in oss.items():
            if nu.get(c, 0) >= v: cnt[c] += 1
    testabili = [(c, v) for c, v in oss.items() if v >= 3]
    sig = {c for c, v in testabili if (cnt[c] + 1) / (N_PERM + 1) < 0.01}

    risultati[gg] = {"nodi": G.number_of_nodes(), "archi": G.number_of_edges(),
                     "fwd": len(o_), "mod": np.mean(mods),
                     "ncom": sorted(set(ncom)), "sig": sig,
                     "testati": len(testabili)}
    r = risultati[gg]
    print(f"{gg:4}gg  nodi:{r['nodi']:3} archi:{r['archi']:3} fwd:{r['fwd']:4}  "
          f"mod:{r['mod']:.3f}  ncom:{r['ncom']}  sig:{len(r['sig'])}/{r['testati']}")

base = risultati[90]["sig"]
print(f"\n-- stabilita' degli archi significativi (riferimento 90gg: {len(base)}) --")
for gg in FINESTRE:
    s = risultati[gg]["sig"]
    print(f"{gg:4}gg  in comune con 90gg: {len(base & s):3}/{len(base)}  "
          f"esclusivi: {len(s - base)}")

sempre = set.intersection(*[risultati[g]["sig"] for g in FINESTRE])
print(f"\narchi significativi in TUTTE le finestre: {len(sempre)}")
for o, d in sorted(sempre):
    print(f"  {o} -> {d}")

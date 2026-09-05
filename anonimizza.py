import json, glob
from pathlib import Path
import polars as pl

mappa = json.load(open("config/anon_map.json"))
def a(n): return mappa.get(n, n)

Path("writeup/data").mkdir(parents=True, exist_ok=True)

archi = pl.read_parquet("processed/archi.parquet")
archi = archi.with_columns(
    pl.col("origine").map_elements(a, return_dtype=pl.String),
    pl.col("destinazione").map_elements(a, return_dtype=pl.String),
).group_by(["origine", "destinazione"]).agg(
    pl.col("peso").sum(),
    pl.col("primo").min(),
    pl.col("ultimo").max(),
).sort("peso", descending=True)

archi.write_csv("writeup/data/edges_anon.csv")
print(f"archi: {len(archi)}")
print(f"anonimizzati: {len(mappa)} canali")
print(archi.head(12))

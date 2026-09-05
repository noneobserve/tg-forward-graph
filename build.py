import json, glob, hashlib
from pathlib import Path
import polars as pl
FINESTRA_GG = 90

righe = []
for f in glob.glob("raw/*.jsonl"):
    canale = Path(f).stem.lower()
    for r in open(f):
        d = json.loads(r)
        righe.append({
            "canale": canale,
            "msg_id": d.get("msg_id"),
            "data": d.get("data"),
            "testo": d.get("testo"),
            "fwd_da": (d.get("fwd_da") or "").lower() or None,
            "fwd_nome": d.get("fwd_nome"),
        })

df = pl.DataFrame(righe)

df = df.with_columns(
    pl.col("data").str.to_datetime(format="%Y-%m-%dT%H:%M:%S%z", time_zone="UTC", strict=False).alias("ts")
).drop("data")

df = df.filter(pl.col("ts") > pl.col("ts").max() - pl.duration(days=FINESTRA_GG))

df = df.unique(subset=["canale", "msg_id"], keep="first").sort(["canale", "msg_id"])

Path("processed").mkdir(exist_ok=True)
df.write_parquet("processed/messaggi.parquet")

archi = (
    df.filter(pl.col("fwd_da").is_not_null())
      .group_by(["fwd_da", "canale"])
      .agg(pl.len().alias("peso"),
           pl.col("ts").min().alias("primo"),
           pl.col("ts").max().alias("ultimo"))
      .rename({"fwd_da": "origine", "canale": "destinazione"})
      .sort("peso", descending=True)
)
archi.write_parquet("processed/archi.parquet")

print(f"messaggi unici: {len(df)}")
print(f"archi: {len(archi)}")
print(f"nodi: {len(set(archi['origine']) | set(archi['destinazione']))}")
print(f"intervallo: {df['ts'].min()} → {df['ts'].max()}")

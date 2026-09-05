import json, glob, collections
from pathlib import Path

archi = collections.Counter()
per_canale = collections.Counter()
msg_tot = fwd_tot = fwd_anon = 0

for f in glob.glob("raw/*.jsonl"):
    src = Path(f).stem
    for riga in open(f):
        d = json.loads(riga)
        msg_tot += 1
        if d.get("fwd_da"):
            d["fwd_da"] = d["fwd_da"].lower()
            fwd_tot += 1
            archi[(d["fwd_da"], src)] += 1
            per_canale[src] += 1
        elif d.get("fwd_nome"):
            fwd_anon += 1

dest = collections.Counter()
for (orig, _), n in archi.items():
    dest[orig] += n

seeds = {Path(f).stem for f in glob.glob("raw/*.jsonl")}
nuovi = [(n, c) for c, n in dest.most_common() if c not in seeds]

print(f"messaggi: {msg_tot}")
print(f"forward con origine: {fwd_tot} ({fwd_tot/msg_tot*100:.1f}%)")
print(f"forward senza origine: {fwd_anon}")
print(f"archi distinti: {len(archi)}")
print(f"canali origine distinti: {len(dest)}")

print("\n-- quanto rilancia ogni seed --")
for c, n in per_canale.most_common():
    print(f"{n:5} {c}")

print("\n-- candidati per il prossimo giro --")
for n, c in nuovi[:30]:
    print(f"{n:5} {c}")

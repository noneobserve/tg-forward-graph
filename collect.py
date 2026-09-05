import json, time, re, sys
from pathlib import Path
import requests
from bs4 import BeautifulSoup

BASE = "https://t.me/s/"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/128.0"}
PAUSA = 2.0

def parse(html):
    soup = BeautifulSoup(html, "lxml")
    out = []
    for m in soup.select("div.tgme_widget_message"):
        post = m.get("data-post", "")
        t = m.select_one("time[datetime]")
        testo = m.select_one("div.tgme_widget_message_text")
        fwd = m.select_one("a.tgme_widget_message_forwarded_from_name")
        out.append({
            "post": post,
            "msg_id": int(post.split("/")[-1]) if "/" in post else None,
            "data": t["datetime"] if t else None,
            "testo": testo.get_text(" ", strip=True) if testo else None,
            "fwd_da": fwd["href"].split("/")[-1].split("?")[0] if fwd and fwd.get("href") else None,
        })
    return out

def raccogli(canale, pagine=5):
    tutti, before = [], None
    for i in range(pagine):
        url = BASE + canale + (f"?before={before}" if before else "")
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code != 200:
            print(f"  {canale}: HTTP {r.status_code}")
            break
        msgs = parse(r.text)
        if not msgs:
            break
        tutti.extend(msgs)
        ids = [m["msg_id"] for m in msgs if m["msg_id"]]
        if not ids:
            break
        before = min(ids)
        time.sleep(PAUSA)
    return tutti

def main():
    seeds = Path("config/seeds.txt")
    canali = [l.strip() for l in seeds.read_text().splitlines()
              if l.strip() and not l.startswith("#")]
    Path("raw").mkdir(exist_ok=True)
    for c in canali:
        print(f"raccolgo {c}...")
        msgs = raccogli(c)
        with open(f"raw/{c}.jsonl", "w") as f:
            for m in msgs:
                f.write(json.dumps(m, ensure_ascii=False) + "\n")
        print(f"  {len(msgs)} messaggi, {sum(1 for m in msgs if m['fwd_da'])} forward")

main()

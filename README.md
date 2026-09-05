# tg-forward-graph

Collection and analysis pipeline for mapping forward relationships
between public Telegram channels.

Produces a directed weighted graph where nodes are channels and
edges represent observed message forwards, as a basis for
structural analysis of information ecosystems.

## Approach

The pipeline maps **structure, not identity**. It measures which
channels relay which, how often, and over what period. It does not
attribute content to individuals, and does not attempt to infer
intent or coordination from relay patterns.

## Data source

Public channel previews (`t.me/s/<channel>`), accessible without an
account or authentication. No channel subscription, no interaction,
no login required to reproduce the collection.

Requests are paginated backwards with a 2-second delay. Only
publicly accessible content is read.

## Requirements

```
python >= 3.10
requests beautifulsoup4 lxml polars
```

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Three stages, each reading from the previous. Raw data is never
modified in place; `processed/` is always regenerable.

**1. Collect** — reads `config/seeds.txt` (one channel handle per
line, no `@`), writes one JSONL file per channel to `raw/`.

```bash
python collect.py
```

**2. Inspect** — prints collection statistics and ranks channels
most frequently forwarded but not yet observed, for snowball
expansion.

```bash
python stats.py
```

**3. Build** — normalises, deduplicates, applies the time window,
writes Parquet to `processed/`.

```bash
python build.py
```

## Output

`processed/messaggi.parquet` — one row per message
`channel, msg_id, ts, testo, fwd_da, fwd_nome`

`processed/archi.parquet` — one row per directed edge
`origine, destinazione, peso, primo, ultimo`

`peso` is the forward count; `primo` and `ultimo` bound the
observed activity of that edge, allowing temporal filtering
downstream.

## Parameters

`FINESTRA_GG` in `build.py` sets the analysis window in days
(default 90). The window is anchored to the most recent message
in the dataset rather than to execution time, so results are
deterministic on a fixed input.

Vary this parameter to test how sensitive results are to the
window choice.

## Repository contents

Included: pipeline code, sampling methodology, aggregated edge
list (channel pairs with counts).

Not included: raw message archives, full message text, session
files, credentials. Message content is collected locally for
analysis but not redistributed.

## Methodology and limitations

See [`notes/campionamento.md`](notes/campionamento.md) (Italian)
for the full sampling procedure, expansion thresholds, stopping
criterion, and declared limitations.

Key limitations in brief:

- **Snowball bias.** The sample reflects what is connected to the
  initial seeds. Isolated clusters are invisible.
- **Observational asymmetry.** Seed channels are observed
  directly; other nodes appear only as forward destinations. Their
  outbound degree is unknown, not zero.
- **Bounded depth.** Five pages per channel. Effective coverage
  varies with posting frequency.

## Interpretation

Observed forwarding measures **relay**, not coordination, and
certainly not inauthenticity. Establishing that an observed
pattern differs from chance requires a null model, which is not
part of this repository.

## Licence

Code: MIT. Aggregated data: CC BY 4.0.

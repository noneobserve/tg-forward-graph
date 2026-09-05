# Forward structure in a Telegram channel cluster

A quantitative analysis of message relay patterns across a
connected cluster of public Italian political channels,
identified by snowball sampling from eight seed channels.

**Scope.** This work measures *structure*, not content, intent,
or identity. It asks which channels relay which, how often, and
whether observed relay volumes exceed what publishing volumes
alone would predict.

---

## Summary

Starting from 8 seed channels and expanding by snowball sampling,
we observed 35 public channels over a 90-day window
(2026-06-07 → 2026-09-05), collecting 2,278 unique messages and
412 forwards with identified origin.

The resulting directed graph has 84 nodes and 160 weighted edges.

Three findings:

1. **The ecosystem is a single connected component.** No isolated
   sub-networks. Reciprocity is 0.225 — roughly one edge in four
   is reciprocated.

2. **It partitions into five stable communities** (modularity
   0.635). The partition is invariant across 50 random seeds and
   across time windows from 30 to 365 days. Four communities are
   territorially organised; one groups publishing outlets with
   international rather than Italian references.

3. **26 of 39 testable edges exceed chance expectation**
   (permutation test, Benjamini-Hochberg corrected). Nine remain
   significant across every window tested.

---

## Why a null model matters

The clearest illustration comes from three edges of **identical
weight (3 forwards)**:

| edge | p |
|------|---|
| arktosmedia → dvxpubco | 0.0002 |
| progettorazzia → migliorcorsa | 0.056 |
| remigrazione_riconquista → barabittmilano | 0.151 |

The same number of forwards is remarkable, marginal, or
unremarkable depending on how active the channels involved are.
Without a reference distribution, all three would have been read
identically — and two of the three readings would have been wrong.

Conversely, `bloccostudentesconazionale → bloccostudentesconapoli`
carries **9 forwards** yet fails significance (p=0.033): both
channels are high-volume, and 9 falls within expectation.

Independently, community detection places that same channel with
the local Naples cluster rather than with its national structure.
Two methods with different assumptions converge.

---

## Method

**Source.** Public channel previews (`t.me/s/<channel>`), readable
without an account. No subscription, no interaction, no
authentication. Channels that disable public preview are not
observable by this method and are absent by construction.

**Seeds.** The eight initial channels are operated by Italian
nationalist and identitarian organisations and by publications
affiliated with that milieu. All are self-described: no political
classification is imposed by this analysis. The full seed list and
selection rationale are in the sampling note.

**Sampling.** Snowball expansion over three rounds, with
inclusion thresholds of 4, 2 and 10 forwards respectively.
Stopping criterion: no remaining candidate exceeded 10.

**Window.** 90 days, anchored to the most recent message in the
dataset rather than to execution time, keeping the filter
deterministic. Raw collection spanned 2021–2026, but page-depth
limits mean historical reach varies inversely with posting
frequency; without a window, edges from incomparable periods
would carry equal weight.

**Null model.** Forwards are expanded into (origin, destination)
pairs; destinations are permuted 5,000 times, preserving each
channel's total forwards sent and received while randomising
pairings. An edge's p-value is the fraction of null networks in
which that pair meets or exceeds the observed weight.

---

## Limitations

**Snowball bias.** The sample reflects what connects to the
initial seeds. Clusters neither relaying nor relayed by observed
channels are invisible.

**Observational asymmetry.** 35 channels are observed directly;
49 further nodes appear only as forward destinations. Their
outbound degree is unknown, not zero.

**Bounded depth.** Five preview pages per channel. Channels
observed for under 60 days are excluded from ratio metrics —
their inbound degree depends on their own short window while
outbound degree depends on everyone else's.

**Null model ignores time.** It preserves marginals but not
temporal profiles. Adequate for "is this link stronger than
expected", not for "are these channels temporally coordinated".

**Untested edges.** 121 of 160 edges carry fewer than 3 forwards
and were not tested.

---

## Interpretation

Forwarding measures **relay**. It does not measure coordination,
and it certainly does not measure inauthenticity. A statistically
significant edge means observed relay volume is not explained by
publishing volumes alone — nothing more. Ordinary explanations
(declared affiliation, thematic proximity, shared editorial
staff) are entirely consistent with these results.

No claim is made about individuals, intent, or organisational
relationships beyond what public relay behaviour shows.

---

## Data and reproducibility

`data/edges_anon.csv` — the full edge list.

Channels operated by identifiable individuals are labelled
`IND_nn`. **This is an editorial choice, not a technical
guarantee**: anyone re-running the documented method recovers the
original handles. It reduces incidental exposure; it does not
withhold evidence.

Code and full methodology notes (Italian): [repository root](../).

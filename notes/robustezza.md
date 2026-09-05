# Robustezza rispetto alla finestra temporale

Data: 2026-09-05
Script: `robustezza.py`

## Domanda

La finestra di 90 giorni è una scelta motivata ma arbitraria. Se
i risultati cambiassero sostanzialmente con finestre diverse,
descriverebbero la scelta anziché l'ecosistema.

Ricalcolo completo — grafo, community detection, modello nullo —
su 30, 60, 90, 180 e 365 giorni. Louvain con 20 seed per finestra,
2000 permutazioni per il modello nullo.

## Risultati

| finestra | nodi | archi | forward | modularità | n. community | significativi |
|----------|------|-------|---------|------------|--------------|---------------|
| 30gg | 63 | 89 | 210 | 0.592 | 5-6 | 9/20 |
| 60gg | 78 | 123 | 315 | 0.657 | 5-6 | 23/31 |
| **90gg** | **84** | **142** | **412** | **0.634** | **5** | **26/39** |
| 180gg | 91 | 161 | 512 | 0.632 | 6 | 33/46 |
| 365gg | 93 | 166 | 540 | 0.628 | 6 | 38/51 |

## Modularità: stabile

Varia tra 0.592 e 0.657 su un intervallo di finestre da 1 a 12
mesi, con 5 o 6 community sempre. La struttura in cluster non
dipende dalla finestra scelta.

## Archi significativi: annidati, non contraddittori

| finestra | in comune con 90gg | esclusivi |
|----------|--------------------|-----------|
| 30gg | 9/26 | 0 |
| 60gg | 21/26 | 2 |
| 180gg | 26/26 | 7 |
| 365gg | 26/26 | 12 |

Allargando la finestra si **aggiungono** archi significativi senza
mai perderne. Nessuna finestra contraddice un'altra.

Il calo a 30 giorni è perdita di potenza statistica, non
instabilità: con 210 forward molti archi scendono sotto il peso
minimo di 3 e non vengono nemmeno testati. Zero archi esclusivi
conferma che a 30 giorni non emerge nulla di incompatibile.

## Nucleo invariante

9 archi significativi in **tutte e cinque** le finestre:

- proitalia_org → IND_01
- casapoundnapoliufficiale → bloccostudentesconapoli
- IND_02 → casapoundnapoliufficiale
- squitiltopo → casapoundnapoliufficiale
- baronungernkhan → progettorazzia
- IND_03 → baronungernkhan
- progettorazzia → monferratononconforme
- lacagoule85 → monferratononconforme
- IND_04 → migliorcorsa

Questi non dipendono da alcuna scelta arbitraria di finestra.
Sono il risultato su cui affermazioni forti sono sostenibili.

Gli altri 17 significativi a 90 giorni vanno presentati come
condizionati alla finestra.

## Da verificare

`bloccostudentesconazionale → barabittmilano` (peso 21, p=0.0002
a 90gg) non compare tra gli invarianti: in almeno una finestra non
supera la soglia. Verificare in quale e perché — presumibilmente a
30gg per volume insufficiente.

## Conclusione

I risultati strutturali (numero e composizione delle community,
modularità) sono robusti. I risultati sui singoli archi sono
robusti per il nucleo di 9 e condizionati per i restanti.

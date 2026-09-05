# Campionamento — ecosistema Telegram

## Domanda
Mappare la struttura di rilancio (forward) tra canali Telegram
pubblici italofoni di un ecosistema politico, per identificarne
cluster, hub e direzione dei flussi.

## Unità di analisi
- Nodo = canale Telegram pubblico
- Arco diretto = forward da canale origine a canale destinazione
- Peso = numero di forward osservati nella finestra

## Fonte dei dati
Anteprima pubblica web (`t.me/s/<canale>`), accessibile senza
account né autenticazione. Paginazione a ritroso tramite parametro
`before`, 5 pagine per canale, pausa di 2 secondi tra richieste.

Nessuna iscrizione ai canali, nessuna interazione. Solo lettura di
contenuti pubblicamente accessibili.

## Strategia: snowball sampling
Espansione iterativa a partire da seed noti, aggiungendo a ogni giro
i canali più frequentemente rilanciati non ancora osservati.

### Seed iniziali (8)
casapoundufficiale, ecodelnord, bloccostudentesconazionale,
barabittmilano, arcadiapirata, progettorazzia, terracava2, IND_01

Criterio: canali di organizzazioni e figure pubbliche riconoscibili
dell'area, identificati da conoscenza pregressa del dominio.
Verificati con HTTP 200 su `t.me/s/`.

### Giri di espansione
| Giro | Soglia | Aggiunti | Motivazione soglia |
|------|--------|----------|--------------------|
| 1 | ≥4 forward | 7 | delimitare il nucleo denso |
| 2 | ≥2 forward | 18 | catturare la periferia |
| 3 | ≥10 forward | 3 | includere solo hub residui |

La soglia è stata variata deliberatamente per fase. Non è un
criterio unico applicato in modo incoerente: 4 per isolare il
nucleo, 2 per estendere alla periferia, 10 per fermarsi senza
troncare nodi ad alto grado entrante.

### Criterio di arresto
Al termine del terzo giro nessun candidato superava la soglia di
10 forward (massimo osservato: 7). Raccolta chiusa.

## Finestra temporale
**90 giorni**, ancorati al timestamp del messaggio più recente del
dataset (non alla data di esecuzione), per rendere il filtro
deterministico e riproducibile.

Motivazione: la profondità storica delle 5 pagine varia
enormemente per canale in funzione della frequenza di
pubblicazione. Il dataset grezzo copriva 2021-03-02 → 2026-09-05,
ma un canale poco attivo contribuiva 10 messaggi su 5 anni mentre
uno attivo ne contribuiva 90 su 5 giorni. Senza taglio, archi
riferiti a periodi incomparabili avrebbero avuto lo stesso peso.

Confronto tra finestre (canali osservati sempre 35):
- 30gg: 1638 msg, 210 forward
- 60gg: 1995 msg, 315 forward
- **90gg: 2278 msg, 412 forward**
- 180gg: 2565 msg, 512 forward
- 365gg: 2629 msg, 540 forward

90 giorni conserva il 71% dei forward mantenendo una finestra
realmente coperta da tutti i canali.

## Campione finale
- 35 canali osservati (sorgenti)
- 2278 messaggi unici
- 160 archi diretti
- 84 nodi totali (osservati + solo destinazione)
- Intervallo: 2026-06-07 → 2026-09-05

## Limiti dichiarati

**Bias di snowball.** Il campione riflette ciò che è connesso ai
seed iniziali. Cluster isolati che non rilanciano né sono
rilanciati dai canali osservati restano invisibili. La mappa
dipende dai semi.

**Asimmetria osservativa.** I 35 canali seed sono osservati
integralmente; gli altri 49 nodi compaiono solo come destinazioni
di forward. Il loro grado uscente è ignoto, non nullo.

**Profondità limitata.** 5 pagine per canale. Per i canali molto
attivi la finestra effettiva è inferiore ai 90 giorni nominali.

**Forward senza origine.** 8 messaggi presentano attribuzione di
forward senza link identificabile (canale privato o inoltro
disabilitato). Esclusi dagli archi, conteggiati separatamente.

**Contenuto non analizzato.** Questa fase mappa solo la struttura
di rilancio. Nessuna analisi semantica, nessuna attribuzione a
persone fisiche.

## Nota
Coordinamento ≠ inautenticità. Gli archi misurano rilanci
osservabili, non intenzionalità né coordinazione organizzata.
Nessuna conclusione su queste dimensioni è supportata dai dati
raccolti in questa fase.

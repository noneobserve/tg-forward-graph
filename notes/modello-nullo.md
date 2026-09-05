# Modello nullo — significatività degli archi

Data: 2026-09-05
Input: `processed/archi.parquet` (finestra 90gg)
Script: `null_model.py`

## Domanda

La modularità elevata (0.635) dimostra che il grafo ha struttura,
non che i singoli archi siano significativi. Un arco di peso 9 tra
due canali molto attivi può essere del tutto ordinario; lo stesso
peso tra due canali poco attivi no.

Serve una distribuzione di riferimento: quanti forward ci si
aspetterebbe tra due canali dati i rispettivi volumi complessivi.

## Metodo

I 412 forward della finestra sono espansi in una sequenza di
coppie (origine, destinazione). Le destinazioni vengono
rimescolate casualmente, generando reti nulle che **conservano i
marginali** — ogni canale mantiene il numero totale di forward
effettuati e ricevuti — ma **randomizzano le coppie**. Gli
auto-loop generati dalla permutazione sono scartati.

Il p-value di un arco è la frazione di reti nulle in cui quella
coppia raggiunge o supera il peso osservato.

Parametri:
- permutazioni: 5000
- seed: 42
- archi testati: solo peso ≥ 3 (39 archi su 160)

## Risultato

**27 archi su 39 significativi a p < 0.01.**

Più forti (p = 0.0002, cioè mai superati in 5000 permutazioni):

| peso | arco |
|------|------|
| 49 | proitalia_org → matbrandi |
| 21 | bloccostudentesconazionale → barabittmilano |
| 15 | casapoundnapoliufficiale → bloccostudentesconapoli |
| 10 | arcadiapirata → barabittmilano |
| 10 | bloccostudentesconazionale → bloccostudentescoavellino |
| 10 | fratotolo → casapoundnapoliufficiale |

## Il risultato più istruttivo

Tre archi di **peso identico (3)** con esiti opposti:

- `arktosmedia → dvxpubco` — p = 0.0002 → significativo
- `progettorazzia → migliorcorsa` — p = 0.056 → non significativo
- `remigrazione_riconquista → barabittmilano` — p = 0.151 → caso

Lo stesso numero di forward è o non è notevole a seconda
dell'attività dei canali coinvolti. Senza modello nullo i tre
archi sarebbero stati trattati allo stesso modo, con conclusioni
errate in due casi su tre.

Questo esempio va usato nel write-up per spiegare il metodo.

## Verifica dell'ipotesi precedente

L'ipotesi della struttura federata (annotata in
`analisi-rete.md`) regge: gli archi da
`bloccostudentesconazionale` verso le sedi locali sono tutti
significativi — barabittmilano 21, avellino 10, sardegna 8,
fvg 8, tutti p ≤ 0.0004.

## Limiti

**Risoluzione del p-value.** Con 5000 permutazioni il minimo
osservabile è 1/5001 = 0.0002. Molti archi hanno esattamente
questo valore, che significa "mai superato", non un p misurato
con precisione. Nel write-up riportare `p < 0.001`, non il valore
puntuale.

**Test multipli.** 39 test simultanei: a soglia 0.05 ci si
aspetterebbero ~2 falsi positivi. Da applicare correzione
Benjamini-Hochberg prima della pubblicazione.

**Il modello ignora il tempo.** Conserva i marginali ma non la
distribuzione temporale dei messaggi. Non tiene conto del fatto
che un canale possa essere stato attivo solo in parte della
finestra. È un nullo di primo livello: adeguato a "questo legame
è più forte del previsto", non a "questi canali sono coordinati
nel tempo".

**Archi di peso < 3 non testati.** 121 archi su 160 restano senza
valutazione di significatività.

## Prossimi passi

1. Correzione per test multipli (Benjamini-Hochberg)
2. Modello nullo che conservi anche i profili temporali
3. Ricalcolo a 30/60/180 giorni per la robustezza rispetto alla
   finestra

## Interpretazione

Un arco significativo indica che il volume di rilancio osservato
non è spiegato dai soli volumi di pubblicazione. **Non** indica
coordinamento, accordo o inautenticità: indica una relazione di
rilancio preferenziale, che può avere cause banali (affiliazione
dichiarata, prossimità tematica, sovrapposizione di redazione).

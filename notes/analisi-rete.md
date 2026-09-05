# Analisi di rete — primo passaggio

Data: 2026-09-05
Input: `processed/archi.parquet` (finestra 90gg, 160 archi, 84 nodi)
Script: `graph.py`, `graph2.py`

## Struttura del grafo

Grafo diretto pesato. Arco origine → destinazione, dove la
destinazione è il canale che effettua il rilancio.

Conseguenza sulla lettura dei gradi:
- grado **entrante** pesato = quanto un canale rilancia da altri
- grado **uscente** pesato = quanto un canale viene rilanciato

(Nel primo passaggio le due etichette erano invertite nello
script. Corretto verificando contro i conteggi indipendenti di
`stats.py`.)

## Metriche di base

- nodi: 84 (35 osservati, 49 solo come destinazione)
- archi: 160
- densità: 0.0229
- reciprocità: 0.225
- componenti deboli: 1 (contiene tutti gli 84 nodi)

L'ecosistema è un blocco unico: nessuna isola separata. Una
reciprocità di 0.225 indica che circa un arco su quattro è
ricambiato — scambio orizzontale, non sola diffusione
gerarchica.

## Errore metodologico rilevato e corretto

Il rapporto rilanciato/rilancia calcolato su tutti i canali
osservati produceva un ranking dominato da `matt1news` (25.0),
`IND_02` (15.0) e `futuronazionaleofficial` (9.0), apparenti
"produttori puri" con grado entrante nullo o quasi.

Verifica delle date di prima osservazione: quei tre canali sono
i più recenti del campione (dal 27-31 agosto, quindi 5-9 giorni
di copertura effettiva contro i 90 nominali).

**Causa.** Il grado uscente di un nodo dipende dalla finestra di
osservazione di *tutti gli altri* canali; il grado entrante
dipende solo dalla *propria*. Un canale osservato per pochi
giorni ha necessariamente grado entrante basso, e il rapporto
risulta strutturalmente gonfiato.

**Correzione.** Introdotto `COPERTURA_MIN_GG = 60`: il rapporto
viene calcolato solo sui canali con almeno 60 giorni di
copertura effettiva. 18 canali su 36 osservati passano il
filtro. Gli esclusi restano nel grafo come nodi, ma non entrano
nelle metriche che confrontano grado entrante e uscente.

## Ruoli osservati (solo canali comparabili)

Produttori (rapporto alto, molto rilanciati e poco rilancianti):
- arcadiapirata 5.00
- remigrazione_riconquista 4.67
- bloccostudentesconazionale 3.50 (56 rilanciato / 16 rilancia)

Amplificatori (rapporto basso, rilanciano molto più di quanto
vengano rilanciati):
- bloccostudentesconapoli 0.03 (1 / 35)
- barabittmilano 0.07 (3 / 41)
- bloccostudentescofvg 0.13 (2 / 15)
- bloccostudentescoavellino 0.15 (3 / 20)

## Community detection

Algoritmo: Louvain su versione non diretta, pesi sommati nelle
due direzioni.

- community: 5
- modularità: 0.635

### Test di stabilità

50 esecuzioni con seed 0-49:
- numero di community: **5 in tutte e 50 le esecuzioni**
- modularità media: 0.634
- coppie di nodi che restano insieme in ≥90% delle esecuzioni:
  788 su 834 (94.5%)

La partizione è una proprietà del grafo, non dell'algoritmo.

### Composizione

| # | nodi | osservati | caratterizzazione |
|---|------|-----------|-------------------|
| 0 | 30 | 11 | progettorazzia, baronungernkhan, migliorcorsa, matt1news |
| 1 | 18 | 9 | bloccostudentesco nazionale/avellino/fvg, barabittmilano |
| 2 | 17 | 8 | casapoundnapoliufficiale, bloccostudentesconapoli, uroborocava |
| 3 | 13 | 4 | arktosmedia, dvxpubco, lanceslegion, imperiumpressofficial |
| 4 | 6 | 3 | proitalia_org, IND_01, canalefahrenheit912 |

## Osservazioni da verificare (NON conclusioni)

**1. Prevalenza territoriale su organizzativa.** I canali
`bloccostudentesco*` non si raggruppano tutti insieme: nazionale,
avellino e fvg stanno nella community 1, napoli nella 2 insieme
all'ambiente napoletano locale. L'algoritmo suggerisce che per
quel nodo il legame geografico prevalga su quello organizzativo.
Da verificare ispezionando gli archi effettivi, non la partizione.

**2. Cluster transnazionale.** La community 3 raggruppa nodi con
profilo editoriale e riferimenti internazionali, distinta dalle
altre quattro a base territoriale italiana. È l'unico
raggruppamento non anticipabile dai dati grezzi.

**3. Asimmetria produttore/distributore.** L'arco
`IND_01 ↔ proitalia_org` ha pesi 2/49: fortemente asimmetrico.
Contrapposto a scambi equilibrati come
`baronungernkhan ↔ ilblast_it` (1/1).

## Cosa manca

**Modello nullo.** La modularità alta dimostra che il grafo ha
struttura, non che i singoli archi siano significativi. Senza una
distribuzione di riferimento — quanti forward ci si aspetterebbe
tra due canali dati i rispettivi volumi di pubblicazione e la
finestra osservata — nessuna affermazione su singole coppie è
supportata.

Metodo previsto: permutazione dei timestamp e shuffle delle
etichette, confronto della distribuzione osservata con quella
attesa.

**Robustezza rispetto alla finestra.** Le metriche vanno
ricalcolate a 30, 60 e 180 giorni per verificare quanto i
risultati dipendano dalla scelta dei 90 giorni.

## Limite di interpretazione

Il rilancio misura relay, non coordinamento e tantomeno
inautenticità. Nessuna affermazione su intenzionalità,
organizzazione o natura degli account è supportata da questi
dati.

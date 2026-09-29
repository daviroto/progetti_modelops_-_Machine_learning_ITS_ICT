# Lab 01 - Soluzione adattata al docente

## Dataset e limiti

Il codice segue lo schema `f1,f2,label`, il classificatore a soglia media su `f1` e lo split/shuffle 75/25 proposti dal docente. L'allegato include solo tre righe d'esempio, non il dataset completo necessario a riprodurre le accuracy 0.82 e 0.90. Il `data.csv` incluso è quindi una fixture sintetica locale compatibile, non il dataset originale; i risultati qui sotto sono quelli misurati sulla fixture.

## Comandi PowerShell

Eseguire dalla cartella del progetto. Serve Python 3.14; non sono richiesti pacchetti esterni.

```powershell
py -3.14 --version
py -3.14 train.py --data data.csv --out model_a.pkl --seed 42
py -3.14 train.py --data data.csv --out model_b.pkl --seed 7
py -3.14 gate.py
```

Output verificato:

```text
run: seed=42 accuracy=0.8333 model=model_a.pkl
run: seed=7 accuracy=0.6667 model=model_b.pkl
gate: model_b.pkl vs baseline model_a.pkl -> BLOCCATA
```

Il gate restituisce exit code 1 se blocca il candidato, così una CI può fermare la promozione. `train.py` salva soglia, seed e accuracy nel pickle; `gate.py` legge i due artefatti e applica `accuracy_candidata >= accuracy_baseline`, verificando anche che entrambi i file esistano.

## Run log

| Run | Dataset | Parametri | Accuracy | Artefatto |
| --- | --- | --- | ---: | --- |
| A (baseline) | `data.csv`, fixture locale di 24 righe | seed=42, split 75/25 | 0.8333 | `model_a.pkl` |
| B (candidato) | `data.csv`, fixture locale di 24 righe | seed=7, split 75/25 | 0.6667 | `model_b.pkl` |

Esito: B viene bloccata perché `0.6667 < 0.8333`; durante il test entrambi i pickle erano presenti.

## Verifiche effettuate

- I due comandi di training sono terminati con exit code 0 e hanno prodotto i pickle con accuracy nei metadati.
- `py -3.14 gate.py` ha stampato `BLOCCATA` e restituito exit code 1, atteso per un candidato peggiore.
- Il ramo positivo della funzione gate, con candidato migliore e artefatto presente, ha restituito `True`.
- Senza il file candidato, `gate.py` ha stampato `BLOCCATA (artefatto assente)` e restituito exit code 1.
- Il CSV con colonne errate viene rifiutato da `train.py` con un messaggio esplicito.

Con le sole tre righe mostrate nell'allegato, il test set contiene una riga: l'accuracy può essere 0 o 1, non 0.82 o 0.90. Per riprodurre esattamente quei numeri serve il CSV completo del docente.

## Cleanup

I modelli sono artefatti temporanei; `data.csv` resta come fixture condivisa del progetto.

```powershell
Remove-Item model_a.pkl, model_b.pkl -Force
```

Cleanup eseguito: pickle e cache Python dei test rimossi. `data.csv` è mantenuto come dataset del deliverable; non restano processi o kernel Python attivi.
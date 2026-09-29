import argparse
import csv
import pickle
import random
from pathlib import Path


def load_dataset(path):
    dataset_path = Path(path)
    if not dataset_path.is_file():
        raise FileNotFoundError(
            f"Dataset non trovato: {path}. Serve un CSV con colonne f1,f2,label."
        )

    with dataset_path.open(newline="", encoding="utf-8") as data_file:
        reader = csv.DictReader(data_file)
        expected_columns = {"f1", "f2", "label"}
        if not reader.fieldnames or not expected_columns.issubset(reader.fieldnames):
            raise ValueError("CSV non valido: servono le colonne f1,f2,label.")

        rows = [
            (float(row["f1"]), float(row["f2"]), int(row["label"]))
            for row in reader
        ]

    if len(rows) < 2:
        raise ValueError("CSV insufficiente: servono almeno due righe di dati.")
    if any(label not in (0, 1) for _, _, label in rows):
        raise ValueError("La colonna label deve contenere solo 0 o 1.")
    return rows


def train(data, seed):
    shuffled = data[:]
    random.Random(seed).shuffle(shuffled)
    split = int(len(shuffled) * 0.75)
    train_rows, test_rows = shuffled[:split], shuffled[split:]

    if not train_rows or not test_rows:
        raise ValueError("Lo split train/test ha prodotto una partizione vuota.")

    threshold = sum(row[0] for row in train_rows) / len(train_rows)
    correct = sum(
        (f1 >= threshold) == bool(label)
        for f1, _, label in test_rows
    )
    accuracy = round(correct / len(test_rows), 4)
    return {"threshold": threshold, "seed": seed}, accuracy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data.csv")
    parser.add_argument("--out", default="model.pkl")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    try:
        data = load_dataset(args.data)
        model, accuracy = train(data, args.seed)
    except (FileNotFoundError, ValueError) as error:
        parser.error(str(error))

    model["accuracy"] = accuracy
    with Path(args.out).open("wb") as model_file:
        pickle.dump(model, model_file)

    print(f"run: seed={args.seed} accuracy={accuracy} model={args.out}")


if __name__ == "__main__":
    main()
import pickle
import sys
from pathlib import Path


def gate(previous_accuracy, new_accuracy, artifact_path):
    return new_accuracy >= previous_accuracy and Path(artifact_path).is_file()


if __name__ == "__main__":
    previous_id, candidate_id = "model_a.pkl", "model_b.pkl"

    if not Path(previous_id).is_file() or not Path(candidate_id).is_file():
        print(f"gate: {candidate_id} vs baseline {previous_id} -> BLOCCATA (artefatto assente)")
        sys.exit(1)

    with Path(candidate_id).open("rb") as model_file:
        candidate_model = pickle.load(model_file)
    with Path(previous_id).open("rb") as model_file:
        previous_model = pickle.load(model_file)

    promoted = gate(
        previous_model["accuracy"],
        candidate_model["accuracy"],
        candidate_id,
    )
    status = "PROMOSSA" if promoted else "BLOCCATA"
    print(f"gate: {candidate_id} vs baseline {previous_id} -> {status}")
    sys.exit(0 if promoted else 1)
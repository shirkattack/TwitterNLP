"""Export a Prodigy dataset straight from the Prodigy DB into train/dev DocBins.

Binary accept/reject annotations are mapped to RELEVANT/IRRELEVANT and split
into a training and a development set.

Usage:
    python scripts/preprocess_from_prodigy.py <prodigy_dataset> corpus/train.spacy corpus/dev.spacy
"""
import random
from pathlib import Path
from typing import Iterable, List

import spacy
import typer
from prodigy.components.db import connect
from spacy.language import Language
from spacy.tokens import DocBin

POSITIVE = "RELEVANT"
NEGATIVE = "IRRELEVANT"
CATEGORIES = (POSITIVE, NEGATIVE)


def load_annotations(dataset_name: str) -> List[dict]:
    """Read a Prodigy dataset and keep only accepted/rejected examples."""
    db = connect()
    if dataset_name not in db:
        raise typer.BadParameter(f"Prodigy dataset {dataset_name!r} does not exist")
    records = []
    for eg in db.get_dataset(dataset_name):
        answer = eg.get("answer")
        if answer not in ("accept", "reject"):
            continue
        records.append(
            {"text": eg["text"], "label": POSITIVE if answer == "accept" else NEGATIVE}
        )
    return records


def make_docbin(nlp: Language, records: Iterable[dict], output: Path) -> int:
    doc_bin = DocBin()
    data_tuples = ((eg["text"], eg) for eg in records)
    for doc, eg in nlp.pipe(data_tuples, as_tuples=True):
        doc.cats = {category: float(category == eg["label"]) for category in CATEGORIES}
        doc_bin.add(doc)
    output.parent.mkdir(parents=True, exist_ok=True)
    doc_bin.to_disk(output)
    return len(doc_bin)


def main(
    dataset: str = typer.Argument(..., help="Name of the annotated Prodigy dataset"),
    output_train: Path = typer.Argument(..., dir_okay=False),
    output_dev: Path = typer.Argument(..., dir_okay=False),
    train_fraction: float = typer.Option(0.8, min=0.0, max=1.0, help="Share of examples used for training"),
    seed: int = typer.Option(0, help="Shuffle seed for a reproducible split"),
) -> None:
    nlp = spacy.blank("en")
    records = load_annotations(dataset)
    random.Random(seed).shuffle(records)
    split_idx = int(len(records) * train_fraction)
    train_docs, dev_docs = records[:split_idx], records[split_idx:]

    n_train = make_docbin(nlp, train_docs, output_train)
    n_dev = make_docbin(nlp, dev_docs, output_dev)
    print(f"Processed {n_train} training documents: {output_train}")
    print(f"Processed {n_dev} development documents: {output_dev}")


if __name__ == "__main__":
    typer.run(main)

"""Convert Prodigy-style JSONL annotations into spaCy's binary DocBin format.

Each input line is a JSON object with a ``text`` field and either

* a ``label`` field holding one of the category names, or
* a Prodigy binary annotation (``label`` + ``answer`` of accept/reject/ignore),
  in which case ``accept`` maps to the label and ``reject`` to its complement.

Usage:
    python scripts/preprocess.py assets/train.jsonl corpus/train.spacy
"""
from pathlib import Path
from typing import Dict, Optional

import spacy
import srsly
import typer
from spacy.tokens import DocBin

POSITIVE = "RELEVANT"
NEGATIVE = "IRRELEVANT"
CATEGORIES = (POSITIVE, NEGATIVE)


def example_to_cats(eg: dict) -> Optional[Dict[str, float]]:
    """Map one annotation record to a ``doc.cats`` dict, or None to skip it."""
    answer = eg.get("answer")
    if answer == "ignore":
        return None
    if answer in ("accept", "reject"):
        label = POSITIVE if answer == "accept" else NEGATIVE
    else:
        label = eg.get("label") or eg.get("labels")
    if label not in CATEGORIES:
        raise ValueError(
            f"Unknown label {label!r}; expected one of {CATEGORIES}. Record: {eg}"
        )
    return {category: float(category == label) for category in CATEGORIES}


def main(
    input_path: Path = typer.Argument(..., exists=True, dir_okay=False),
    output_path: Path = typer.Argument(..., dir_okay=False),
) -> None:
    nlp = spacy.blank("en")
    doc_bin = DocBin()
    skipped = 0
    data_tuples = ((eg["text"], eg) for eg in srsly.read_jsonl(input_path))
    for doc, eg in nlp.pipe(data_tuples, as_tuples=True):
        cats = example_to_cats(eg)
        if cats is None:
            skipped += 1
            continue
        doc.cats = cats
        doc_bin.add(doc)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc_bin.to_disk(output_path)
    print(f"Processed {len(doc_bin)} documents ({skipped} skipped): {output_path}")


if __name__ == "__main__":
    typer.run(main)

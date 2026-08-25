"""Convert a CSV of raw tweets into the JSONL format Prodigy expects.

Usage:
    python scripts/prodigy_formatter.py --import-file tweets.csv --output tweets.jsonl

The CSV must have a header row; the column holding the tweet text defaults to
``text`` and can be changed with ``--text-column``.
"""
import csv
from pathlib import Path
from typing import Iterator

import srsly
import typer


def read_texts(input_path: Path, text_column: str) -> Iterator[dict]:
    with input_path.open("r", encoding="utf8", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None or text_column not in reader.fieldnames:
            raise typer.BadParameter(
                f"Column {text_column!r} not found in {input_path}; columns: {reader.fieldnames}"
            )
        for row in reader:
            text = (row.get(text_column) or "").strip()
            if text:
                yield {"text": text}


def main(
    import_file: Path = typer.Option(..., exists=True, dir_okay=False, help="CSV file to convert"),
    output: Path = typer.Option(..., dir_okay=False, help="Destination JSONL file"),
    text_column: str = typer.Option("text", help="Name of the CSV column containing the text"),
) -> None:
    records = list(read_texts(import_file, text_column))
    output.parent.mkdir(parents=True, exist_ok=True)
    srsly.write_jsonl(output, records)
    print(f"Wrote {len(records)} records from {import_file} to {output}")


if __name__ == "__main__":
    typer.run(main)

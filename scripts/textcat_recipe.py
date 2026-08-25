"""Prodigy recipe for plain manual text classification of tweets.

Streams a JSONL file, drops duplicate texts and shows each example in the
binary classification interface. No model is involved, which makes this the
recipe to use when bootstrapping the very first annotations.

Usage:
    prodigy textcat.manual-tweets my_dataset tweets.jsonl --label RELEVANT -F scripts/textcat_recipe.py
"""
from typing import List

import prodigy
from prodigy.components.filters import filter_duplicates
from prodigy.components.loaders import JSONL
from prodigy.util import set_hashes, split_string


@prodigy.recipe(
    "textcat.manual-tweets",
    dataset=("The dataset to save annotations to", "positional", None, str),
    source=("The source data as a JSONL file", "positional", None, str),
    label=("One or more comma-separated labels", "option", "l", split_string),
)
def textcat_manual_tweets(dataset: str, source: str, label: List[str] = None):
    labels = label or ["RELEVANT"]
    stream = (set_hashes(eg) for eg in JSONL(source))
    stream = filter_duplicates(stream, by_input=True, by_task=False)
    # Attach the label so the classification view shows it on every card
    stream = ({**eg, "label": labels[0]} for eg in stream)

    return {
        "view_id": "classification",
        "dataset": dataset,
        "stream": stream,
        "config": {"labels": labels},
    }

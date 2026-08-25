"""Prodigy recipe: active-learning text classification with a trained spaCy model.

The model scores incoming tweets, the ``prefer_uncertain`` sorter surfaces the
ones it is least sure about, and every batch of answers is fed back into the
model so its suggestions improve during the session. Optionally, a JSONL file
of match patterns can be combined with the model to seed positive examples.

Usage:
    prodigy textcat.teach-custom my_dataset tweets.jsonl \
        --model training/model-best --label RELEVANT \
        --patterns patterns/patterns.jsonl -F scripts/textcat_teach.custom_model.py
"""
from typing import List, Optional

import prodigy
import spacy
from prodigy.components.filters import filter_duplicates
from prodigy.components.loaders import JSONL
from prodigy.components.sorters import prefer_uncertain
from prodigy.models.matcher import PatternMatcher
from prodigy.models.textcat import TextClassifier
from prodigy.util import combine_models, split_string


@prodigy.recipe(
    "textcat.teach-custom",
    dataset=("The dataset to save annotations to", "positional", None, str),
    source=("The source data as a JSONL file", "positional", None, str),
    model=("Path to or name of a spaCy pipeline with a textcat component", "option", "m", str),
    patterns=("Optional JSONL file of match patterns", "option", "p", str),
    label=("One or more comma-separated labels", "option", "l", split_string),
)
def textcat_teach_custom(
    dataset: str,
    source: str,
    model: str = "training/model-best",
    patterns: Optional[str] = None,
    label: Optional[List[str]] = None,
):
    labels = label or ["RELEVANT"]
    nlp = spacy.load(model)
    stream = filter_duplicates(JSONL(source), by_input=True, by_task=False)
    textcat = TextClassifier(nlp, labels)

    if patterns is None:
        predict, update = textcat, textcat.update
    else:
        matcher = PatternMatcher(
            nlp,
            prior_correct=5.0,
            prior_incorrect=5.0,
            label_span=False,
            label_task=True,
        ).from_disk(patterns)
        # Interleave model and matcher suggestions and update both on answers
        predict, update = combine_models(textcat, matcher)

    # Focus annotation effort on examples scored closest to 0.5
    stream = prefer_uncertain(predict(stream))

    return {
        "view_id": "classification",
        "dataset": dataset,
        "stream": stream,
        "update": update,
        "config": {"labels": labels},
    }

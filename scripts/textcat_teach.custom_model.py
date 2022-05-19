# prodigy textcat.custom_model testdata2 /home/esteban/Patterns_Factory/Pattern_Maker/textcat_patterns.jsonl --label RELEVANT -F textcat_teach.custom_model.py 

import prodigy
import spacy
from prodigy.components.loaders import JSONL
from prodigy.components.sorters import prefer_uncertain
#from prodigy.components.sorters import prefer_high_scores

from prodigy.models.textcat import TextClassifier
from prodigy.models.matcher import PatternMatcher
from prodigy.util import combine_models, split_string
import random
from typing import List, Iterable
from prodigy.components.preprocess import split_sentences
from prodigy.components.filters import filter_duplicates
from typing import List, Optional



@prodigy.recipe(
    "textcat.custom-model",
    dataset=("The dataset to use", "positional", None, str),
    source=("The source data as a JSONL file", "positional", None, str),
    patterns=("Optional match patterns", "option", "p", str),
    label=("One or more comma-separated labels", "option", "l", split_string),
)
def textcat_custom_model(dataset: str, source: str, label: List[str], patterns: Optional[str] = None,):
    """
    Use active learning-powered text classification with a custom model. To
    demonstrate how it works, this demo recipe uses a simple dummy model that
    "precits" random scores. But you can swap it out for any model of your
    choice, for example a text classification model implementation using
    PyTorch, TensorFlow or scikit-learn.
    """
    # Load the stream from a JSONL file and return a generator that yields a
    # dictionary for each example in the data.
    

    #nlp = spacy.load("/home/esteban/Patterns_Factory/ANNOTATIONS/TEXTCAT/dmp_textcat_model")
    #nlp = spacy.load("/home/esteban/Patterns_Factory/ANNOTATIONS/TEXTCAT/dmp_textcat_model")
    
    nlp = spacy.load("/home/esteban/twitter_nlp/training/model-best")
    
    stream = JSONL(source)
    
    # stream = split_sentences(nlp, stream) # Use this for the REDDIT data

    stream = filter_duplicates(stream, by_input=True, by_task=False)
    
    model = TextClassifier(nlp, label)


    
    if patterns is None:
        # No patterns are used, so just use the model to suggest examples
        # and only use the model's update method as the update callback
        predict = model
        update = model.update
    else:
        # Initialize the pattern matcher and load in the JSONL patterns.
        # Set the matcher to not label the highlighted spans, only the text.
        matcher = PatternMatcher(
            nlp,
            prior_correct=5.0,
            prior_incorrect=5.0,
            label_span=False,
            label_task=True,
        )
        matcher = matcher.from_disk(patterns)
        # Combine the NER model and the matcher and interleave their
        # suggestions and update both at the same time
        predict, update = combine_models(model, matcher)

    # Use the prefer_uncertain sorter to focus on suggestions that the model
    # is most uncertain about (i.e. with a score closest to 0.5). The model
    # yields (score, example) tuples and the sorter yields just the example
    

    # The update method is called every time Prodigy receives new answers from
    # the web app. It can be used to update the model in the loop.
    #update = model.update

    stream = prefer_uncertain(model(stream))

    #uncomment the below option to stream high scores instead of uncertain
    #stream = prefer_high_scores(model(stream))

    return {
        "view_id": "classification",  # Annotation interface to use
        "dataset": dataset,  # Name of dataset to save annotations
        "stream": stream,  # Incoming stream of examples
        #"update": update,  # Update callback, called with batch of answers
        "config": {
            "labels": ["RELEVANT"]}
    }
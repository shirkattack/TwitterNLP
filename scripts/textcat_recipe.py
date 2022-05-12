# pyenv activate nightly
# prodigy textcat.custom_model testdata2 excellent_textcat_patterns_part2.jsonl -F textcat_recipe.py
import prodigy
import spacy
from prodigy.components.loaders import JSONL
from prodigy.components.sorters import prefer_uncertain
from prodigy.util import split_string
import random
from typing import List, Iterable
from prodigy.util import set_hashes
#from prodigy.components.preprocess import split_sentences
from prodigy.components.filters import filter_duplicates



@prodigy.recipe(
    "textcat.custom-model",
    dataset=("The dataset to use", "positional", None, str),
    source=("The source data as a JSONL file", "positional", None, str),
    #exclusive=("Treat classes as mutually exclusive", "flag", "E", bool),
    label=("One or more comma-separated labels", "option", "l", split_string),
)
def textcat_custom_model(dataset: str, source: str, label: List[str]):
    """
    Use active learning-powered text classification with a custom model. To
    demonstrate how it works, this demo recipe uses a simple dummy model that
    "predicts" random scores. But you can swap it out for any model of your
    choice, for example a text classification model implementation using
    PyTorch, TensorFlow or scikit-learn.
    """
    # Load the stream from a JSONL file and return a generator that yields a
    # dictionary for each example in the data.
    
    nlp = spacy.load('en_core_web_sm')
    
    stream = JSONL(source)
    #stream = prefer_uncertain(model(stream))
    #stream = split_sentences(nlp, stream)
    stream = [set_hashes(eg) for eg in stream]
    stream = filter_duplicates(stream, by_input=True, by_task=False)
    
    
    
    labels = ['RELEVANT']

    # The update method is called every time Prodigy receives new answers from
    # the web app. It can be used to update the model in the loop.
    #update = model.update


    return {
        "view_id": "classification",  # Annotation interface to use
        "dataset": dataset,  # Name of dataset to save annotations
        "stream": stream,  # Incoming stream of examples
        #"update": update,  # Update callback, called with batch of answers
        "config": {'labels': labels}
    }


# Add annotation instructions into the recipe



# Add a custom match pattern option
# nlp = spacy.load(spacy_model)

#     # Initialize the pattern matcher and load in the JSONL patterns
#     matcher = PatternMatcher(nlp).from_disk(patterns)

#     if resume:
#         # Connect to the database using the settings from prodigy.json
#         DB = connect()
#         if dataset and dataset in DB:
#             # Get the existing annotations and update the matcher
#             existing = DB.get_dataset(dataset)
#             matcher.update(existing)

#     # Load the stream from a JSONL file and return a generator that yields a
#     # dictionary for each example in the data.
#     stream = JSONL(source)

#     # Apply the matcher to the stream, which returns (score, example) tuples.
#     # Filter out the scores to only yield the examples for annotations.
#     stream = (eg for score, eg in matcher(stream))

# def custom_csv_loader(file_path):
#     with open(file_path) as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             text = row.get('Text')
#             yield {'text': text, 'meta': {'original':text}}


#class DummyModel(object):
#     # This is a dummy model to help illustrate how to use Prodigy with a model
#     # in the loop. It currently "predicts" random numbers – but you can swap
#     # it out for any model of your choice, for example a text classification
#     # model implementation using PyTorch, TensorFlow or scikit-learn.

#     def __init__(self, labels: List[str]):
#         # The model can keep arbitrary state – let's use a simple random float
#         # to represent the current weights
#         self.weights = random.random()
#         self.labels = labels

#     def __call__(self, stream: Iterable[dict]):
#         for eg in stream:
#             # Score the example with respect to the current weights and
#             # assign a label
#             eg["label"] = random.choice(self.labels)
#             score = (random.random() + self.weights) / 2
#             yield (score, eg)

#     def update(self, answers: List[dict]):
#         # Update the model weights with the new answers. This method receives
#         # the examples with an added "answer" key that either maps to "accept",
#         # "reject" or "ignore".
#         self.weights = random.random()


# Recipe decorator with argument annotations: (description, argument type,
# shortcut, type / converter function called on value before it's passed to
# the function). Descriptions are also shown when typing --help.
import typer
import random
from prodigy.components.db import connect
#import srsly
from pathlib import Path
from spacy.util import get_words_and_spaces
from spacy.tokens import Doc, DocBin
import spacy


def preprocess(annotated):
    """use this to get a binanry classification dataset
    Args:
        annotated (_str_): _description_
        dataset (_list_): imported list of annotated data from prodigy
    Returns:
        _type_: list of dictionary
    """
    db = connect()
    dataset = db.get_dataset(annotated) # name of the prodigy labeled data
    processed = []
    for data in dataset:
        if data['answer'] != 'ignore':
            processed.append({
                'text': data['text'],
                'labels': 'RELEVANT' if 'accept' in data['answer'] else 'IRRELEVANT'
            })
    return processed


def make_spacy(nlp, output, records, categories):
    #nlp = spacy.blank("en")
    doc_bin = DocBin()
    data_tuples = ((eg["text"], eg) for eg in records)
    for doc, eg in nlp.pipe(data_tuples, as_tuples=True):
        doc.cats = {category:0 for category in categories}
        doc.cats[eg["labels"]] = 1
        doc_bin.add(doc)
    return doc_bin.to_disk(output)


def main(
    #input_path: Path = typer.Argument(..., exists=True, dir_okay=False),
    output_train: Path = typer.Argument(..., dir_okay=False), # output training
    output_dev: Path = typer.Argument(..., dir_okay=False), # output dev
):
    
    CATEGORIES = ['RELEVANT', 'IRRELEVANT']
    SPLIT_EVAL = 0.8
    nlp = spacy.blank("en")

    #output_dev = "./dev_docs.spacy"
    #output_train = "./train_docs.spacy"
    
    train_docs = preprocess(str("merged_twitter2"))
    random.shuffle(train_docs)
    split_idx = int(len(train_docs) * SPLIT_EVAL)
    train_docs, dev_docs = train_docs[:split_idx], train_docs[split_idx:]

    # output for the training data
    make_spacy(nlp, output_train, train_docs, CATEGORIES)
    # output for the eval data
    make_spacy(nlp, output_dev, dev_docs, CATEGORIES)
    print(f"Processed {len(train_docs)} documents: {output_train}")
    print(f"Processed {len(dev_docs)} documents: {output_dev}")


if __name__ == "__main__":
    typer.run(main)
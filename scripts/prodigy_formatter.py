import argparse
import csv
import srsly

def read_file(input_path):
    results = []
    with open(input_path, "r", encoding="utf8") as file:
        csvreader = csv.reader(file)
        for x in csvreader:
            results.append({"text": x[0]})
    return results


def main(params: argparse.Namespace) -> None:
    print('-' * 140)
    print(f"Reading Data for conversion into Prodigy Format for file: {params.import_file}")
    text = read_file(params.import_file)
    print('-' * 140)
    srsly.write_jsonl(params.output, text)
    print('-' * 140)
    print(f'Finished Processing the {params.output} JSONL Data')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Arguments for converting a csv into a Spacy JSONL training data file",
        add_help=True,
    )
    parser.add_argument(
        "--import_file",
        type=str,
        default="training_data.csv",
        help="import path for the .csv file you want to convert",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="training_data.jsonl",
        help="Enter the output path to export the JSONL file.",
    )
   
    params = parser.parse_args()
    main(params)

# In the CLI run the command below:
# python prodigy_formatter.py --import_file test.csv --output data.jsonl
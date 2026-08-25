# TwitterNLP: Detecting Cryptocurrency Scams on Twitter

A [spaCy](https://spacy.io) text-classification project that flags tweets
discussing scams and fraud in cryptocurrency. Tweets were annotated in
[Prodigy](https://prodi.gy) using an active-learning loop, weak-labelled with
[Snorkel](https://www.snorkel.org/) labelling functions, and the resulting model
was tuned with [Weights & Biases](https://wandb.ai) sweeps.

The classifier is binary: `RELEVANT` (the tweet describes a scam, a fraud
event, or how to identify one) vs `IRRELEVANT` (everything else, including
promotions that merely mention the word "scam").

## Project layout

| Path | Purpose |
| --- | --- |
| `project.yml` | spaCy project definition: assets, commands and workflows |
| `configs/` | Training configs: `config.cfg` (CPU bag-of-words), `cnn.cfg` (CNN), `bert.cfg` (transformer, GPU) |
| `corpus/` | Binary `train.spacy` / `dev.spacy` corpora, W&B sweep definitions and the sample annotation data |
| `patterns/` | Token-match patterns (crypto, cyber, scam vocabularies) used to seed annotation |
| `scripts/` | Preprocessing, Prodigy recipes, sweep runners and the Streamlit demo |
| `notebooks/` | Data preparation and Snorkel labelling-function experiments |
| `assets/` | Raw annotation exports and downloaded vectors |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_lg   # vectors used by the CPU/CNN configs
```

The Prodigy recipes additionally require a [Prodigy](https://prodi.gy)
licence. Weights & Biases logging requires `wandb login`; to train without it,
switch `[training.logger]` in the chosen config to `spacy.ConsoleLogger.v1`.

## Commands

Commands are run with [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and are only re-executed when their inputs change.

| Command | Description |
| --- | --- |
| `preprocess` | Convert the JSONL annotations in `assets/` to spaCy's binary format |
| `init-labels` | Generate the label files for the training config |
| `train` | Train the text classification model (`vars.config` selects the architecture) |
| `evaluate` | Evaluate `training/model-best` and export `training/metrics.json` |
| `sweep` | Run a Bayesian W&B hyperparameter sweep |
| `visualize` | Launch the Streamlit demo |
| `package` | Package the trained model as a pip-installable wheel |

The `all` workflow runs `preprocess` → `train` → `evaluate`:

```bash
python -m spacy project run all
```

To train on a GPU with the transformer config:

```bash
python -m spacy project run train . --vars.config bert.cfg --vars.gpu_id 0
```

## Annotation workflow

1. Convert raw tweets to Prodigy's JSONL format:

   ```bash
   python scripts/prodigy_formatter.py --import-file tweets.csv --output tweets.jsonl
   ```

2. Bootstrap a first dataset with the manual recipe:

   ```bash
   prodigy textcat.manual-tweets crypto_scams tweets.jsonl --label RELEVANT -F scripts/textcat_recipe.py
   ```

3. Once a first model is trained, switch to the active-learning recipe, which
   surfaces the tweets the model is least certain about and updates the model
   with every batch of answers. Match patterns can be mixed in to seed
   positive examples:

   ```bash
   prodigy textcat.teach-custom crypto_scams tweets.jsonl \
       --model training/model-best --label RELEVANT \
       --patterns patterns/patterns.jsonl -F scripts/textcat_teach.custom_model.py
   ```

4. Export the dataset straight from the Prodigy database into train/dev corpora:

   ```bash
   python scripts/preprocess_from_prodigy.py crypto_scams corpus/train.spacy corpus/dev.spacy
   ```

### Annotation policy

A tweet is `RELEVANT` when it is one of:

1. A description of a specific behaviour or pattern of a cryptocurrency scam
2. A specific event involving a cryptocurrency coin, token or its value being
   used fraudulently
3. Instructive content on how to identify a scam (e.g. tutorials, tips)

A tweet is `IRRELEVANT` when it merely *mentions* scams — most commonly
promotions for scam-checker tools, "we recover your lost crypto" services or
generic hype. Some examples that shaped the policy:

| Tweet (abridged) | Label | Why |
| --- | --- | --- |
| "Sick of getting rugged and scammed in Crypto? … this team is working hard to change things! Check them out" | `IRRELEVANT` | Promotion that name-drops scams |
| "Honeypot/scam checker, buy/sell tax, audits, whitepapers, all token data in one place" | `IRRELEVANT` | Product promotion |
| "Be cautious of profiles where they use BAYC and Crypto Punks PFPs … people make accounts with them to gain followers or scam people" | `RELEVANT` | Scam-identification advice |
| "Supreme Court asks crypto currency scam accused to disclose username, password of Bitcoin wallet" | `RELEVANT` | News about a specific fraud event |
| "many a scam coin in crypto #apecoin looks like one" | edge case | Opinion without a described behaviour |

## Hyperparameter sweeps

`corpus/sweep_bayes.yml` defines a W&B sweep over dropout, learning rate,
n-gram size and CNN depth, optimising macro AUC on the dev set. It can be
launched either through the W&B CLI or from Python:

```bash
wandb sweep corpus/sweep_bayes.yml && wandb agent <sweep-id>
# or
python scripts/spacy_sweeps.py corpus/gpu_config.cfg training --gpu-id 0 --count 20
```

## Data

The `corpus/data/` directory contains the annotation exports used for this
project (raw tweet text collected via the Twitter API, filtered with the
patterns in `patterns/`). See the note in that directory before redistributing
tweet content.

## Roadmap

Beyond the binary classifier, the wider project aimed to add:

| Model | Labels |
| --- | --- |
| Multi-label classification | `Fraud Event`, `Fraud Description` |
| Named Entity Recognition | `Person`, `Cryptotoken`, `Contract`, `Value`, `Buyer and Seller` |
| Threat-level score | 0–99 |
| Credibility score | 0–99 |

## License

Released under the [MIT License](LICENSE).

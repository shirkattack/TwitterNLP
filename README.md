<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# Mapping the Crypto Risk Landscape: Detecting Scams in Cryptocurrency through Social Media (Text Classification)

This project uses [spaCy](https://spacy.io) with annotated data from [Prodigy](https://prodi.gy) to train a **binary text classifier with exclusive classes** to predict Tweets focused on scams and fraud in cryptocurrency.

The model classifies negative tweets about scams relating to cryptocurrency into categories based on what the scam is about. Designed to strengthen risk assesment for investment in cryptocurrency.

## 📋 project.yml

The [`project.yml`](project.yml) defines the data assets required by the
project, as well as the available commands and workflows. For details, see the
[spaCy projects documentation](https://spacy.io/usage/projects).

### ⏯ Commands

The following commands are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run).
Commands are only re-run if their inputs have changed.

| Command | Description |
| --- | --- |
| `preprocess` | Convert the data to spaCy's binary format |
| `train` | Train a text classification model |
| `evaluate` | Evaluate the model and export metrics |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `all` | `preprocess` &rarr; `train` &rarr; `evaluate` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| [`assets/train.jsonl`](assets/docs_issues_training.jsonl) | Local | JSONL-formatted training data exported from Prodigy, annotated with `RELEVANT` `IRRELEVANT` (XXX examples) |
| [`assets/dev.jsonl`](assets/docs_issues_eval.jsonl) | Local | JSONL-formatted development data exported from Prodigy, annotated with `RELEVANT` `IRRELEVANT` (XXX examples) |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->

## 📚 Data

Labelling the data with [Prodigy](https://prodi.gy) took about two hours and was
done manually using the binary classification interface. The raw text was
sourced from the from the [GitHub API](https://developer.github.com/v3/) using
the search queries `"docs"`, `"documentation"`, `"readme"` and `"instructions"`.

### Training and evaluation data format

The training and evaluation datasets are distributed in Prodigy's simple JSONL
(newline-delimited JSON) format. Each entry contains a `"text"`, the `"label"`
and an `"answer"` (`"accept"` if the label applies, `"reject"` if it doesn't
apply). Here are two simplified example entries:

```json
{
  "text": "Add FAQ's to the documentation",
  "label": "DOCUMENTATION",
  "answer": "accept"
}
```

```json
{
  "text": "Proposal: deprecate SQTagUtil.java",
  "label": "DOCUMENTATION",
  "answer": "reject"
}
```

### List of labels and corresponding titles

|               **Models**               |  **Labels**  |
| :-----------------------------------: | :---------------------: |
|       🚀 Multiclassification        |       `Fraud Event`, `Fraud Description`       |
| 🔧 Named Entity Recognition | `Person`, `Cryptotoken`, `Contract`, `Value`, `Buyer and Seller`  |
|       📦 Threat-Level Score        | `scores range from 0-99` |
|              💥 Credibility Score               |   💥 `scores range from 0-99`   |

### Data creation workflow

```bash
prodigy mark docs_issues_data ./raw_text.jsonl --label DOCUMENTATION --view-id classification
```

### Annotation Policy for Text Classification
1. Something that describes a specific behavior or pattern of a scam with regards to cryptocurrency
2. Something that describes a specific EVENT detailing the crypto currency coin or value
multiclassification (fraud event, fraud description)
3. Something that is instructive to identify a scam (e.g. Tutorials on how to identify a scam)

<img width="250" src="https://user-images.githubusercontent.com/13643239/69798875-7d3a5280-11d2-11ea-94d2-e04f9e18b69e.png" alt="" align="right">

## 🚘🐱 Live demo and model download

We also trained
[a model](https://autocat.apps.allenai.org/?uid=d9cd6f8c-8f1d-4367-b1ae-b6264bfe2cda)
using Allen AI's [Autocat](https://autocat.apps.allenai.org) app (a web-based
tool for training, visualizing and showcasing spaCy text classification models).
You can try out the classifier in real-time and see the updated predictions as
you type. You can also evaluate it on your own data, download the model Python
package or just `pip install` it with one command to try it locally.
[**View model here.**](https://autocat.apps.allenai.org/?uid=d9cd6f8c-8f1d-4367-b1ae-b6264bfe2cda)

To use the JSONL data in Autocat, we added `"labels": ["DOCUMENTATION"]` to all
examples with `"answer": "accept"` and `"labels": ["N/A"]` to all examples with
`"answer": "reject"`.

False positve Examples:

"@NFTONETHWeb3 @ShibNFTMeta @MetaMartianss Sick of getting rugged and scammed in Crypto? 
Wanna change it?
While most just complain, this team is working hard to change things!
Check them out https://t.co/n0yrTpQPmu https://t.co/3IcQdiL89E"

@newbornseal @LofiGuyNFT Come join us as we go on the adventure of giving
visibility into scammers and how they operate. We
help recover lost crypto &amp; Nft to those who got
scammed!

# False positive
below is considered a 'promotion' and therefore a false positive

RT @Hunter_samurai1: ♦️Honeypot/scam checker, buy/sell tax, audits, whitepapers, all token data all in one place with auto-refresh
#CoinSca

# false positive promotion below
WARNING! KOXX-PAYING - OUTSIDE PROJECT - 99.9% FAST SCAM SIGNALS! BEWARE..

https://t.co/McixwLYCy6

#EmilyNews #invest #HYIPs #bitcoin #crypto #btc


# Edge case (ambivalkence)
not sure about the below:
many a scam coin in crypto #apecoin looks like one

# not sure about this one
Beware of people trying to scam on emblems. No bungie email proof, want money sent via cashapp/crypto, random profile. Btw guys here’s a code for Darkest Day Emblem stv-fy4-32j, you all owe me $500 🤣🤣🤣🤣🤣🤣 https://t.co/IFcLTJ9lJa

# Scam ADVICE
NFT Tip of the day:
Be cautious of profiles where they use BAYC and Crypto Punks PFPs. Since these are the most reputable projects out, people will sometimes make accounts with them as the PFP to gain followers or scam people.

# Scam NEWS
Supreme Court asks crypto currency scam accused to disclose username, password of Bitcoin wallet to ED
#cryptocurrency 
https://t.co/83XSkWThdR
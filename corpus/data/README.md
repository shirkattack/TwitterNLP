# Annotation data

| File | Contents |
| --- | --- |
| `twitter_training_data.csv` / `.jsonl` | Raw tweets collected via the Twitter API with crypto-related search terms (`ID`, `text`) |
| `twitter_filtered.jsonl` | Tweets matching the `patterns/` vocabularies, used to seed annotation |
| `twitter_annotation_data.csv` | Tweets queued for Prodigy annotation |
| `filtered_training_data.csv` | Annotated tweets with `RELEVANT` / `IRRELEVANT` labels |
| `twitter_test_data.csv` | Held-out tweets with Prodigy `accept` / `reject` answers |
| `new_annotation_data.jsonl` | Second annotation batch, weak-labelled in `notebooks/twitter_pattern_maker.ipynb` |

**Redistribution note:** these files contain tweet text and user handles.
The Twitter/X developer policy only permits redistributing tweet *IDs* at
scale; if you reuse this data, rehydrate from the `ID` column rather than
copying the text.

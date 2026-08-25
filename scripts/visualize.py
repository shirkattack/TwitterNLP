"""Streamlit demo: classify a tweet with the trained scam-detection model.

Usage:
    streamlit run scripts/visualize.py
    MODEL_PATH=path/to/model-best streamlit run scripts/visualize.py
"""
import os
from pathlib import Path

import spacy
import spacy_streamlit
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = Path(os.environ.get("MODEL_PATH", ROOT / "training" / "model-best"))


@st.cache_resource
def load_model(path: str):
    return spacy.load(path)


st.title("TwitterNLP Scam Identifier")

if not MODEL_PATH.exists():
    st.error(
        f"No trained model found at {MODEL_PATH}. Run `spacy project run train` "
        "or set the MODEL_PATH environment variable."
    )
    st.stop()

nlp = load_model(str(MODEL_PATH))
text = st.text_input("Enter a tweet to classify")
if text:
    spacy_streamlit.visualize_textcat(nlp(text))

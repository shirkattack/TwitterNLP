import streamlit as st
import spacy
import spacy_streamlit
from spacy_streamlit import visualize_textcat


model = "/home/esteban/twitter_nlp/training/model-best"

model_name = "cardiff_hf_2.0"
st.image('/home/esteban/twitter_nlp/scripts/brg.png', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
st.title("TwitterNLP Scam Identifier")
default_text = st.text_input("Enter the sentence")

nlp = spacy.load(model)
doc = nlp(default_text)

spacy_streamlit.visualize_textcat(doc)

st.text(f"Classification Model Developed by the BRG Innovation Lab")

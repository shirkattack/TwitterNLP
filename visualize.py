#import spacy
# #from spacy_streamlit import visualize_ner
# import spacy_streamlit

# models = ["/home/esteban/twitter_nlp/model/model-best"] #enter path to model here
# #doc = nlp("I was scammed by cryptocurrency")
# default_text = "I was scammed by cryptocurrency"
# visualizers = ["textcat"]
# spacy_streamlit.visualize(models, default_text, visualizers)


# import spacy
# import streamlit as st
# from spacy_streamlit import visualize_textcat


# model = "/home/esteban/twitter_nlp/model/model-best"
# nlp = spacy.load(model)
# doc = nlp("I truly and sincerely have enough ETH in my wallet but I have no Bitcoin and I am willing to swap my ETH for BTC.... Please kindly hit me up if you needed ETH and you will send me 2BTC. This is not a scam.")
# visualize_textcat(doc)



import streamlit as st
import spacy
import spacy_streamlit
from spacy_streamlit import visualize_textcat

default_text = "I truly and sincerely have enough ETH in my wallet but I have no Bitcoin and I am willing to swap my ETH for BTC.... Please kindly hit me up if you needed ETH and you will send me 2BTC. This is not a scam."

model = "/home/esteban/twitter_nlp/model/model-best"
model_name = "cardiff_hf_2.0"

nlp = spacy.load(model)
doc = nlp(default_text)

st.title("TwitterNLP Scam Identifier")

spacy_streamlit.visualize_textcat(
    doc)

st.text(f"Model *{model_name}* Developed by the BRG Innovation Lab")
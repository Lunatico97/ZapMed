# !!! WARNING: Make sure you read my comments! --> {Diwas}
# Subroutine to generate summary

from transformers import AutoTokenizer, TFAutoModelForSeq2SeqLM
import nltk
import streamlit as st


# Subroutine to load T5-trained tokenizer and model
# @st.cache(allow_output_mutation=True) ---> Deprecated
@st.cache_resource(show_spinner=True)
def load_model(model_card):
    print("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained(model_card)
    model = TFAutoModelForSeq2SeqLM.from_pretrained(model_card)
    nltk.download("punkt")
    print("Are you ready to zap in an instant !")
    return tokenizer, model


class Summarizer:
    def __init__(self, model_card, max_input_length=1024):
        # Set up name of model card
        self.model_card = model_card
        self.max_input_length = max_input_length ;

    def kickstart_model(self):
        self.tokenizer, self.model = load_model(self.model_card) ;

    def generate_summary(self, text, limit, ngs, lp, rp, temp, beams=8):
        # Tokenize text to feed the model
        inputs = ["summarize: " + text]
        inputs = self.tokenizer(
            inputs,
            max_length=self.max_input_length,
            truncation=True,
            return_tensors="tf",
        )
        # Compute predictions
        print(text, limit, ngs, lp, rp, temp, beams) ;
        print('Generating summary .....') ;
        output = self.model.generate(
            **inputs,
            do_sample=True,
            num_beams=beams,
            min_length=limit - 10,
            max_length=limit,
            no_repeat_ngram_size=ngs,
            length_penalty=lp,
            repetition_penalty=rp,
            temperature=temp,
            top_k=50,
            top_p=0.95
        )
        decoded_output = self.tokenizer.batch_decode(output, skip_special_tokens=True)[0] ;
        summary = nltk.sent_tokenize(decoded_output.strip()) ;
        print('Summary generated successfully !!') ;
        return summary

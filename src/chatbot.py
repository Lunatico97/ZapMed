# !!! WARNING: Make sure you read my comments! --> {Diwas}
# Subroutine to answer prompts

from transformers import AutoTokenizer, TFAutoModelForSeq2SeqLM ;
import nltk
import streamlit as st

# Subroutine to load T5-trained tokenizer and model for context prompting
# @st.cache(allow_output_mutation=True) ---> Deprecated
@st.cache_resource(show_spinner=True)
def loadFlanT5():
    print("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
    model = TFAutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
    return tokenizer, model


class Chatbot:
    def __init__(self, max_input_length=1024):
        self.max_input_length = max_input_length ;

    def kickstart_model(self):
        self.tokenizer, self.model = loadFlanT5() ;

    def askQuery(self, question, context):
        # Tokenize text to feed the model
        parameters = {
            "max_new_tokens": 50,
            "top_k": 50,
            "top_p": 0.95,
            "do_sample": True,
        }
        text = "{context}\nAnswer this question: {question}" ;
        text = text.replace("{context}", context) ;
        text = text.replace("{question}", question) ;

        inputs = self.tokenizer(
            text,
            max_length=self.max_input_length,
            truncation=True,
            return_tensors="tf",
        )
        # Compute predictions
        print(text, parameters) ;
        print('Answering ....') ;
        output = self.model.generate(
            **inputs,
            num_beams=5,
            **parameters
        )
        decoded_output = self.tokenizer.batch_decode(output, skip_special_tokens=True)[0] ;
        answer = nltk.sent_tokenize(decoded_output.strip()) ;
        print('Summary generated successfully !!') ;
        return answer ;


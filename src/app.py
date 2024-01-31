# !!! WARNING: Make sure you read my comments! --> {Diwas}
# Import libraries
import os ;
import streamlit as st ;
from extractor import base_path ;
from summarizer import Summarizer ;
from pdfer import displayPDF, getTextFromPDF, textToChunks, cleanText ;

# PDF2Text Function
def PDF2Text(filename):
    name = getTextFromPDF(filename) ;
    with open(f"{base_path}/output/{name}.txt", "r") as f:
        text = f.readlines() ;
        #print(text) ;
    f.close() ;
    return text ;

# Page Title Configuration
st.set_page_config(
    page_title="ZapMed",
    page_icon="⚡",
) ;

# Header Texts
st.header("Zap through your medical papers and articles") ;
st_model_load = st.text('!!!!! WAIT --- Setting up environment !!!!!') ;

# Initialize summarizer with model card
summarizer = Summarizer(model_card = "DiwasDiwas/t5-small-ZapMed") ;
summarizer.kickstart_model() ;
st.success('⚡ Are you ready to zap in an instant !? ⚡') ;
st_model_load.text("") ;

# Defaults
if 'max_length' not in st.session_state:
    st.session_state.max_length = 100 ;
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.8 ;
if 'length_penalty' not in st.session_state:
    st.session_state.length_penalty = 2.0 ;
if 'repitition_penalty' not in st.session_state:
    st.session_state.repitition_penalty = 5.0 ;
if 'ngrams_norepeat' not in st.session_state:
    st.session_state.ngrams_norepeat = 2 ;
if 'beams' not in st.session_state:
    st.session_state.beams = 4 ;

# On-Change Functions
def on_change_max_length():
        st.session_state.max_length = max_length ;

def on_change_length_penalty():
    st.session_state.length_penalty = length_penalty ;

def on_change_temperature():
   st.session_state.temperature = temperature ;

def on_change_repitition_penalty():
    st.session_state.repitition_penalty = repitition_penalty ;

def on_change_beams():
    st.session_state.beams = beams ;

def on_change_ngrams_norepeat():
    st.session_state.ngrams_norepeat = ngrams_norepeat ;

# Sidebar components with sliders to configure model parameters
with st.sidebar:
    st.image('images/zapmed.png') ;
    st.header("Options") ;
    max_length = st.slider("Generation Length", min_value=50, max_value=128, value=100, step=5, on_change=on_change_max_length) ;
    length_penalty = st.slider("Length Penalty", min_value=1, max_value=10, value=2, step=1, on_change=on_change_length_penalty) ;
    advanced = st.sidebar.checkbox(label="Advanced Options ") ;
    if advanced:  
        temperature = st.slider("Temperature", min_value=0.1, max_value=1.5, value=0.8, step=0.05, on_change=on_change_temperature) ;
        st.markdown("_[Diversity / Randomness]_")        
        repitition_penalty = st.slider("Repitition Penalty", min_value=1.0, max_value=10.0, value=5.0, step=1.0, on_change=on_change_repitition_penalty) ;        
        beams = st.slider("Beam searches", min_value=1, max_value=10, value=4, step=1, on_change=on_change_beams) ;
        ngrams_norepeat = st.slider("'N' words No-repeat", min_value=1, max_value=5, value=2, step=1, on_change=on_change_ngrams_norepeat) ;
    else:
        temperature = 0.8 ;
        repitition_penalty = 5.0 ;
        ngrams_norepeat = 2 ;
        beams = 4 ;

# Tabs to switch modes of operations
tab1, tab2 = st.tabs(["Text", "PDF"]) ;
with tab1: 
    if 'text' not in st.session_state:
        st.session_state.text = "" ;  
    st_text_area = st.text_area('Paste the text to summarize: ', value=st.session_state.text, height=250) ;
    if 'summary' not in st.session_state:
        st.session_state.summary = "" ;
    # Generate Button Configuration
    if st.button('Generate'):
        st.session_state.text = st_text_area ;
        st_text_area = cleanText(st_text_area) ;
        st.session_state.summary = summarizer.generate_summary(
           		text = st_text_area, limit = max_length,
          		ngs = ngrams_norepeat,
            	lp = length_penalty, 
            	rp = repitition_penalty,
            	temp = temperature,
            	beams = beams
        	) ;

    if st.session_state.summary != "" :
        with st.container(border=True):
            st.subheader("Generated summary:- ") ;
            for summary in st.session_state.summary:
                st.markdown("__" + summary + "__") ;

with tab2:
   # PDF Uploader
    text = "" ;
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"]) ;
    if uploaded_file is not None:
        # Get the filename and create a unique save path
        filename = uploaded_file.name ;
        name, _extension = os.path.splitext(filename) ;
        save_path = f"{base_path}/uploads/{filename}" ;
        # Write the uploaded file to the save path
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer()) ;
        # Inform the user that the file is saved
        f.close() ;
        st.success(f"File '{filename}' successfully uploaded and saved!") ;
        # Display Button Configuration
        if st.button('Display PDF'):
            displayPDF(save_path) ;
        # PDF2Text Configuration
        tab3, tab4 = st.tabs(['Extract Text', 'Generate Summary']) ;
        text = "" ;
        finalSum = "" ;
        summaries = [] ;
        with tab3:
            text = PDF2Text(filename) ;
            print(text) ;
            with st.container(border=True):
                st.subheader("Extracted Text:- ") ;
                st.markdown(text[0]) ;

        with tab4:
            progress_text = "Operation in progress. Please wait !!!" ;
            loadBar = st.progress(0, text=progress_text) ;
            chunks = textToChunks(text[0]) ;
            for index, chunk in enumerate(chunks):
                chunk = cleanText(chunk) ;
                summaries.append(
                    summarizer.generate_summary(
                        text = chunk, limit = max_length,
                        ngs = ngrams_norepeat,
                        lp = length_penalty, 
                        rp = repitition_penalty,
                        temp = temperature,
                        beams = beams
                    )[0] 
                ) ;
                loadBar.progress((index+1)/len(chunks), text=progress_text + f' [ {((index+1)/len(chunks))*100} % ]') ;
            st.markdown("Operation successfully completed !") ;
            finalSum = ' '.join(summaries) ;
            with open(f"{base_path}/output/summary_{name}.txt" , "w") as f:
                f.write(finalSum) ;
            print('Summary stored at /output directory !!') ;
            f.close() ;
            with st.container(border=True):
                with open(f"{base_path}/output/summary_{name}.txt", "r") as f:
                    output = f.readlines() ;
                f.close() ;
                st.subheader("Summarized Text:- ") ;
                st.markdown(output) ;

    else:
        st.info("Please upload a PDF file ! ") ;





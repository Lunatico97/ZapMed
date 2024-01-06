# !!! WARNING: Make sure you read my comments! --> {Diwas}
from extractor import run_sdk, extract_relevant_text, base_path ;
import streamlit as st ;
import base64 ;
import os ; 
import re ;

# Subroutine to extract text from PDF
def getTextFromPDF(file_name):
    pdf_name = f"{file_name}" ;
    name, _extension = os.path.splitext(pdf_name) ;
    zip_name = f"{name}.zip" ;
    # It will run Adobe SDK, which processes pdf and produces output file to output folder
    run_sdk(pdf_name, zip_name) ;
    # It will extract the clean text from the generated output
    final_text = extract_relevant_text(zip_name) ;
    # Open text file in write mode
    text_file = open(f"{base_path}/output/{name}.txt", "w") ;
    # Write content to file
    n = text_file.write(final_text) ;
    if n == len(final_text):
        print(f"File successfully written !! --> /output/{name}.txt") ;
        st.success(f"File successfully written !! --> /output/{name}.txt") ;
    else:
        print("!!! File write {FAILURE} !!!") ;
    text_file.close() ;
    return name ;

# Subroutine to display PDF on Streamlit App
def displayPDF(file):
    # Opening file from file path. this is used to open the file from a website rather than local
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8') ;
    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="950" type="application/pdf"></iframe>' ;
    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True) ;

# Subroutine to break corpus to chunks
def textToChunks(text, max_chunk_size=1024):
    chunks = [] ;
    current_chunk = [] ;
    current_chunk_size = 0 ;
    for sentence in text.split("."):
        sentence_length = len(sentence) + 1 ;
        if current_chunk_size + sentence_length <= max_chunk_size:
            current_chunk.append(sentence + " ") ;
            current_chunk_size += sentence_length ;
        else:
            current_chunk = '.'.join(current_chunk) ;
            chunks.append(current_chunk) ;
            current_chunk = [] ;
            current_chunk.append(sentence + " ") ;
            current_chunk_size = sentence_length ;
    if current_chunk:
        current_chunk = '.'.join(current_chunk) ;
        chunks.append(current_chunk) ;
    return chunks ;

# Subroutine to clean text
def cleanText(text):
    text = str(text) ;
    text = re.sub(r'\[[0-9]*\]', ' ', text) ;
    text = re.sub(r'\s+', ' ', text) ;
    return text ;

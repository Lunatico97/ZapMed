# !!! WARNING: Make sure you read my comments! --> {Diwas}
# Import libraries
import os
import streamlit as st
from extractor import base_path
from summarizer import Summarizer
from chatbot import Chatbot
import matplotlib.pyplot as plt ;
from pdfer import displayPDF, getTextFromPDF, textToChunks, cleanText ;
from analytics import generateBLEU, lexicalRedundancy ;
from word_cloud import filterText, generateWordCloud ;

# PDF2Text Function
def PDF2Text(filename):
    name = getTextFromPDF(filename)
    with open(f"{base_path}/output/{name}.txt", "r") as f:
        text = f.readlines()
        # print(text) ;
    f.close()
    return text


# Page Title Configuration
st.set_page_config(
    layout="wide",
    page_title="ZapMed",
    page_icon="⚡",
)

# Header Texts
st.header("Zap through your medical papers and articles")
st_model_load = st.text("!!!!! WAIT --- Setting up environment !!!!!")

# Initialize summarizer with model card
summarizer = Summarizer(model_card="DiwasDiwas/t5-small-ZapMed")
summarizer.kickstart_model()
st.success("⚡ Are you ready to zap in an instant !? ⚡")
st_model_load.text("")
chatbot = Chatbot()
chatbot.kickstart_model()

# Defaults
if "max_length" not in st.session_state:
    st.session_state.max_length = 100
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.8
if "length_penalty" not in st.session_state:
    st.session_state.length_penalty = 2.0
if "repitition_penalty" not in st.session_state:
    st.session_state.repitition_penalty = 5.0
if "ngrams_norepeat" not in st.session_state:
    st.session_state.ngrams_norepeat = 2
if "beams" not in st.session_state:
    st.session_state.beams = 4


# On-Change Functions
def on_change_max_length():
    st.session_state.max_length = max_length


def on_change_length_penalty():
    st.session_state.length_penalty = length_penalty


def on_change_temperature():
    st.session_state.temperature = temperature


def on_change_repitition_penalty():
    st.session_state.repitition_penalty = repitition_penalty


def on_change_beams():
    st.session_state.beams = beams


def on_change_ngrams_norepeat():
    st.session_state.ngrams_norepeat = ngrams_norepeat


with st.sidebar:
    st.image("images/zapmed.png")
    st.header("Options")
    max_length = st.slider(
        "Generation Length",
        min_value=50,
        max_value=128,
        value=100,
        step=5,
        on_change=on_change_max_length,
    )
    length_penalty = st.slider(
        "Length Penalty",
        min_value=1,
        max_value=10,
        value=2,
        step=1,
        on_change=on_change_length_penalty,
    )
    advanced = st.sidebar.checkbox(label="Advanced Options ")
    if advanced:
        temperature = st.slider(
            "Temperature",
            min_value=0.1,
            max_value=1.5,
            value=0.8,
            step=0.05,
            on_change=on_change_temperature,
        )
        st.markdown("_[Diversity / Randomness]_")
        repitition_penalty = st.slider(
            "Repitition Penalty",
            min_value=1.0,
            max_value=10.0,
            value=5.0,
            step=1.0,
            on_change=on_change_repitition_penalty,
        )
        beams = st.slider(
            "Beam searches",
            min_value=1,
            max_value=10,
            value=4,
            step=1,
            on_change=on_change_beams,
        )
        ngrams_norepeat = st.slider(
            "'N' words No-repeat",
            min_value=1,
            max_value=5,
            value=2,
            step=1,
            on_change=on_change_ngrams_norepeat,
        )
    else:
        temperature = 0.8
        repitition_penalty = 5.0
        ngrams_norepeat = 2
        beams = 4

tab1, tab2 = st.tabs(["Text", "PDF"])
# Tabs to switch modes of operations
with tab1:
    if "text" not in st.session_state:
        st.session_state.text = ""
    if "summary" not in st.session_state:
        st.session_state.summary = ""
    col1, col2 = st.columns(2)
    with col1:
        input_text_box = st.text_area(
            "Input text",
            height=500,
            key="input-text",
        )
        st.session_state.text = input_text_box
    with col2:
        cleaned_text = "" ;
        summary_text_box = st.text_area(
            "Summary text",
            height=500,
            key="summary-text",
            value=" ".join(st.session_state.summary),
        )
        if st.button("Summarize", key="text-summarize"):
            cleaned_text = cleanText(st.session_state.text)
            st.session_state.summary = summarizer.generate_summary(
                text=cleaned_text,
                limit=max_length,
                ngs=ngrams_norepeat,
                lp=length_penalty,
                rp=repitition_penalty,
                temp=temperature,
                beams=beams,
            )
            #st.rerun() ;
        
        if st.session_state.summary != "":
            with st.container(border=True):
                #st.markdown(f"BLEU Score: {generateBLEU(cleaned_text, st.session_state.summary[0])}") ;
                st.markdown(f"Redundancy: {lexicalRedundancy(cleaned_text, st.session_state.summary[0])}") ;
                feed = filterText(st.session_state.summary[0]) ;
                fig, ax = plt.subplots(figsize = (12, 8)) ;
                ax.imshow(generateWordCloud(feed)) ;
                plt.axis("off") ;
                st.pyplot(fig) ;

    if "text_chat_output" not in st.session_state:
        st.session_state.text_chat_output = ""
    text_prompt = st.text_area(
        "Enter chat prompt after pasting text",
        height=100,
    )
    if st.button("Enter", key="text-prompt-enter"):
        if st.session_state.text != "" and text_prompt != "":
            st.session_state.text_chat_output = chatbot.askQuery(
                text_prompt, st.session_state.text
            )
        else:
            st.session_state.text_chat_output = (
                "Error: please provide valid context and prompt"
            )
        print(st.session_state.text_chat_output)
        st.markdown("__" + st.session_state.text_chat_output[0] + "__")
#        if st.session_state.summary != "":
#            with st.container(border=True):
#                st.subheader("Generated summary:- ")
#                for summary in st.session_state.summary:
#                    st.markdown("__" + summary + "__")
#
with tab2:
    col3, col4 = st.columns(2)
    # Add text boxes to each column
    if "pdf_text" not in st.session_state:
        st.session_state.pdf_text = ""
    if "pdf_summary" not in st.session_state:
        st.session_state.pdf_summary = ""
    with col3:
        extracted_text_box = st.text_area(
            "Extracted text",
            height=500,
            key="extracted-text",
            value=st.session_state.pdf_text,
            disabled=True,
        )
        uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
        if uploaded_file is not None:
            # Get the filename and create a unique save path
            filename = uploaded_file.name
            name, _extension = os.path.splitext(filename)
            save_path = f"{base_path}/uploads/{filename}"
            # Write the uploaded file to the save path
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            # Inform the user that the file is saved
            f.close()
            st.success(f"File '{filename}' successfully uploaded and saved!")
            # Display Button Configuration
            if st.button("Display PDF"):
                displayPDF(save_path)
            st.text("Extracting text....")
            text = PDF2Text(filename)
            st.text("Text extracted successfully !!!")
            if st.session_state.pdf_text != text[0]:
                st.session_state.pdf_text = text[0]
                st.rerun()
            # PDF Uploader

        #  context_file = st.file_uploader("Upload context file", type=["pdf"])
        #  if context_file is not None:
        #      # Get the filename and create a unique save path
        #      filename = context_file.name
        #      name, _extension = os.path.splitext(filename)
        #      save_path = f"{base_path}/uploads/{filename}"
        #      # Write the uploaded file to the save path
        #      with open(save_path, "wb") as f:
        #          f.write(context_file.getbuffer())
        #      # Inform the user that the file is saved
        #      f.close()
        #      st.success(f"File '{filename}' successfully uploaded and saved!")
        #      # Display Button Configuration
        #      if st.button("Display PDF"):
        #          displayPDF(save_path)
        #      # PDF2Text Conversion
        #      context = PDF2Text(filename)
        #      st.text_area("Ask anything: ", prompt, height=100)
        #      if st.button("->"):
        #          result = chatbot.askQuery(prompt, context[0])
        #          with st.container(border=True):
        #              st.subheader("ZapMed:- ")
        #              st.markdown(result[0])

        #      with open(f"{base_path}/output/summary_{name}.txt", "r") as f:
        #          output = f.readlines()
        #          f.close()
        #          st.subheader("Summarized Text:- ")
        #          st.markdown(output)

        #  else:
        #      st.info("Please upload a PDF file ! ")

    with col4:
        summary_text_box = st.text_area(
            "Summary Text",
            height=500,
            key="summary-text-pdf",
            value=st.session_state.pdf_summary,
            disabled=True,
        )
        # Generate Button Configuration
        if st.button("Summarize", key="pdf-summarize"):
            progress_text = "Operation in progress. Please wait !!!"
            loadBar = st.progress(0, text=progress_text)
            text = st.session_state.pdf_text
            print(text)
            chunks = textToChunks(text)
            summaries = []
            for index, chunk in enumerate(chunks):
                chunk = cleanText(chunk)
                summaries.append(
                    summarizer.generate_summary(
                        text=chunk,
                        limit=max_length,
                        ngs=ngrams_norepeat,
                        lp=length_penalty,
                        rp=repitition_penalty,
                        temp=temperature,
                        beams=beams,
                    )[0]
                )
                loadBar.progress(
                    (index + 1) / len(chunks),
                    text=progress_text + f" [ {((index+1)/len(chunks))*100} % ]",
                )
            st.markdown("Operation successfully completed !")
            finalSum = " ".join(summaries)
            with open(f"{base_path}/output/summary_{name}.txt", "w") as f:
                f.write(finalSum)
                print("Summary stored at /output directory !!")
            f.close()
            with st.container(border=True):
                with open(f"{base_path}/output/summary_{name}.txt", "r") as f:
                    output = f.readlines()
                f.close()
                summary_output = " ".join(output) ;
                #st.markdown(f"BLEU Score: {generateBLEU(cleaned_text, summary_output)}") ;
                st.markdown(f"Redundancy: {lexicalRedundancy(cleaned_text, summary_output)}") ;
                feed = filterText(summary_output) ;
                fig, ax = plt.subplots(figsize = (12, 8)) ;
                ax.imshow(generateWordCloud(feed)) ;
                plt.axis("off") ;
                st.pyplot(fig) ;

    if "pdf_chat_output" not in st.session_state:
        st.session_state.pdf_chat_output = ""
    pdf_prompt = st.text_area(
        "Enter chat prompt after text extraction is complete",
        height=100,
        key="pdf-chat-prompt",
    )
    if st.button("Enter", key="pdf-prompt-enter"):
        if st.session_state.pdf_text != "" and pdf_prompt != "":
            st.session_state.pdf_chat_output = chatbot.askQuery(
                pdf_prompt, st.session_state.pdf_text
            )
        else:
            st.session_state.pdf_chat_output = (
                "Error: please provide valid context and prompt",
            )
        print(st.session_state.pdf_chat_output)
        st.markdown("__" + st.session_state.pdf_chat_output[0] + "__")
        #    # PDF Uploader
        #    text = ""
        #    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
        #    if uploaded_file is not None:
        #        # Get the filename and create a unique save path
        #        filename = uploaded_file.name
        #        name, _extension = os.path.splitext(filename)
        #        save_path = f"{base_path}/uploads/{filename}"
        #        # Write the uploaded file to the save path
        #        with open(save_path, "wb") as f:
        #            f.write(uploaded_file.getbuffer())
        #        # Inform the user that the file is saved
        #        f.close()
        #        st.success(f"File '{filename}' successfully uploaded and saved!")
        #        # Display Button Configuration
        #        if st.button("Display PDF"):
        #            displayPDF(save_path)
        #        # PDF2Text Configuration
        #        tab3, tab4, tab5 = st.tabs(["Extract Text", "Chat", "Generate Summary"])
        #        text = ""
        #
        #
        #        with tab3:
        #            text = PDF2Text(filename)
        #            if len(text) == 0:
        #                st.markdown(
        #                    "## No text was extracted, please upload a pdf with proper text"
        #                )
        #            else:
        #                with st.container(border=True):
        #                    st.subheader("Extracted Text:- ")
        #                    st.markdown(text[0])
        #        with tab4:
        #            prompt = ""
        #            chatbot = Chatbot()
        #            chatbot.kickstart_model()
        #            if st.button("Start Chatting"):
        #                print(text)
        #                if len(text) != 0:
        #                    context = text[0]
        #                    st.text_area("Ask anything: ", prompt, height=100)
        #                    if st.button("Enter"):
        #                        result = chatbot.askQuery(prompt, context[0])
        #                        print("Chat reply: ", result)
        #                        with st.container(border=True):
        #                            st.subheader("ZapMed:- ")
        #                            st.markdown(result[0])
        #
        #        with tab5:
        #            if st.button("Start Generating"):
        #                progress_text = "Operation in progress. Please wait !!!"
        #                loadBar = st.progress(0, text=progress_text)
        #                chunks = textToChunks(text[0])
        #                for index, chunk in enumerate(chunks):
        #                    chunk = cleanText(chunk)
        #                    summaries.append(
        #                        summarizer.generate_summary(
        #                            text=chunk,
        #                            limit=max_length,
        #                            ngs=ngrams_norepeat,
        #                            lp=length_penalty,
        #                            rp=repitition_penalty,
        #                            temp=temperature,
        #                            beams=beams,
        #                        )[0]
        #                    )
        #                    loadBar.progress(
        #                        (index + 1) / len(chunks),
        #                        text=progress_text + f" [ {((index+1)/len(chunks))*100} % ]",
        #                    )
        #                st.markdown("Operation successfully completed !")
        #                finalSum = " ".join(summaries)
        #                with open(f"{base_path}/output/summary_{name}.txt", "w") as f:
        #                    f.write(finalSum)
        #                print("Summary stored at /output directory !!")
        #                f.close()
        #                with st.container(border=True):
        #                    with open(f"{base_path}/output/summary_{name}.txt", "r") as f:
        #                        output = f.readlines()
        #                    f.close()
        #                    st.subheader("Summarized Text:- ")
        #                    st.markdown(output)
        #
        #    else:
        #        st.info("Please upload a PDF file ! ")
        #
        # with tab03:
        #    # PDF Uploader
        #    text = ""
        #    prompt = ""
        #    chatbot = Chatbot()
        #    chatbot.kickstart_model()
        #    context_file = st.file_uploader("Upload context file", type=["pdf"])
        #    if context_file is not None:
        #        # Get the filename and create a unique save path
        #        filename = context_file.name
        #        name, _extension = os.path.splitext(filename)
        #        save_path = f"{base_path}/uploads/{filename}"
        #        # Write the uploaded file to the save path
        #        with open(save_path, "wb") as f:
        #            f.write(context_file.getbuffer())
        #        # Inform the user that the file is saved
        #        f.close()
        #        st.success(f"File '{filename}' successfully uploaded and saved!")
        #        # Display Button Configuration
        #        if st.button("Display PDF"):
        #            displayPDF(save_path)
        #        # PDF2Text Conversion
        #        context = PDF2Text(filename)
        #        st.text_area("Ask anything: ", prompt, height=100)
        #        if st.button("->"):
        #            result = chatbot.askQuery(prompt, context[0])
        #            with st.container(border=True):
        #                st.subheader("ZapMed:- ")
        #                st.markdown(result[0])
        #
        #        with open(f"{base_path}/output/summary_{name}.txt", "r") as f:
        #            output = f.readlines()
        #            f.close()
        #            st.subheader("Summarized Text:- ")
        #            st.markdown(output)
        #
        #    else:
        #        st.info("Please upload a PDF file ! ")

import streamlit as st
from pypdf import PdfReader
import asyncio
import agent
import os

# Page Config
st.set_page_config(page_title="Study Buddy", page_icon="📚", layout="wide")

st.title("📚 Study Notes Summarizer & Quiz Generator")
st.markdown("Upload your study notes (PDF) to get a summary and test your knowledge!")

# Initialize Session State
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "quiz" not in st.session_state:
    st.session_state.quiz = ""

# File Uploader
uploaded_file = st.file_uploader("Upload your Study Notes (PDF)", type="pdf")

def extract_text(pdf_file):
    """Extracts text from the uploaded PDF file."""
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

if uploaded_file is not None:
    # Only extract if we haven't already or if it's a new file (simplified logic: just extract)
    # Ideally we'd check file ID, but for now extracting is fast enough for typical notes.
    text = extract_text(uploaded_file)
    
    if text:
        st.session_state.pdf_text = text
        st.success(f"✅ PDF uploaded successfully! ({len(text)} characters extracted)")
        
        # Summarize Button
        if st.button("📝 Summarize Notes", type="primary"):
            with st.spinner("Analyzing text and generating summary..."):
                try:
                    # async call to agent
                    summary = asyncio.run(agent.summarize_text(st.session_state.pdf_text))
                    st.session_state.summary = summary
                    # Reset quiz when new summary is generated to keep flow logical
                    st.session_state.quiz = "" 
                except Exception as e:
                    st.error(f"An error occurred during summarization: {e}")

    else:
        st.warning("Could not extract text from the PDF. Please try another file.")

# Display Summary
if st.session_state.summary:
    st.divider()
    st.subheader("📌 Summary")
    st.markdown(st.session_state.summary)
    
    st.divider()
    st.subheader("🧠 Test Your Knowledge")
    
    # Quiz Button (Only appears after summary)
    if st.button("❓ Create Quiz"):
        with st.spinner("Generating questions based on original text..."):
            try:
                # Generates quiz from ORIGINAL text as requested
                quiz = asyncio.run(agent.generate_quiz(st.session_state.pdf_text))
                st.session_state.quiz = quiz
            except Exception as e:
                st.error(f"An error occurred during quiz generation: {e}")

# Display Quiz
if st.session_state.quiz:
    st.markdown("---")
    st.subheader("📝 Quiz")
    st.markdown(st.session_state.quiz)

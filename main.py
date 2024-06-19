# app.py
import streamlit as st
from rag import qa_chain

# Streamlit app
st.title("RAG Chatbot with Neo4j and LangChain")

# User input
question = st.text_input("Enter your question:")

if question:
    # Get the answer using LangChain
    answer = qa_chain({"query": question})

    # Display the answer
    st.write(f"**Answer:** {answer['result']}")
# WORKING FILE
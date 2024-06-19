# rag.py
import os
import openai
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from connections import driver, run_cypher_query

# Set OpenAI API key
openai_api_key = 'sk-proj-sbsW3pa4EZnrHQuzhO9cT3BlbkFJtHwUQ5thzJ68uf0Vg4QU'  # Replace with your OpenAI API key
openai.api_key = openai_api_key

# Initialize OpenAI Embeddings
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Function to retrieve paragraphs from Neo4j
def retrieve_paragraphs(driver):
    query = """
    MATCH (p:Paragraph:Embeddable)
    RETURN p.text AS text
    """
    paragraphs = run_cypher_query(driver, query)
    return [record['text'] for record in paragraphs]

# Retrieve paragraphs and store embeddings
paragraphs = retrieve_paragraphs(driver)
documents = [{"text": text} for text in paragraphs]
vectorstore = FAISS.from_texts([doc["text"] for doc in documents], embeddings)

# Initialize OpenAI LLM
llm = OpenAI(openai_api_key=openai_api_key)

# Set up LangChain RetrievalQA
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever(), chain_type="stuff")

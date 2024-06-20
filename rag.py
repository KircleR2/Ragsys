# rag.py
import openai
import logging
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from connections import driver, run_cypher_query
from cachetools import cached, TTLCache

# Set OpenAI API key
openai_api_key = ''  # Add your OpenAI API key here
openai.api_key = openai_api_key

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI Embeddings
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Function to decide email type based on user query
def decide_email_type(query):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that decides the type of email based on user queries."},
            {"role": "user", "content": f"Determine the email type (Trial Onboarding, Follow Up, Promotion) for the following query: {query}"}
        ]
    )
    email_type = response.choices[0].message.content.strip()
    return email_type

# Function to retrieve verbal identity and descriptions with relationships from Neo4j
def retrieve_verbal_identity_and_descriptions(driver):
    query = """
    MATCH (v:VerbalIdentity)
    RETURN v.text AS text, v.description AS description
    """
    logger.info(f"Executing Cypher query to retrieve verbal identity: {query}")
    verbal_identity_records = run_cypher_query(driver, query)
    logger.info(f"Query results: {verbal_identity_records}")

    if verbal_identity_records:
        verbal_identity = verbal_identity_records[0]['text']
        descriptions = [record['description'] for record in verbal_identity_records if 'description' in record]

        relationship_query = """
        MATCH (v:VerbalIdentity)-[r]->(related)
        RETURN type(r) AS relationship, related.text AS related_text
        """
        logger.info(f"Executing Cypher query to retrieve relationships: {relationship_query}")
        relationship_records = run_cypher_query(driver, relationship_query)
        logger.info(f"Relationship query results: {relationship_records}")

        relationships = [f"{record['relationship']}: {record['related_text']}" for record in relationship_records]
        return verbal_identity, descriptions, relationships
    return "No verbal identity defined.", [], []

# Placeholder function to simulate learning from feedback
def learn_from_feedback(feedback):
    # Implement your machine learning model here
    pass

# Initialize cache with a TTL (time to live) of 10 minutes and max size of 100 entries
cache = TTLCache(maxsize=100, ttl=600)

# Function to preprocess Cypher query
def preprocess_query(query):
    # Example preprocessing: remove extra spaces, standardize formatting, etc.
    query = query.strip()
    # Add other preprocessing steps as needed
    return query

# Function to retrieve paragraphs from Neo4j
@cached(cache)
def retrieve_paragraphs(driver):
    raw_query = """
    MATCH (p:Paragraph:Embeddable)
    RETURN p.text AS text
    """
    query = preprocess_query(raw_query)
    logger.info(f"Executing Cypher query to retrieve paragraphs: {query}")
    paragraphs = run_cypher_query(driver, query)
    logger.info(f"Paragraph query results: {paragraphs}")
    return [record['text'] for record in paragraphs]

# Email templates
email_templates = {
    "Trial Onboarding": "Welcome to our trial! We're excited to have you. Here are some resources to get started...",
    "Follow Up": "We noticed you haven't completed your registration. Here's a quick guide to help you finish...",
    "Promotion": "Great news! We're offering a special promotion just for you. Don't miss out on this limited-time offer..."
}

# Function to generate email content
def generate_email_content(email_type, qa_chain, query, verbal_identity, descriptions, relationships):
    base_content = email_templates.get(email_type, "Default email content")
    answer = qa_chain({"query": query})
    initial_content = f"{base_content}\n\n{answer['result']}"
    final_content = final_review(initial_content, verbal_identity, descriptions, relationships)
    return final_content

# Function for final review by secondary LLM
def final_review(content, verbal_identity, descriptions, relationships):
    description_text = "\n\n".join(descriptions)
    relationship_text = "\n\n".join(relationships)
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that reviews email content for quality and consistency."},
            {"role": "user", "content": f"Review the following email content for quality and consistency based on the verbal identity, descriptions, and relationships:\n\nVerbal Identity:\n{verbal_identity}\n\nDescriptions:\n{description_text}\n\nRelationships:\n{relationship_text}\n\nEmail Content:\n{content}"}
        ]
    )
    final_content = response.choices[0].message.content.strip()
    return final_content

# Retrieve paragraphs and store embeddings
paragraphs = retrieve_paragraphs(driver)
documents = [{"text": text} for text in paragraphs]
vectorstore = FAISS.from_texts([doc["text"] for doc in documents], embeddings)

# Initialize OpenAI LLM
llm = OpenAI(openai_api_key=openai_api_key)

# Set up LangChain RetrievalQA
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever(), chain_type="stuff")
#WORKING FILE

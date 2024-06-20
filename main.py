# app.py
import streamlit as st
from rag import qa_chain, generate_email_content, decide_email_type, learn_from_feedback, retrieve_verbal_identity_and_descriptions, driver

# Streamlit app
st.title("RAG Chatbot with Neo4j and LangChain")

# User input
question = st.text_input("Enter your query:")

if question:
    # Automate email type decision
    email_type = decide_email_type(question)

    # Retrieve verbal identity and descriptions with relationships
    verbal_identity, descriptions, relationships = retrieve_verbal_identity_and_descriptions(driver)

    # Display the chosen email type
    st.write(f"**Decided Email Type:** {email_type}")

    # Generate the email content
    email_content = generate_email_content(email_type, qa_chain, question, verbal_identity, descriptions, relationships)

    # Display the email content
    st.write(f"**Generated Email:**\n\n{email_content}")

    # Feedback loop
    feedback = st.text_area("Provide feedback or edits:", email_content)

    if st.button("Submit Feedback"):
        st.write("Thank you for your feedback!")
        learn_from_feedback(feedback)
        # In a real application, you would process and store the feedback
# WORKING FILE

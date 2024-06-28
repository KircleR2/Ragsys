# RAG Chatbot with Neo4j and LangChain

This repository contains the code for a RAG (Retrieval-Augmented Generation) Chatbot application that generates email content based on user queries and selections. It leverages a combination of a knowledge base stored in a Neo4j database and the language generation capabilities of OpenAI's language models. The application is built using Streamlit, which provides an interactive web interface for users.

## Overview

The RAG Chatbot application is designed to generate email content in accordance with a brand's verbal identity. It retrieves relevant paragraphs, verbal identities, descriptions, and relationships from a Neo4j database and uses OpenAI's language models to create contextually relevant email content. The application also incorporates feedback mechanisms to continuously improve the generated content.

## Features

- **Automated Email Type Decision**: The LLM decides the email type based on user queries.
- **Verbal Identity Adherence**: The generated emails adhere to the brand's verbal identity, incorporating descriptions and relationships defined in the database.
- **Real-time Feedback Loop**: Users can provide feedback on the generated email content to improve future outputs.
- **Caching for Efficiency**: The application uses caching mechanisms to store frequently accessed data and reduce query times.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/KircleR2/Ragsys.git
    cd rag-chatbot
    ```

2. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up your Neo4j database**:
    - Ensure you have a Neo4j database running.
    - Update the `connections.py` file with your Neo4j connection details.
    - Restore the Neo4j dump file:
        1. Place the dump file (e.g., `rag_Sample_Angel.dump`) in a known location.
        2. Start the Neo4j server.
        3. Use the following commands to restore the database:
            ```sh
            neo4j stop
            neo4j-admin load --from=/path/to/rag_Sample_Angel.dump --database=neo4j --force
            neo4j start
            ```

4. **Set your OpenAI API key**:
    - Add your OpenAI API key to the `rag.py` file:
    ```python
    openai_api_key = 'your-openai-api-key'
    openai.api_key = openai_api_key
    ```

## Usage

1. **Start the Streamlit app**:
    ```sh
    streamlit run app.py
    ```

2. **Interact with the application**:
    - Open your web browser and go to `http://localhost:8501`.
    - Enter your query in the input field.
    - View the generated email content based on the selected email type and provided query.
    - Provide feedback on the generated content to help improve future outputs.

## Code Structure

- **`app.py`**: The main entry point for the Streamlit application. It handles user input, retrieves verbal identity and descriptions, and displays the generated email content.
- **`rag.py`**: Contains the core logic for interacting with the Neo4j database, deciding the email type, and generating email content based on the retrieved data and OpenAI's language models.
- **`connections.py`**: Manages the connection to the Neo4j database and executes Cypher queries.

## Example

Here’s an example of how the generated email might look:

```plaintext
Decided Email Type: The email type for this query is Promotion.

Generated Email:

Subject: Celebrating [Employee's Name]: Our Newly Promoted Data Analyst!

Dear [Recipient's Name],

I hope this message finds you well.

I am delighted to announce the promotion of [Employee's Name] to the position of Data Analyst at [Company's Name]. This well-deserved promotion is a testament to [Employee's Name]'s dedication, expertise, and exceptional performance in their role.

[Employee's Name] has consistently demonstrated a keen analytical mind and a strong capacity for turning data into actionable insights. Their contributions have been pivotal in driving our projects forward and ensuring our decision-making processes are underpinned by solid data.

Please join me in congratulating [Employee's Name] on this significant achievement. We are confident that in their new role, they will continue to excel and bring even greater value to our team and clients.

Best regards,

[Your Full Name]
[Your Job Title]
[Your Contact Information]
[Company's Name]

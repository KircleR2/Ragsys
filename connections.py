# connections.py
import os
from neo4j import GraphDatabase

# Neo4j connection details
NEO4J_URI = "neo4j+s://0b0c911c.databases.neo4j.io"  
NEO4J_USER = "neo4j"                 
NEO4J_PASSWORD = "RGZW9GaL2VDISdVOfylZJo-E7uLca5vGKjQVcE0ehcQ"          

# Function to connect to Neo4j
def get_neo4j_connection(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver

# Function to execute a Cypher query
def run_cypher_query(driver, query):
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]

# Initialize Neo4j connection
driver = get_neo4j_connection(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

# connections.py
from neo4j import GraphDatabase

# Neo4j connection details
NEO4J_URI = ""  
NEO4J_USER = ""                 
NEO4J_PASSWORD = ""          

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
# WORKING FILE

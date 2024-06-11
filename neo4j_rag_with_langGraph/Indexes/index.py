import os
import openai
from langchain.vectorstores import Neo4jVector
from langchain_openai import OpenAIEmbeddings
#from neo4j import GraphDatabase

openai.api_key  = os.environ.get("OPENAI_API_KEY")
EMBEDDING_MODEL = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))

AURA_CONNECTION_URI = os.environ.get('AURA_CONNECTION_URI')
AURA_USERNAME = os.environ.get('AURA_USERNAME')
AURA_PASSWORD = os.environ.get('AURA_PASSWORD')

def get_neo4j_vector_index():   

    ''' Create title vector and Instantiate Neo4j vector from graph'''
    
    neo4j_vector_index = Neo4jVector.from_existing_graph(
        embedding = EMBEDDING_MODEL,
        url = AURA_CONNECTION_URI,
        username = AURA_USERNAME,
        password = AURA_PASSWORD,
        index_name = 'title_abstract_vector',
        node_label = 'Article',
        text_node_properties = ['title', 'abstract'],
        embedding_node_property = 'embedding_vectors',
    )
    return neo4j_vector_index

def get_neo4j_title_vector_index(): 
    
    '''Create title vector and Instantiate Neo4j vector from graph'''
    
    neo4j_title_vector_index = Neo4jVector.from_existing_graph(
        embedding = EMBEDDING_MODEL,
        url = AURA_CONNECTION_URI,
        username = AURA_USERNAME,
        password = AURA_PASSWORD,
        index_name = 'title_vector',
        node_label = 'Title',
        text_node_properties = ['text'],
        embedding_node_property = 'embedding_vectors',
    )
    return neo4j_title_vector_index

def get_neo4j_abstract_vector_index(): 
    
    ''' Create title vector and Instantiate Neo4j vector from graph'''
    
    neo4j_abstract_vector_index = Neo4jVector.from_existing_graph(
        embedding = EMBEDDING_MODEL,
        url = AURA_CONNECTION_URI,
        username = AURA_USERNAME,
        password = AURA_PASSWORD,
        index_name = 'abstract_vector',
        node_label = 'Abstract',
        text_node_properties = ['text'],
        embedding_node_property = 'embedding_vectors',
    )
    return neo4j_abstract_vector_index

def get_neo4j_topic_vector_index(): 
    
    '''Create title vector and Instantiate Neo4j vector from graph'''
    
    neo4j_topic_vector_index = Neo4jVector.from_existing_graph(
        embedding = EMBEDDING_MODEL,
        url = AURA_CONNECTION_URI,
        username = AURA_USERNAME,
        password = AURA_PASSWORD,
        index_name = 'topic_vector',
        node_label = 'Topic',
        text_node_properties = ['text'],
        embedding_node_property = 'embedding_vectors',
    )
    return neo4j_topic_vector_index
# Import Python Libraries
import os
import openai
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA

# Import Custom Libraries
from Indexes import index

llm = ChatOpenAI(
    model="gpt-3.5-turbo", 
    temperature=0,
    api_key=os.environ.get("OPENAI_API_KEY"),
)

vector_index = index.get_neo4j_vector_index()

def get_vector_graph_chain():
    '''Create a Neo4j Retrieval QA Chain. Returns top K most relevant articles'''
    vector_graph_chain = RetrievalQA.from_chain_type(
        llm, 
        chain_type="stuff", 
        retriever = vector_index.as_retriever(search_kwargs={'k':3}), 
        verbose=True,
        return_source_documents=True,
    )
    return vector_graph_chain
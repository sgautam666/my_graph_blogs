# Import Python Libraries
import os
import openai
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA, GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph

# Import Custom Libraries
from Prompts.prompt_template import create_few_shot_prompt, create_few_shot_prompt_with_context
from Graph.state import GraphState

# Instantiate a Neo4j graph
graph = Neo4jGraph(
    url=os.environ.get('AURA_CONNECTION_URI'),
    username=os.environ.get('AURA_USERNAME'),
    password=os.environ.get('AURA_PASSWORD')
)

# Instantiate a openai model
llm = ChatOpenAI(
    model="gpt-3.5-turbo", 
    temperature=0,
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_graph_qa_chain(state: GraphState):
    
    """Create a Neo4j Graph Cypher QA Chain"""
    
    prompt = state["prompt"]
    
    graph_qa_chain = GraphCypherQAChain.from_llm(
            cypher_llm = llm, #should use gpt-4 for production
            qa_llm = llm,
            validate_cypher= True,
            graph=graph,
            verbose=True,
            cypher_prompt = prompt,
            # return_intermediate_steps = True,
            return_direct = True,
        )
    return graph_qa_chain

def get_graph_qa_chain_with_context(state: GraphState):
    
    """Create a Neo4j Graph Cypher QA Chain. Using this as GraphState so it can access state['prompt']"""
    
    prompt_with_context = state["prompt_with_context"] 
    
    graph_qa_chain = GraphCypherQAChain.from_llm(
            cypher_llm = llm, #should use gpt-4 for production
            qa_llm = llm,
            validate_cypher= True,
            graph=graph,
            verbose=False,
            cypher_prompt = prompt_with_context,
            # return_intermediate_steps = True,
            return_direct = True,
        )
    return graph_qa_chain
from chains.graph_qa_chain import _get_graph_qa_chain
from graph.state import GraphState
from langchain.agents import tool

graph_qa_chain = _get_graph_qa_chain()


# Define tools for the agent
@tool
def graph_qa(state: GraphState):
    
    ''' Returns a dict with keys: 
    dict_keys(['query', 'result']) 
    '''
    question = state["question"]
    
    result = graph_qa_chain.invoke(
        {
            #"context": graph.schema, 
            "query": question,
        },
    )
    return {"result": result, "question":question}
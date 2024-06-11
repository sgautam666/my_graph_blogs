from chains.vector_graph_chain import _get_vector_graph_chain
from graph.state import GraphState
from langchain.agents import tool

vector_graph_chain = _get_vector_graph_chain()


# Define tools for the agent
@tool
def vector_search(state: GraphState):
    
    ''' Returns a dict with keys: 
    dict_keys(['query', 'result', 'source_documents']) 
    '''
    question = state["question"]
    
    chain_result = vector_graph_chain.invoke({
        "query": question},
    )
    results = []
    for doc in chain_result['source_documents']: 
        temp_dict = {}
        formatted_doc = doc.page_content.strip().split('\n')

        for line in formatted_doc:
            key, value = line.split(': ', 1)
            if key == 'title':
                temp_dict['title'] = value
                temp_dict['article_id'] = doc.metadata['article_id']
                results.append(temp_dict)
        
    return {"result": results, "question":question}
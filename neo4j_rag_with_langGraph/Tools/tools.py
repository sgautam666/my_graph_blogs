# Replace with the actual URI, username, and password
from neo4j import GraphDatabase

neo4j_url = os.environ.get('AURA_CONNECTION_URI')
neo4j_user = os.environ.get('AURA_USERNAME')
neo4j_pwd = os.environ.get('AURA_PASSWORD')

driver = GraphDatabase.driver(AURA_CONNECTION_URI, auth=(AURA_USERNAME, AURA_PASSWORD))

"""These tools are not currently used, but may be used when implementing agents"""

# Define tools for the agent
@tool
def vector_search_tool(question):
    
    ''' Returns a dict with keys: 
    dict_keys(['query', 'result', 'source_documents']) 
    '''
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
        
    return results

@tool
def graph_query_tool(query_text):
    ''' Call directly to the graph with input cypher statements'''
    with driver.session() as session:
        result = session.run(query_text)
        return [record.data() for record in result]

@tool
def graph_qa_tool(question):
    
    ''' Returns a dict with keys: 
    dict_keys(['query', 'result']) 
    '''
    result = graph_qa_chain.invoke(
        {
            #"context": graph.schema, 
            "query": question,
        },
    )
    return result
# Import Python Libraries
from dotenv import load_dotenv
from langgraph.graph import END, StateGraph


# Import Custom Libraries
from Chains.router import question_router
from Graph.state import GraphState
from Graph.labels import DECOMPOSER, VECTOR_SEARCH, GRAPH_QA, GRAPH_QA_WITH_CONTEXT, PROMPT_TEMPLATE, PROMPT_TEMPLATE_WITH_CONTEXT
from Graph.nodes import decomposer, vector_search, graph_qa, graph_qa_with_context, prompt_template, prompt_template_with_context


load_dotenv()

def route_question(state: GraphState):
    print("---ROUTE QUESTION---")
    question = state["question"]
    source = question_router.invoke({"question": question})
    if source.datasource == "vector search":
        print("---ROUTE QUESTION TO VECTOR SEARCH---")
        return "decomposer"
    elif source.datasource == "graph query":
        print("---ROUTE QUESTION TO GRAPH QA---")
        return "prompt_template"
    

workflow = StateGraph(GraphState)

# Nodes for graph qa
workflow.add_node(PROMPT_TEMPLATE, prompt_template)
workflow.add_node(GRAPH_QA, graph_qa)

# Nodes for graph qa with vector search
workflow.add_node(DECOMPOSER, decomposer)
workflow.add_node(VECTOR_SEARCH, vector_search)
workflow.add_node(PROMPT_TEMPLATE_WITH_CONTEXT, prompt_template_with_context)
workflow.add_node(GRAPH_QA_WITH_CONTEXT, graph_qa_with_context)

# Set conditional entry point for vector search or graph qa
workflow.set_conditional_entry_point(
    route_question,
    {
        'decomposer': DECOMPOSER, # vector search
        'prompt_template': PROMPT_TEMPLATE # for graph qa
    },
)

# Edges for graph qa with vector search
workflow.add_edge(DECOMPOSER, VECTOR_SEARCH)
workflow.add_edge(VECTOR_SEARCH, PROMPT_TEMPLATE_WITH_CONTEXT)
workflow.add_edge(PROMPT_TEMPLATE_WITH_CONTEXT, GRAPH_QA_WITH_CONTEXT)
workflow.add_edge(GRAPH_QA_WITH_CONTEXT, END)

# Edges for graph qa
workflow.add_edge(PROMPT_TEMPLATE, GRAPH_QA)
workflow.add_edge(GRAPH_QA, END)

app = workflow.compile()

#app.get_graph().draw_mermaid_png(output_file_path="graph.png")
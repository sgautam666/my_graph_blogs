from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["vector search", "graph query"] = Field(
        ...,
        description="Given a user question choose to route it to vectorstore or graphdb.",
    )
    
llm = ChatOpenAI(temperature=0)
structured_llm_router = llm.with_structured_output(RouteQuery)

system = """You are an expert at routing a user question to perform vector search or graph query. 
The vector store contains documents related article title, abstracts and topics. Here are three routing situations:
If the user question is about similarity search, perform vector search. The user query may include term like similar, related, relvant, identitical, closest etc to suggest vector search. For all else, use graph query.

Example questions of Vector Search Case: 
    Find articles about photosynthesis
    Find similar articles that is about oxidative stress
    
Example questions of Graph DB Query: 
    MATCH (n:Article) RETURN COUNT(n)
    MATCH (n:Article) RETURN n.title

Example questions of Graph QA Chain: 
    Find articles published in a specific year and return it's title, authors
    Find authors from the institutions who are located in a specific country, e.g Japan
"""

route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}")
    ]
)

question_router = route_prompt | structured_llm_router
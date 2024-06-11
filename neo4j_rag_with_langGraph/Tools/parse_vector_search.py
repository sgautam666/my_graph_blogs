# Import Python Libraries
from pydantic import BaseModel
from typing import List
import re

# Import Custom Libraries
from Graph.state import GraphState

class Metadata(BaseModel):    
    topics: str
    article_id: str

class DocumentModel(BaseModel):
    page_content: str
    metadata: Metadata

    def extract_title(self) -> str:
        # Extract the title from page_content
        match = re.search(r'title: (.+)', self.page_content)
        if match:
            return match.group(1)
        return ""

class ResultModel(BaseModel):
    documents: List[DocumentModel]
    

def create_context(state: GraphState):
    """Originally designed to be a node, but not used as node anymore, merged to vector search step"""
    chain_result = state["documents"]
    question = state["question"]

    # Convert the result to a list of DocumentModel instances
    documents = [DocumentModel(**doc.dict()) for doc in chain_result['source_documents']]
    extracted_data = [{"title": doc.extract_title(), "article_id": doc.metadata.article_id} for doc in documents]
    article_ids = [("article_id", doc.metadata.article_id) for doc in documents]
    
    return {"article_ids": article_ids, "question":question, "subqueries": queries}
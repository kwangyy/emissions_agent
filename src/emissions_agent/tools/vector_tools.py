from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import json
from pathlib import Path
from .vector_manager import get_vector_manager

class UpsertInput(BaseModel):
    """Input schema for Upsert tool."""
    collection_name: str = Field(..., description="Name of the vector collection")
    documents: str = Field(..., description="JSON string of documents to upsert")

class UpsertTool(BaseTool):
    name: str = "upsert"
    description: str = "Insert or update documents in vector store"
    args_schema: Type[BaseModel] = UpsertInput

    def _run(self, collection_name: str, documents: str) -> str:
        try:
            docs = json.loads(documents)
            vector_manager = get_vector_manager()
            result = vector_manager.upsert_documents(collection_name, docs)
            return result
        except Exception as e:
            return f"Error upserting documents: {str(e)}"

class QueryInput(BaseModel):
    """Input schema for Query tool."""
    collection_name: str = Field(..., description="Name of the vector collection")
    query_text: str = Field(..., description="Text to search for")

class QueryTool(BaseTool):
    name: str = "query"
    description: str = "Query vector store with text"
    args_schema: Type[BaseModel] = QueryInput

    def _run(self, collection_name: str, query_text: str) -> str:
        try:
            vector_manager = get_vector_manager()
            results = vector_manager.query_collection(collection_name, query_text)
            return json.dumps(results, indent=2)
        except Exception as e:
            return f"Error querying collection: {str(e)}"

class SimilaritySearchInput(BaseModel):
    """Input schema for SimilaritySearch tool."""
    collection_name: str = Field(..., description="Name of the vector collection")
    query_text: str = Field(..., description="Text to search for")
    top_k: int = Field(default=5, description="Number of results to return")

class SimilaritySearchTool(BaseTool):
    name: str = "similarity_search"
    description: str = "Perform similarity search in vector store"
    args_schema: Type[BaseModel] = SimilaritySearchInput

    def _run(self, collection_name: str, query_text: str, top_k: int = 5) -> str:
        try:
            vector_manager = get_vector_manager()
            results = vector_manager.similarity_search(collection_name, query_text, top_k)
            return json.dumps(results, indent=2)
        except Exception as e:
            return f"Error performing similarity search: {str(e)}"

class RetrieveTopKWithSpansInput(BaseModel):
    """Input schema for RetrieveTopKWithSpans tool."""
    collection_name: str = Field(..., description="Name of the vector collection")
    query_text: str = Field(..., description="Text to search for")
    top_k: int = Field(default=5, description="Number of results to return")

class RetrieveTopKWithSpansTool(BaseTool):
    name: str = "retrieve_topk_with_spans"
    description: str = "Retrieve top K documents with text spans for citation"
    args_schema: Type[BaseModel] = RetrieveTopKWithSpansInput

    def _run(self, collection_name: str, query_text: str, top_k: int = 5) -> str:
        try:
            vector_manager = get_vector_manager()
            results = vector_manager.retrieve_with_spans(collection_name, query_text, top_k)
            return json.dumps(results, indent=2)
        except Exception as e:
            return f"Error retrieving documents with spans: {str(e)}"

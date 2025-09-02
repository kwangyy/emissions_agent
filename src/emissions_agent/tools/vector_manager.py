"""
Vector database manager using ChromaDB for document storage and retrieval.
"""

import chromadb
from chromadb.config import Settings
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
import hashlib

class VectorManager:
    """Manages ChromaDB collections for document storage and retrieval."""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize ChromaDB client with persistence."""
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collections = {}
    
    def get_or_create_collection(self, collection_name: str):
        """Get existing collection or create new one."""
        if collection_name not in self.collections:
            try:
                self.collections[collection_name] = self.client.get_collection(collection_name)
            except:
                self.collections[collection_name] = self.client.create_collection(collection_name)
        return self.collections[collection_name]
    
    def upsert_documents(self, collection_name: str, documents: List[Dict[str, Any]]) -> str:
        """Insert or update documents in a collection."""
        collection = self.get_or_create_collection(collection_name)
        
        ids = []
        texts = []
        metadatas = []
        
        for doc in documents:
            # Generate unique ID if not provided
            doc_id = doc.get('id', hashlib.md5(doc['text'].encode()).hexdigest())
            ids.append(doc_id)
            texts.append(doc['text'])
            metadatas.append(doc.get('metadata', {}))
        
        collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )
        
        return f"Upserted {len(documents)} documents to collection '{collection_name}'"
    
    def query_collection(self, collection_name: str, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Query a collection with text."""
        collection = self.get_or_create_collection(collection_name)
        
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'id': results['ids'][0][i],
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None
            })
        
        return formatted_results
    
    def similarity_search(self, collection_name: str, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Perform similarity search in a collection."""
        return self.query_collection(collection_name, query_text, top_k)
    
    def retrieve_with_spans(self, collection_name: str, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve documents with highlighted spans for citation."""
        results = self.similarity_search(collection_name, query_text, top_k)
        
        # Add span highlighting (simple keyword highlighting for now)
        for result in results:
            text = result['text']
            # Simple span highlighting - in a real implementation, you'd use more sophisticated NLP
            highlighted_text = text.replace(query_text, f"**{query_text}**")
            result['highlighted_text'] = highlighted_text
            result['spans'] = [{'start': text.find(query_text), 'end': text.find(query_text) + len(query_text)}]
        
        return results

# Global vector manager instance
_vector_manager = None

def get_vector_manager() -> VectorManager:
    """Get or create the global vector manager instance."""
    global _vector_manager
    if _vector_manager is None:
        _vector_manager = VectorManager()
    return _vector_manager

"""
Singleton tool registry to avoid recreating tool instances.
"""

from typing import Dict, Any
from .data_tools import (
    LoadEmissionsDataTool, 
    LoadKnowledgeBaseTool, 
    AnalyzeEmissionsTool, 
    CompareEmissionsTool, 
    GetDataInfoTool,
    CreateVectorCollectionsTool
)
from .vector_tools import UpsertTool, QueryTool, SimilaritySearchTool, RetrieveTopKWithSpansTool
from .reporting_tools import WriteMDTool, WriteFileTool, SaveQuestionReportTool

class ToolRegistry:
    """Singleton registry for tool instances."""
    
    _instance = None
    _tools: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
            cls._instance._initialize_tools()
        return cls._instance
    
    def _initialize_tools(self):
        """Initialize all tool instances once."""
        self._tools = {
            # Data tools
            'load_emissions_data': LoadEmissionsDataTool(),
            'load_knowledge_base': LoadKnowledgeBaseTool(),
            'analyze_emissions': AnalyzeEmissionsTool(),
            'compare_emissions': CompareEmissionsTool(),
            'get_data_info': GetDataInfoTool(),
            'create_vector_collections': CreateVectorCollectionsTool(),
            
            # Vector tools
            'upsert': UpsertTool(),
            'query': QueryTool(),
            'similarity_search': SimilaritySearchTool(),
            'retrieve_topk_with_spans': RetrieveTopKWithSpansTool(),
            
            # Reporting tools
            'write_md': WriteMDTool(),
            'write_file': WriteFileTool(),
            'save_question_report': SaveQuestionReportTool(),
        }
    
    def get_tool(self, tool_name: str):
        """Get a tool instance by name."""
        return self._tools.get(tool_name)
    
    def get_tools(self, tool_names: list) -> list:
        """Get multiple tool instances by names."""
        return [self._tools[name] for name in tool_names if name in self._tools]
    
    def get_data_tools(self) -> list:
        """Get all data-related tools."""
        return [
            self._tools['load_emissions_data'],
            self._tools['load_knowledge_base'],
            self._tools['analyze_emissions'],
            self._tools['compare_emissions'],
            self._tools['get_data_info'],
            self._tools['create_vector_collections'],
        ]
    
    def get_vector_tools(self) -> list:
        """Get all vector-related tools."""
        return [
            self._tools['upsert'],
            self._tools['query'],
            self._tools['similarity_search'],
            self._tools['retrieve_topk_with_spans'],
        ]
    
    def get_reporting_tools(self) -> list:
        """Get all reporting-related tools."""
        return [
            self._tools['write_md'],
            self._tools['write_file'],
            self._tools['save_question_report'],
        ]

# Global registry instance
def get_tool_registry() -> ToolRegistry:
    """Get the global tool registry instance."""
    return ToolRegistry()

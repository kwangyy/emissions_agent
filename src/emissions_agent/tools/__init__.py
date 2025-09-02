"""
Tool registry for emissions agent.
Maps tools.yaml specifications to actual Python implementations.
"""

# This file now serves as a simple import aggregator.
# The actual tool registry logic is in tool_registry.py

# Re-export tools for convenient importing
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

# For backwards compatibility, import the modern registry
from .tool_registry import get_tool_registry

__all__ = [
    # Data tools
    'LoadEmissionsDataTool', 'LoadKnowledgeBaseTool', 'AnalyzeEmissionsTool', 
    'CompareEmissionsTool', 'GetDataInfoTool', 'CreateVectorCollectionsTool',
    
    # Vector tools
    'UpsertTool', 'QueryTool', 'SimilaritySearchTool', 'RetrieveTopKWithSpansTool',
    
    # Reporting tools
    'WriteMDTool', 'WriteFileTool', 'SaveQuestionReportTool',
    
    # Registry
    'get_tool_registry'
]
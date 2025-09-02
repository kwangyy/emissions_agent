from crewai.tools import BaseTool
from typing import Type, Dict, List, Optional
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
import fitz  # PyMuPDF
from pathlib import Path
import os
import json
from .vector_manager import get_vector_manager

# Global data storage
_dataframes: Dict[str, pd.DataFrame] = {}
_documents: Dict[str, List[dict]] = {}

# ============================================================================
# DATA LOADING TOOLS
# ============================================================================

class LoadEmissionsDataInput(BaseModel):
    """Input schema for LoadEmissionsData tool."""
    data_directory: str = Field(default="./data", description="Directory containing emissions data files")

class LoadEmissionsDataTool(BaseTool):
    name: str = "load_emissions_data"
    description: str = "Load all emissions data files (scope1.csv, scope2.csv, scope3.csv) into memory"
    args_schema: Type[BaseModel] = LoadEmissionsDataInput

    def _run(self, data_directory: str = "./data") -> str:
        try:
            # Handle relative paths from current working directory
            if data_directory.startswith('./'):
                data_dir = Path.cwd() / data_directory[2:]
            elif data_directory.startswith('/') or ':' in data_directory:
                data_dir = Path(data_directory)
            else:
                data_dir = Path.cwd() / data_directory
            
            loaded_files = []
            
            for filename in ["scope1.csv", "scope2.csv", "scope3.csv"]:
                file_path = data_dir / filename
                if file_path.exists():
                    df = pd.read_csv(file_path)
                    df_name = filename.replace('.csv', '')
                    _dataframes[df_name] = df
                    loaded_files.append(f"{filename}: {len(df)} rows")
                else:
                    loaded_files.append(f"{filename}: File not found")
            
            return f"Loaded emissions data from {data_dir}: {'; '.join(loaded_files)}"
        except Exception as e:
            return f"Error loading data: {str(e)}"

class LoadKnowledgeBaseInput(BaseModel):
    """Input schema for LoadKnowledgeBase tool."""
    data_directory: str = Field(default="./data", description="Directory containing knowledge base files")

class LoadKnowledgeBaseTool(BaseTool):
    name: str = "load_knowledge_base"
    description: str = "Load knowledge base documents (PDFs) and prepare them for vector search"
    args_schema: Type[BaseModel] = LoadKnowledgeBaseInput

    def _run(self, data_directory: str = "./data") -> str:
        try:
            # Handle relative paths from current working directory (consistent with LoadEmissionsDataTool)
            if data_directory.startswith('./'):
                data_dir = Path.cwd() / data_directory[2:]
            elif data_directory.startswith('/') or ':' in data_directory:
                data_dir = Path(data_directory)
            else:
                data_dir = Path.cwd() / data_directory
            loaded_files = []
            
            # Only load PDF files that actually exist
            expected_pdfs = ["ghg-protocol-revised.pdf", "peer1_emissions_report.pdf", "peer2_emissions_report.pdf"]
            available_pdfs = []
            
            # Check which PDFs are actually available
            for filename in expected_pdfs:
                file_path = data_dir / filename
                if file_path.exists():
                    available_pdfs.append(filename)
                    
            if not available_pdfs:
                return f"No PDF files found in {data_directory}. Expected: {expected_pdfs}"
            
            # Load only available PDFs
            for filename in available_pdfs:
                file_path = data_dir / filename
                try:
                    doc = fitz.open(file_path)
                    chunks = []
                    for page_num, page in enumerate(doc):
                        text = page.get_text()
                        if text.strip():  # Only add non-empty chunks
                            for i in range(0, len(text), 1000):
                                chunk = text[i:i + 1000]
                                if chunk.strip():  # Only add non-empty chunks
                                    chunks.append({
                                        'text': chunk,
                                        'metadata': {
                                            'page': page_num + 1,
                                            'source': str(file_path),
                                            'document_name': filename.replace('.pdf', '')
                                        }
                                    })
                    doc.close()
                    
                    doc_name = filename.replace('.pdf', '')
                    _documents[doc_name] = chunks
                    loaded_files.append(f"{filename}: {len(chunks)} chunks")
                except Exception as file_error:
                    loaded_files.append(f"{filename}: Error loading - {str(file_error)}")
            
            # Report unavailable files for transparency
            missing_files = [f for f in expected_pdfs if f not in available_pdfs]
            if missing_files:
                loaded_files.append(f"Missing files: {', '.join(missing_files)}")
            
            return f"Available PDFs loaded: {'; '.join(loaded_files)}"
        except Exception as e:
            return f"Error loading knowledge base: {str(e)}"

# ============================================================================
# DATA ANALYSIS TOOLS
# ============================================================================

class AnalyzeEmissionsInput(BaseModel):
    """Input schema for AnalyzeEmissions tool."""
    scope: str = Field(..., description="Scope to analyze (scope1, scope2, scope3, or all)")
    analysis_type: str = Field(..., description="Type of analysis (summary, hotspots, quality)")

class AnalyzeEmissionsTool(BaseTool):
    name: str = "analyze_emissions"
    description: str = "Analyze emissions data for insights, hotspots, and quality assessment"
    args_schema: Type[BaseModel] = AnalyzeEmissionsInput

    def _run(self, scope: str, analysis_type: str) -> str:
        try:
            if scope == "all":
                dataframes = {k: v for k, v in _dataframes.items() if k.startswith("scope")}
            else:
                if scope not in _dataframes:
                    return f"Dataframe '{scope}' not found. Available: {list(_dataframes.keys())}"
                dataframes = {scope: _dataframes[scope]}
            
            results = {}
            for df_name, df in dataframes.items():
                if analysis_type == "summary":
                    results[df_name] = self._get_summary(df)
                elif analysis_type == "hotspots":
                    results[df_name] = self._get_hotspots(df)
                elif analysis_type == "quality":
                    results[df_name] = self._get_quality(df)
                else:
                    return f"Unsupported analysis type. Use: summary, hotspots, quality"
            
            return json.dumps(results, indent=2, default=str)
        except Exception as e:
            return f"Error analyzing emissions: {str(e)}"
    
    def _get_summary(self, df: pd.DataFrame) -> dict:
        """Get emissions summary"""
        if 'CO2e_Tonnes' not in df.columns:
            return {"error": "No CO2e_Tonnes column"}
        
        total = df['CO2e_Tonnes'].sum()
        return {
            "total_emissions": total,
            "average_emissions": df['CO2e_Tonnes'].mean(),
            "max_emissions": df['CO2e_Tonnes'].max(),
            "records": len(df)
        }
    
    def _get_hotspots(self, df: pd.DataFrame) -> dict:
        """Identify emissions hotspots"""
        if 'CO2e_Tonnes' not in df.columns:
            return {"error": "No CO2e_Tonnes column"}
        
        if 'Facility' in df.columns:
            facility_emissions = df.groupby('Facility')['CO2e_Tonnes'].sum().sort_values(ascending=False)
            return {"facility_hotspots": facility_emissions.head(3).to_dict()}
        elif 'Category' in df.columns:
            category_emissions = df.groupby('Category')['CO2e_Tonnes'].sum().sort_values(ascending=False)
            return {"category_hotspots": category_emissions.head(3).to_dict()}
        else:
            return {"error": "No Facility or Category column for hotspot analysis"}
    
    def _get_quality(self, df: pd.DataFrame) -> dict:
        """Assess data quality"""
        issues = []
        if df.isnull().sum().sum() > 0:
            issues.append("Missing values")
        if df.duplicated().sum() > 0:
            issues.append("Duplicate rows")
        
        return {
            "total_rows": len(df),
            "missing_values": df.isnull().sum().sum(),
            "duplicate_rows": df.duplicated().sum(),
            "quality_score": max(0, 100 - len(issues) * 20),
            "issues": issues
        }

class CompareEmissionsInput(BaseModel):
    """Input schema for CompareEmissions tool."""
    scope1: str = Field(..., description="First scope to compare")
    scope2: str = Field(..., description="Second scope to compare")

class CompareEmissionsTool(BaseTool):
    name: str = "compare_emissions"
    description: str = "Compare emissions between different scopes"
    args_schema: Type[BaseModel] = CompareEmissionsInput

    def _run(self, scope1: str, scope2: str) -> str:
        try:
            if scope1 not in _dataframes or scope2 not in _dataframes:
                return f"One or both dataframes not found. Available: {list(_dataframes.keys())}"
            
            df1, df2 = _dataframes[scope1], _dataframes[scope2]
            total1, total2 = df1['CO2e_Tonnes'].sum(), df2['CO2e_Tonnes'].sum()
            
            comparison = {
                scope1: {"total": total1, "records": len(df1)},
                scope2: {"total": total2, "records": len(df2)},
                "difference": total1 - total2,
                "percentage_diff": ((total1 - total2) / total2 * 100) if total2 != 0 else float('inf')
            }
            
            return json.dumps(comparison, indent=2, default=str)
        except Exception as e:
            return f"Error comparing emissions: {str(e)}"

class GetDataInfoInput(BaseModel):
    """Input schema for GetDataInfo tool."""
    data_type: str = Field(default="dataframes", description="Type of data (dataframes or documents)")

class GetDataInfoTool(BaseTool):
    name: str = "get_data_info"
    description: str = "Get information about loaded data"
    args_schema: Type[BaseModel] = GetDataInfoInput

    def _run(self, data_type: str = "dataframes") -> str:
        try:
            if data_type == "dataframes":
                info = {}
                for name, df in _dataframes.items():
                                    info[name] = {
                    "rows": len(df),
                    "column_count": len(df.columns),
                    "columns": list(df.columns)
                }
            elif data_type == "documents":
                info = {}
                for name, docs in _documents.items():
                    info[name] = {"chunks": len(docs)}
            else:
                return f"Invalid data_type. Use: dataframes or documents"
            
            return json.dumps(info, indent=2)
        except Exception as e:
            return f"Error getting data info: {str(e)}"

# ============================================================================
# UTILITY FUNCTIONS FOR OTHER MODULES
# ============================================================================

def get_dataframe(name: str) -> pd.DataFrame:
    """Get a dataframe by name."""
    return _dataframes.get(name)

def has_dataframe(name: str) -> bool:
    """Check if a dataframe exists."""
    return name in _dataframes

def list_dataframes() -> list:
    """List all dataframe names."""
    return list(_dataframes.keys())

def get_documents(name: str) -> List[dict]:
    """Get documents by name."""
    return _documents.get(name, [])

def has_documents(name: str) -> bool:
    """Check if documents exist."""
    return name in _documents

def list_documents() -> list:
    """List all document names."""
    return list(_documents.keys())

class CreateVectorCollectionsInput(BaseModel):
    """Input schema for CreateVectorCollections tool."""
    force_recreate: bool = Field(default=False, description="Whether to recreate existing collections")

class CreateVectorCollectionsTool(BaseTool):
    name: str = "create_vector_collections"
    description: str = "Create specialized vector collections from loaded data for efficient querying"
    args_schema: Type[BaseModel] = CreateVectorCollectionsInput

    def _run(self, force_recreate: bool = False) -> str:
        try:
            from .vector_manager import get_vector_manager
            vector_manager = get_vector_manager()
            
            collections_created = []
            
            # Check if collections already exist
            existing_collections = []
            try:
                existing_collections = [col.name for col in vector_manager.client.list_collections()]
            except:
                pass
            

            
            # Create GHG protocol collection from PDF documents
            if "ghg_protocol" not in existing_collections or force_recreate:
                ghg_docs = []
                for doc_name, chunks in _documents.items():
                    if 'ghg' in doc_name.lower() or 'protocol' in doc_name.lower():
                        for i, chunk in enumerate(chunks):
                            ghg_docs.append({
                                'id': f"{doc_name}_chunk_{i}",
                                'text': chunk['text'],
                                'metadata': {
                                    **chunk['metadata'],
                                    'data_type': 'regulatory_guidance'
                                }
                            })
                
                if ghg_docs:
                    result = vector_manager.upsert_documents("ghg_protocol", ghg_docs)
                    collections_created.append(f"ghg_protocol: {result}")
            else:
                collections_created.append("ghg_protocol: Already exists, skipped")
            
            # Create peer benchmarks collection
            if "peer_benchmarks" not in existing_collections or force_recreate:
                peer_docs = []
                for doc_name, chunks in _documents.items():
                    if 'peer' in doc_name.lower():
                        for i, chunk in enumerate(chunks):
                            peer_docs.append({
                                'id': f"{doc_name}_chunk_{i}",
                                'text': chunk['text'],
                                'metadata': {
                                    **chunk['metadata'],
                                    'data_type': 'peer_benchmark'
                                }
                            })
                
                if peer_docs:
                    result = vector_manager.upsert_documents("peer_benchmarks", peer_docs)
                    collections_created.append(f"peer_benchmarks: {result}")
            else:
                collections_created.append("peer_benchmarks: Already exists, skipped")
            
            return f"Created vector collections: {'; '.join(collections_created)}"
            
        except Exception as e:
            return f"Error creating vector collections: {str(e)}"
 
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import pandas as pd
from pathlib import Path

class WriteMDInput(BaseModel):
    """Input schema for WriteMD tool."""
    content: str = Field(..., description="Markdown content to write")
    file_path: str = Field(..., description="Path to save the markdown file")

class WriteMDTool(BaseTool):
    name: str = "write_md"
    description: str = "Write content to a markdown file"
    args_schema: Type[BaseModel] = WriteMDInput

    def _run(self, content: str, file_path: str) -> str:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote markdown to {file_path}"
        except Exception as e:
            return f"Error writing markdown file: {str(e)}"

class WriteFileInput(BaseModel):
    """Input schema for WriteFile tool."""
    content: str = Field(..., description="Content to write")
    file_path: str = Field(..., description="Path to save the file")

class WriteFileTool(BaseTool):
    name: str = "write_file"
    description: str = "Write content to a file"
    args_schema: Type[BaseModel] = WriteFileInput

    def _run(self, content: str, file_path: str) -> str:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote content to {file_path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"

class SaveQuestionReportInput(BaseModel):
    """Input schema for SaveQuestionReport tool."""
    question: str = Field(..., description="The question that was answered")
    answer: str = Field(..., description="The detailed answer to the question")
    question_number: int = Field(..., description="Question number for file naming")

class SaveQuestionReportTool(BaseTool):
    name: str = "save_question_report"
    description: str = "Save a question and its answer as a separate report file"
    args_schema: Type[BaseModel] = SaveQuestionReportInput

    def _run(self, question: str, answer: str, question_number: int) -> str:
        try:
            # Create outputs directory if it doesn't exist
            output_dir = Path("outputs")
            output_dir.mkdir(exist_ok=True)
            
            # Generate filename
            filename = f"question_{question_number}_report.md"
            file_path = output_dir / filename
            
            # Create markdown content
            content = f"""# Question {question_number} Report

## Question
{question}

## Answer
{answer}

---
*Generated on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
            
            # Save the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"Successfully saved question report to {file_path}"
        except Exception as e:
            return f"Error saving question report: {str(e)}"
#!/usr/bin/env python
import sys
import warnings
import os
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from emissions_agent.crew import EmissionsAgent

# Load environment variables from .env file
# Look for .env file in current directory and parent directories
env_path = Path('.') / '.env'
if not env_path.exists():
    env_path = Path('..') / '.env'
load_dotenv(env_path, override=True)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Standard questions for the emissions analysis
STANDARD_QUESTIONS = [
    "Should employee business travel be classified as Scope 1 or Scope 3? Explain the reasoning and describe how I can calculate my business travel emissions?",
    "Are my scope 2 emissions calculation valid according to the Greenhouse Gas Protocol?",
    "How do my scope 1 & 2 emissions compare with other companies in my industry, and what insights can I derive from this comparison?",
    "What is our highest emitting Scope 3 category and what specific activities contribute to it?",
    "Which suppliers should I prioritise to engage for emissions reduction efforts?",
    "Generate a summary report of our total emissions by scope with key insights"
]

def check_api_key():
    """Check if OpenAI API key is available."""
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  Warning: OPENAI_API_KEY not found in environment variables.")
        print("   Please create a .env file with your OpenAI API key:")
        print("   OPENAI_API_KEY=your_openai_api_key_here")
        print("   Get your API key from: https://platform.openai.com/api-keys")
        return False
    return True

def ensure_outputs_dir():
    """Ensure outputs directory exists."""
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(exist_ok=True)
    return outputs_dir

def save_report_fallback(question_text: str, result: str, question_number: int):
    """Fallback mechanism to save report if agent didn't call the tool."""
    outputs_dir = ensure_outputs_dir()
    report_file = outputs_dir / f"question_{question_number}_report.md"
    
    if not report_file.exists():
        try:
            from src.emissions_agent.tools.reporting_tools import SaveQuestionReportTool
            save_tool = SaveQuestionReportTool()
            save_result = save_tool._run(
                question=question_text, 
                answer=str(result), 
                question_number=question_number
            )
            print(f"📄 Report saved via fallback: {save_result}")
        except Exception as e:
            print(f"⚠️  Failed to save report via fallback: {e}")

def run_full_crew():
    """Run the full crew with all questions in one comprehensive analysis."""
    if not check_api_key():
        return
    
    inputs = {
        'questions': STANDARD_QUESTIONS,
        'analysis_focus': 'comprehensive emissions analysis with specific business questions',
        'current_year': str(datetime.now().year)
    }
    
    try:
        print("🚀 Starting comprehensive emissions analysis with all questions...")
        EmissionsAgent().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the full crew: {e}")

def run_single_question(question_text: str, question_number: int = 1, save_fallback: bool = True):
    """Run a single question analysis."""
    if not check_api_key():
        return None
    
    ensure_outputs_dir()
    
    inputs = {
        'question': question_text,
        'question_number': question_number,
        'current_year': str(datetime.now().year)
    }
    
    try:
        print(f"🚀 Answering question: {question_text}")
        print(f"📁 Output will be saved to: outputs/question_{question_number}_report.md")
        
        result = EmissionsAgent().simple_crew().kickoff(inputs=inputs)
        
        # Use fallback save mechanism if enabled
        if save_fallback:
            save_report_fallback(question_text, str(result), question_number)
        
        print(f"\n✅ Question {question_number} completed and saved to outputs/question_{question_number}_report.md")
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the question: {e}")

def run_questions_individually():
    """Run each standard question individually and collect results."""
    if not check_api_key():
        return None
    
    outputs_dir = ensure_outputs_dir()
    results = {}
    
    for i, question in enumerate(STANDARD_QUESTIONS, 1):
        print(f"\n{'='*80}")
        print(f"QUESTION {i}: {question}")
        print(f"{'='*80}")
        
        result = run_single_question(question, question_number=i, save_fallback=True)
        if result:
            results[f"Question {i}"] = {
                "question": question,
                "answer": result
            }
    
    # Create a summary index file
    create_summary_index(outputs_dir)
    
    return results

def create_summary_index(outputs_dir: Path):
    """Create a summary index of all question reports."""
    summary_content = f"""# Emissions Analysis - Question Reports Summary

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Questions Analyzed

"""
    for i, question in enumerate(STANDARD_QUESTIONS, 1):
        summary_content += f"{i}. [{question}](question_{i}_report.md)\n"
    
    try:
        with open(outputs_dir / "question_reports_index.md", 'w', encoding='utf-8') as f:
            f.write(summary_content)
        print(f"📋 Summary index created: outputs/question_reports_index.md")
    except Exception as e:
        print(f"⚠️  Failed to create summary index: {e}")

def train(iterations: int, filename: str):
    """Train the crew for a given number of iterations."""
    inputs = {
        "questions": STANDARD_QUESTIONS,
        'analysis_focus': 'comprehensive emissions analysis with specific business questions',
        'current_year': str(datetime.now().year)
    }
    try:
        EmissionsAgent().crew().train(n_iterations=iterations, filename=filename, inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def test(iterations: int, eval_llm: str):
    """Test the crew execution and returns the results."""
    inputs = {
        "questions": STANDARD_QUESTIONS,
        'analysis_focus': 'comprehensive emissions analysis with specific business questions',
        "current_year": str(datetime.now().year)
    }
    
    try:
        EmissionsAgent().crew().test(n_iterations=iterations, eval_llm=eval_llm, inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def replay(task_id: str):
    """Replay the crew execution from a specific task."""
    try:
        EmissionsAgent().crew().replay(task_id=task_id)
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='Emissions Agent - AI-powered emissions analysis')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Run full comprehensive analysis
    run_parser = subparsers.add_parser('run', help='Run comprehensive analysis with all questions in one crew')
    
    # Run questions individually 
    questions_parser = subparsers.add_parser('questions', help='Run all questions individually and save separate reports')
    
    # Single question
    single_parser = subparsers.add_parser('ask', help='Ask a single question')
    single_parser.add_argument('question', help='The question to ask')
    single_parser.add_argument('--number', '-n', type=int, default=1, help='Question number for file naming (default: 1)')
    
    # Training
    train_parser = subparsers.add_parser('train', help='Train the crew')
    train_parser.add_argument('iterations', type=int, help='Number of training iterations')
    train_parser.add_argument('filename', help='Training filename')
    
    # Testing
    test_parser = subparsers.add_parser('test', help='Test the crew')
    test_parser.add_argument('iterations', type=int, help='Number of test iterations')
    test_parser.add_argument('eval_llm', help='Evaluation LLM')
    
    # Replay
    replay_parser = subparsers.add_parser('replay', help='Replay crew execution')
    replay_parser.add_argument('task_id', help='Task ID to replay')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        run_full_crew()
    elif args.command == 'questions':
        run_questions_individually()
    elif args.command == 'ask':
        run_single_question(args.question, args.number)
    elif args.command == 'train':
        train(args.iterations, args.filename)
    elif args.command == 'test':
        test(args.iterations, args.eval_llm)
    elif args.command == 'replay':
        replay(args.task_id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
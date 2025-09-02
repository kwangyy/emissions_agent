from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from typing import List
from emissions_agent.tools.tool_registry import get_tool_registry

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class EmissionsAgent():
    """Emissions Analysis & Insights Agent crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    @agent
    def data_engineer(self) -> Agent:
        agent_config = self.agents_config['data_engineer']  # type: ignore[index]
        tool_registry = get_tool_registry()
        tools = [
            # Data tools
            tool_registry.get_tool('load_emissions_data'),
            tool_registry.get_tool('load_knowledge_base'),
            tool_registry.get_tool('create_vector_collections'),
            tool_registry.get_tool('analyze_emissions'),
            # Vector tools
            tool_registry.get_tool('upsert'),
            tool_registry.get_tool('query'),
            tool_registry.get_tool('similarity_search'),
        ]
        return Agent(
            config=agent_config,
            tools=tools,
            verbose=True
        )

    @agent
    def emissions_analyst(self) -> Agent:
        agent_config = self.agents_config['emissions_analyst']  # type: ignore[index]
        tool_registry = get_tool_registry()
        tools = [
            # Data analysis tools
            tool_registry.get_tool('analyze_emissions'),
            tool_registry.get_tool('compare_emissions'),
            tool_registry.get_tool('get_data_info'),
            # Vector tools for cross-referencing data and regulations
            tool_registry.get_tool('query'),
            tool_registry.get_tool('similarity_search'),
            tool_registry.get_tool('retrieve_topk_with_spans'),
            # Report saving tool
            tool_registry.get_tool('save_question_report'),
        ]
        return Agent(
            config=agent_config,
            tools=tools,
            verbose=True
        )

    @agent
    def sustainability_advisor(self) -> Agent:
        agent_config = self.agents_config['sustainability_advisor']  # type: ignore[index]
        tool_registry = get_tool_registry()
        tools = [
            # Vector tools for precise regulatory guidance retrieval
            tool_registry.get_tool('query'),
            tool_registry.get_tool('similarity_search'),
            tool_registry.get_tool('retrieve_topk_with_spans'),
            tool_registry.get_tool('load_knowledge_base'),
        ]
        
        # No duplicate knowledge sources - PDFs will be loaded via custom vector tools
        return Agent(
            config=agent_config,
            tools=tools,
            verbose=True
        )

    @agent
    def insights_reporter(self) -> Agent:
        agent_config = self.agents_config['insights_reporter']  # type: ignore[index]
        tool_registry = get_tool_registry()
        tools = [
            # Reporting tools
            tool_registry.get_tool('write_md'),
            tool_registry.get_tool('write_file'),
            tool_registry.get_tool('save_question_report'),
            # Analysis tools
            tool_registry.get_tool('analyze_emissions'),
        ]
        return Agent(
            config=agent_config,
            tools=tools,
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def data_ingestion_and_quality_assessment(self) -> Task:
        return Task(
            config=self.tasks_config['data_ingestion_and_quality_assessment'], # type: ignore[index]
        )

    @task
    def emissions_analysis_and_insights(self) -> Task:
        return Task(
            config=self.tasks_config['emissions_analysis_and_insights'], # type: ignore[index]
        )

    @task
    def sustainability_guidance_and_education(self) -> Task:
        return Task(
            config=self.tasks_config['sustainability_guidance_and_education'], # type: ignore[index]
        )

    @task
    def natural_language_query_processing(self) -> Task:
        return Task(
            config=self.tasks_config['natural_language_query_processing'], # type: ignore[index]
        )

    @task
    def comprehensive_emissions_report(self) -> Task:
        return Task(
            config=self.tasks_config['comprehensive_emissions_report'], # type: ignore[index]
            output_file='emissions_report.md'
        )

    @task
    def single_question_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['single_question_analysis'], # type: ignore[index]
            # Remove hardcoded output_file - let save_question_report tool handle file naming
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Emissions Analysis & Insights Agent crew"""
        # Create knowledge sources following official CrewAI documentation
        # https://docs.crewai.com/concepts/knowledge
        
        # Text file knowledge source for user preferences (only small context file)
        user_prefs_knowledge = TextFileKnowledgeSource(
            file_paths=["user_preference.txt"]
        )

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            knowledge_sources=[user_prefs_knowledge],
        )

    def simple_crew(self) -> Crew:
        """Creates a simple crew for answering single questions"""
        
        # Text file knowledge source for user preferences (only small context file)
        user_prefs_knowledge = TextFileKnowledgeSource(
            file_paths=["user_preference.txt"]
        )

        return Crew(
            agents=[self.data_engineer(), self.emissions_analyst()], # Only essential agents
            tasks=[self.data_ingestion_and_quality_assessment(), self.single_question_analysis()], # Simplified tasks
            process=Process.sequential,
            verbose=True,
            # Only user preferences - PDFs handled by custom vector tools to avoid duplication
            knowledge_sources=[user_prefs_knowledge],
        )

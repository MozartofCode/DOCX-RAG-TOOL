from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import DOCXSearchTool
import os

# Uncomment the following line to use an example of a custom tool
# from rag_tool.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class RagToolCrew():
	"""RagTool crew"""

	

	@agent
	def researcher(self) -> Agent:
		docx_file = os.path.abspath("Untitled.docx")

		# Validate the file exists
		if not os.path.exists(docx_file):
			raise FileNotFoundError(f"The DOCX file was not found at: {docx_file}")
		
		return Agent(
			config=self.agents_config['researcher'],
			tools=[DOCXSearchTool(docx=docx_file)],
			verbose=True
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)
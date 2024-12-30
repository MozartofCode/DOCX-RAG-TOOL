from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import DOCXSearchTool
import os


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

	@agent
	def writer(self) -> Agent:
		return Agent(
			config=self.agents_config['writer'],
			verbose=True
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def writer_task(self) -> Task:
		return Task(
			config=self.tasks_config['writer_task'],
		)

	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)
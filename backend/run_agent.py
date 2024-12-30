import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew
from crewai_tools import DOCXSearchTool
import warnings
warnings.filterwarnings('ignore')
import os
openai_api_key = os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
load_dotenv()

def main(question):
    # Define tools
    docx_file = os.path.abspath("./backend/company.docx")

		# Validate the file exists
    if not os.path.exists(docx_file):
       raise FileNotFoundError(f"The DOCX file was not found at: {docx_file}")
		

    # Define agents
    researcher = Agent(        
        role= "Senior Document Researcher",
        goal= "Uncover cutting-edge information about a company based on their company document and answer the '{question}' of"
              " the customer in a clear and concise manner and ONLY INCLUDE THE RELEVANT INFORMATION FROM THE DOCUMENT",
        backstory= "You're a seasoned researcher with a knack for uncovering the best information"
              " inside a given document and displaying it in a friendly way as a costumer service agent."
              " Known for your ability to find the most relevant information and present it in a clear and concise manner",
        verbose=False,
        tools=[DOCXSearchTool(docx=docx_file)]
    )

    writer = Agent(
        role= "Senior Content Writer",
        goal= "Answer the {question} of the customer based on the findings from the company documents."
              " Present this information in a clear and concise manner as brief and concise as possible.",
        backstory= "You're a seasoned writer with a knack for presenting the information in the most brief and concise way."
              " Known for your ability to write in a clear and concise manner and present the information in a friendly way"
              " as a costumer service agent, ",
        verbose=False
    )

    
    # Define the task
    research_task = Task(
      description=(
        " Conduct a thorough research to answer a customers question: '{question}' "
        " Make sure you find any relevant information and present it in the best possible way"
        " for the customer to understand" 
      ),
      expected_output= "Costumer Service message as a response to the given inquiry based on the research from the given company document",
      agent=researcher
    )

    writer_task = Task(
      description=(
        " Write a response to the customer's inquiry: '{question}'"
        " Make sure you include all the relevant information and present it in a friendly way"
        " that is concicse and BRIEF"   
      ),
      expected_output= "A response to the {question} in the form of an answer from a customer service agent",
      agent=writer
    )

    # Initialize Crew
    crew = Crew(
        agents=[researcher, writer], 
        tasks=[research_task, writer_task], 
        manager_llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7),
        verbose=False,
    )

    # Run the Crew with the given dare
    question_input = {"question": question}
    result = crew.kickoff(inputs=question_input)

    return result.raw

from textwrap import dedent
from crewai import Agent
from tools import dev_tool
from utils import print_agent_output

class AnalyseAgents():
	def python_dev_agent(self):
		return Agent(
			role='Python programmer',
			goal=dedent("""Create the piece of code as needed and test it using the repl tool.
			   Don't forget to print at the end to get the result.
			   If the code is correct, send it. 
			   If it is not correct, fix it and test it again."""),
			backstory=dedent("""\
				You are a Senior Python programmer at a leading tech company.
				You do your best to	produce perfect code
				You have access to pandas, numpy, matplotlib and other data science libraries"""),
			allow_delegation=False,
			verbose=True,
			memory=False,
			tools=[dev_tool],
			max_iter=3,
			step_callback=lambda x: print_agent_output(x,"Python programmer")
		)

	def data_analyst_agent(self):
		return Agent(
			role='Data analyst',
  		goal=dedent("""\
				You receive the format of some data and a question.
				You write a plan to answer the question using the data as a data analyst would do.
				You can do back and forth with the python programmer if you need to.
				You send this plan to the python developper.
				You don't write any python code yourself."""),
  		backstory=dedent("""\
				You are a senior data analyst at a leading tech company.
			    You work with the Python programmer and the project manager to get the job done"""),
			allow_delegation=True,
			verbose=True,
			memory=True,
			max_iter=5,
			step_callback=lambda x: print_agent_output(x,"Data analyst")
		)

	def project_manager(self):
		return Agent(
			role='Project manager',
  		goal='Send the data and question to the python developper. And ensure that the received code does the job that it is supposed to do.',
  		backstory=dedent("""\
				You are a project manager in a leading tech company.
					 You work with the data analyst."""),
			allow_delegation=True,
			verbose=True,
			memory=True,
			max_iter=2,
			step_callback=lambda x: print_agent_output(x,"Project manager")
		)
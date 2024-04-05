from textwrap import dedent
from crewai import Task

class AnalyseTasks():
	
    def receive_task(self, agent, data, question):
        return Task(description=dedent(f"""\
			You are receiving a question and data from the human :

			Question
			------------
			{question}
			
			Data
			------------
			{data}

			You send the question and path of the data to the python programmer. He will be tasked to open the file and assess the structure of the data."""),
            expected_output=dedent("""The question and the path of the data.
                                   eg. 'What is the population of the city with the highest population?','/path/to/data.csv'"""),
            agent=agent
        )
    
    def open_and_assess_file_task(self, agent, tasks):
        return Task(description=dedent(f"""\
            You will open the file that the project manager sent you and assess the structure of the data.
            You will use python code to do so. Dont forget to print the data structure if you want to receive it.
            You will then send the structure of the data to the data analyst.
            You will also send the question to the data analyst.
            """),
            expected_output=dedent("""The structure of the data.
            eg. 'city','latitude','longitude','population','region','country'
            And the question that was asked.
            eg. 'What is the population of the city with the highest population?'"""),
            agent=agent,
            context=tasks
        )

    def analyse_data_task(self, agent, tasks):
        return Task(description=dedent(f"""\
            You will look at the data structure that the python programmer sent you.
            You will also look at the question related to those data.
            You will devise a plan to reach the answer to this question knowing the structure of the data.
            You will send this plan to the python developper that will code something that will answer this question.
            You can do back and forth with the python programmer if you need to have more informations about the data before writing the final plan.
            """),
            expected_output=dedent("""The plan that you created to answer the question.
                                   eg. '1. Import the data from the csv file.
                                   2. Check for missing values in the data.
                                   3. Find the city with the highest population.'"""),
            agent=agent,
            context=tasks
        )

    def code_task(self, agent, tasks):
        return Task(description=dedent(f"""\
            You will create python code according to the data analyst instructions.
            You will run this code and test it using the repl tool.
            If the code return an error, you must fix it and test it again.
            """),
            expected_output=dedent("""The code and output of the code after it has been succesfully tested.
            eg. import pandas as pd; df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}); print(df.head());   a  b;0  1  4;1  2  5;2  3  6"""),
            agent=agent,
            context=tasks
        )

    def validate_task(self, agent, question, tasks):
        return Task(description=dedent(f"""\
            You will validate that the code the python developper sent you answer the question correctly:
            
            Question
            ------------
            {question}

            Your Final answer must be the full python code, only the python code and nothing else.
            """),
            expected_output=dedent("""The full code that the python developper sent and after it has been validated."""),
            agent=agent,
            output_file='full_code.txt',
            context=tasks
        )
    

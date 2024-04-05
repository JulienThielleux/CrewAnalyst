def main():

    from crewai import Crew, Process
    from langchain_openai import ChatOpenAI
    from dotenv import load_dotenv

    from tasks import AnalyseTasks
    from agents import AnalyseAgents

    tasks = AnalyseTasks()
    agents = AnalyseAgents()

    load_dotenv(override=True)

    # Print welcome message and ask for data and question
    print("Welcome to the data analysis tool for CrewAI")
    print('--------------------------------------------')

    data = input("Where are the data you need to analyse ? : ")
    question = input("What would you like to analyse ? : ")

    # Initialize the OpenAI GPT-4 language model
    OpenAIGPT4TURBO = ChatOpenAI(
        #model="gpt-4-turbo-preview"
        model="gpt-3.5-turbo"
    )

    # Create Agents
    python_dev_agent = agents.python_dev_agent()
    data_analyst_agent = agents.data_analyst_agent()
    project_manager = agents.project_manager()

    # Create Tasks
    receive_task = tasks.receive_task(project_manager, data, question)
    open_and_assess_file_task = tasks.open_and_assess_file_task(python_dev_agent, [receive_task])
    analyse_data_task = tasks.analyse_data_task(data_analyst_agent, [receive_task,open_and_assess_file_task])
    code_task = tasks.code_task(python_dev_agent,[receive_task,analyse_data_task, open_and_assess_file_task])
    validate_task = tasks.validate_task(project_manager, question, [receive_task,analyse_data_task, open_and_assess_file_task, code_task])


    # Create Crew
    crew = Crew(
        agents=[
            project_manager,
            data_analyst_agent,
            python_dev_agent
        ],
        tasks=[
            receive_task,
            open_and_assess_file_task,
            analyse_data_task,
            code_task,
            validate_task,
        ],
        verbose=True,
        process=Process.sequential,
        full_output=True,
        share_crew=False,
        manager_llm=OpenAIGPT4TURBO,
        max_iter=3
        )

    code = crew.kickoff()

    # Print results
    print("\n\n########################")
    print("## Here is the result")
    print("########################\n")
    print("final code for the data analyse:")
    print(code)

if __name__ == "__main__":
    main()
from langchain.utilities import PythonREPL
from langchain.agents import Tool

python_repl = PythonREPL()

# You can create the tool to pass to an agent
dev_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run,
)
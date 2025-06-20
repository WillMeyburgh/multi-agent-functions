from multi_agent_functions.v1.google.tasks.toolkit import GoogleTasksToolkit
from multi_agent_functions.v2.agent.base_agent import BaseAgent
from langgraph.prebuilt import create_react_agent

class ReactAgent(BaseAgent):
    def __init__(self, name: str, system_prompt: str, toolkit):
        super().__init__(name, system_prompt)
        self.toolkit = toolkit
        self.graph = None

    def compile(self, model):
        self.graph = create_react_agent(
            model,
            tools = self.toolkit.get_tools(),
            name=self.name,
            prompt=self.system_prompt
        )

    def invoke(self, state):
        return self.graph.invoke(state)
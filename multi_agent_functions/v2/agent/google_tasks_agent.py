from multi_agent_functions.v1.google.tasks.toolkit import GoogleTasksToolkit
from multi_agent_functions.v2.agent.react_agent import ReactAgent


class GoogleTasksAgent(ReactAgent):
    def __init__(self, name, system_prompt):
        super().__init__(name, system_prompt, GoogleTasksToolkit())
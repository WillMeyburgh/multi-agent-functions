from multi_agent_functions.google.calender.agent import GoogleCalendarAgent
from multi_agent_functions.google.calender.client import GoogleCalendarClient
from multi_agent_functions.google.tasks.agent import GoogleTasksAgent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

from multi_agent_functions.supervisor.agent import SupervisorAgent


model = init_chat_model(
    "google_genai:gemini-2.0-flash-thinking-exp-01-21",
    temperature=0,
)

agent = SupervisorAgent()
state = agent.init_state()
graph = agent.compile(model)

while True:
    state['messages'].append(HumanMessage(input("User: ")))
    for mode, chunk in graph.stream(state, stream_mode=["updates", "custom"]):
        if 'agent' in chunk:
            if 'messages' in chunk['agent']:
                if chunk['agent']['messages'][-1].content != '':
                    print(chunk['agent']['messages'][-1].content)
                state['messages'].append(chunk['agent']['messages'][-1])
        if 'tools' in chunk:
            state['messages'].append(chunk['tools']['messages'][-1])
            print(chunk['tools']['messages'][-1].name)
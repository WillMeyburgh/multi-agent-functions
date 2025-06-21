from multi_agent_functions.v1.google.calender.agent import GoogleCalendarAgent
from multi_agent_functions.v1.google.calender.client import GoogleCalendarClient
from multi_agent_functions.v1.google.tasks.agent import GoogleTasksAgent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

from multi_agent_functions.v1.llm.rate_limited_model import RateLimitedModel
from multi_agent_functions.v1.supervisor.agent import SupervisorAgent


model = init_chat_model(
    # "google_genai:gemini-2.0-flash-thinking-exp-01-21",
    "google_genai:gemini-2.5-flash",
    temperature=0,
)

model = RateLimitedModel(
    model,
    int(60/9)
)

agent = SupervisorAgent()
state = agent.init_state()
graph = agent.compile(model)

i = 0

"""
could you create a event for tomorrow 9 am with title warframes with all the tasks in my warframe tasklist as summary
"""

state['messages'].append(HumanMessage('could you create a event for tomorrow 9 am with title warframes with all the tasks in my warframe tasklist as summary'))

while True:
    # state['messages'].append(HumanMessage(input("User: ")))
    i+=1
    state = graph.invoke(state)
    for message in state['messages'][i:]:
        if message.content.strip() != '':
            print("AI:", message.content)
        i+=1
    break
    # for mode, chunk in graph.stream(state, stream_mode=["updates", "custom"]):
    #     if 'agent' in chunk:
    #         if 'messages' in chunk['agent']:
    #             if chunk['agent']['messages'][-1].content != '':
    #                 print(chunk['agent']['messages'][-1].content)
    #             state['messages'].append(chunk['agent']['messages'][-1])
    #     if 'tools' in chunk:
    #         state['messages'].append(chunk['tools']['messages'][-1])
    #         print(chunk['tools']['messages'][-1].name)
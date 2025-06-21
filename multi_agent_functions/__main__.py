from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

from multi_agent_functions.v1.llm.rate_limited_model import RateLimitedModel
from multi_agent_functions.v2.supervisor_graph import SupervisorGraph


model = init_chat_model(
    "google_genai:gemini-2.0-flash-thinking-exp-01-21",
    # "google_genai:gemini-2.5-flash",
    temperature=0.5,
)

model = RateLimitedModel(
    model,
    int(60/9)
)

state = SupervisorGraph.init_state()
graph = SupervisorGraph().compile(model)

"""
could you create a event for tomorrow 9 am with title warframes with all the tasks in my warframe tasklist as summary
"""

state['messages'].append(HumanMessage('could you create a event called warframes for 9 am tomorrow, for 30 minutes with description of all the tasks in my warframe tasklist, then afterwards add the event id to the tasklist'))

while True:
    # state['messages'].append(HumanMessage(input("User: ")))
    state = graph.invoke(state)
    print("AI:", state['messages'][-1].content)
    break
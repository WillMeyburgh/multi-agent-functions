from ast import List
from typing import Generic, Hashable, Literal, TypeVar

from pydantic import BaseModel, Field
from multi_agent_functions.v2.agent.base_agent import BaseAgent
from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import START, StateGraph

from multi_agent_functions.v2.agent.state import AgentState
from langgraph.types import Command, N

class Supervisor(BaseModel):
    next: Literal['enhancer', 'google_tasks', 'google_calendar', '__end__'] = Field(
        description="Select the next worker: 'enhancer' (enhances request and breaks into steps), 'google_tasks' (manages Google Tasks), 'google_calendar' (manages Google Calendar), or '__end__' (user query complete)."
    )
    reason: str = Field(
        description="The reason for the decision. When 'next' is '__end__', this field should contain the final message to the user (e.g., a summary, a question for more info, or a simple response)."
    )

class SupervisorGraph:
    def __init__(self):
        self.agents = BaseAgent.load_all()
        self.model = None

    @classmethod
    def init_state(cls) -> AgentState:
        return AgentState(messages=[])

    def supervisor_node(self, state: AgentState) -> Command[Literal['enhancer', 'google_tasks', 'google_calendar', '__end__']]:
        model = self.model.with_structured_output(Supervisor)

        result: Supervisor = model.invoke(
            [
                SystemMessage(self.agents['supervisor'].system_prompt),
            ] + state['messages']
        )

        return Command(
            update={
                'messages': [
                    HumanMessage(result.reason, name='supervisor')
                ],
            },
            goto=result.next
        )

    def agent_node(self, agent: str):
        def inner(state: AgentState) -> Command[Literal['supervisor']]:
            result = self.agents[agent].invoke({
                'messages': [state['messages'][-1]]
            })

            return Command(
                update={
                    'messages': [
                        HumanMessage(result['messages'][-1].content, name=agent)
                    ]
                },
                goto='supervisor'
            )
        return inner

    def compile(self, model) -> CompiledStateGraph:
        self.model = model
        for agent in self.agents.values():
            agent.compile(model)
        graph = StateGraph(AgentState)
        graph.add_node("supervisor", self.supervisor_node)
        graph.add_node("google_tasks", self.agent_node('google_tasks'))
        graph.add_node('google_calendar', self.agent_node('google_calendar'))
        graph.add_node('enhancer', self.agent_node('enhancer'))
        graph.add_edge(START, 'supervisor')

        return graph.compile()

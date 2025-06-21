import yaml
from abc import ABC, abstractmethod
from typing import Dict
from multi_agent_functions.v2.agent.state import AgentState
from langchain_core.messages import SystemMessage

class BaseAgent:
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt

    def compile(self, model) -> None:
        self.model = model
    
    def invoke(self, state: AgentState) -> AgentState:
        messages = [
            SystemMessage(self.system_prompt)
        ] + state['messages']

        response = self.model.invoke(messages)
        state['messages'].append(response)
        return state


    @classmethod
    def create_agent(cls, name: str, system_prompt: str) -> "BaseAgent":
        match(name):
            case "google_tasks":
                from .google_tasks_agent import GoogleTasksAgent
                return GoogleTasksAgent(name, system_prompt)
            case "google_calendar":
                from .google_calendar_agent import GoogleCalendarAgent
                return GoogleCalendarAgent(name, system_prompt)
        return cls(name, system_prompt)
    
    @classmethod
    def load_all(cls) -> Dict[str, "BaseAgent"]:
        agents = {}
        agents_file_path = "agents.yaml" # Path relative to the current working directory

        try:
            with open(agents_file_path, 'r') as f:
                agent_data_list = yaml.safe_load(f)

            if not isinstance(agent_data_list, list):
                print(f"Warning: Expected a list of agents in {agents_file_path}, but got {type(agent_data_list)}")
                return agents # Return empty dict if format is unexpected

            for agent_data in agent_data_list:
                if isinstance(agent_data, dict) and 'name' in agent_data and 'system_prompt' in agent_data:
                    agent_name = agent_data['name']
                    system_prompt = agent_data['system_prompt']
                    agents[agent_name] = cls.create_agent(agent_name, system_prompt)
                else:
                    print(f"Warning: Skipping invalid agent entry in {agents_file_path}: {agent_data}")

        except FileNotFoundError:
            print(f"Error: {agents_file_path} not found.")
        except yaml.YAMLError as e:
            print(f"Error parsing {agents_file_path}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while loading agents: {e}")

        return agents

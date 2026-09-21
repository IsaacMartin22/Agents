from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Type

from .base import AgentContext, AgentResult, BaseAgent


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: Dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> BaseAgent:
        self._agents[agent.name] = agent
        return agent

    def register_many(self, agents: Iterable[BaseAgent]) -> None:
        for agent in agents:
            self.register(agent)

    def get(self, name: str) -> Optional[BaseAgent]:
        return self._agents.get(name)

    def list_agents(self) -> List[str]:
        return sorted(self._agents.keys())

    def run(self, name: str, context: AgentContext) -> AgentResult:
        agent = self.get(name)
        if agent is None:
            raise KeyError(f"Unknown agent: {name}")
        if not agent.supports_event(context.event_name):
            raise ValueError(f"Agent '{name}' does not support event '{context.event_name}'")
        return agent.run(context)

    def available_agents(self) -> Dict[str, str]:
        return {name: agent.description for name, agent in sorted(self._agents.items())}

    @classmethod
    def from_agents(cls, agent_types: Iterable[Type[BaseAgent]]) -> "AgentRegistry":
        registry = cls()
        for agent_type in agent_types:
            registry.register(agent_type())
        return registry

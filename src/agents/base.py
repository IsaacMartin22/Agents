from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from .llm import OpenAIClient


@dataclass
class AgentContext:
    repo: str = ""
    event_name: str = ""
    ref: str = ""
    sha: str = ""
    pr_number: Optional[int] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    agent_name: str
    status: str
    summary: str
    details: Dict[str, Any] = field(default_factory=dict)


class BaseAgent:
    """Common interface for all agents in this repository."""

    name = "base-agent"
    description = "Base agent implementation"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.llm = OpenAIClient(self.config)

    def run(self, context: AgentContext) -> AgentResult:
        raise NotImplementedError("Agent implementations must provide a run(context) method.")

    def supports_event(self, event_name: str) -> bool:
        return True

    def generate_summary(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        response = self.llm.generate(prompt, system_prompt=system_prompt)
        return response.strip() if response else "No summary generated."

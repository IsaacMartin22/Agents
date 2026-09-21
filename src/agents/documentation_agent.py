from __future__ import annotations

from .base import AgentContext, AgentResult, BaseAgent


class DocumentationAgent(BaseAgent):
    name = "documentation-agent"
    description = "Checks whether a pull request likely needs documentation updates."

    def run(self, context: AgentContext) -> AgentResult:
        system_prompt = (
            "You are a senior technical writer reviewing a software pull request. "
            "Assess whether the change likely requires documentation updates and keep the output concise."
        )
        prompt = (
            f"Repository: {context.repo}\n"
            f"Event: {context.event_name}\n"
            f"PR number: {context.pr_number}\n"
            "Review the likely impact on end-user or contributor-facing documentation. "
            "State whether docs should be updated and what sections are most relevant."
        )
        summary = self.generate_summary(prompt, system_prompt=system_prompt)
        return AgentResult(
            agent_name=self.name,
            status="queued",
            summary=summary,
            details={
                "event_name": context.event_name,
                "repo": context.repo,
                "pr_number": context.pr_number,
                "checks": ["diff review", "doc-scope analysis", "update recommendation"],
                "uses_openai": self.llm.is_configured(),
            },
        )

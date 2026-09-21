from __future__ import annotations

from .base import AgentContext, AgentResult, BaseAgent


class SecurityAgent(BaseAgent):
    name = "security-agent"
    description = "Performs a security-focused review for risky pull request changes."

    def run(self, context: AgentContext) -> AgentResult:
        system_prompt = (
            "You are a security reviewer focused on application and infrastructure safety. "
            "Highlight likely risks without over-claiming. Keep the response concise but actionable."
        )
        prompt = (
            f"Repository: {context.repo}\n"
            f"Event: {context.event_name}\n"
            f"PR number: {context.pr_number}\n"
            "Review the change for likely security issues, risky dependency or config changes, and unsafe patterns."
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
                "checks": ["secret scan", "unsafe pattern detection", "dependency risk review"],
                "uses_openai": self.llm.is_configured(),
            },
        )

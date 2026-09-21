from __future__ import annotations

from .base import AgentContext, AgentResult, BaseAgent


class CodeReviewAgent(BaseAgent):
    name = "code-review-agent"
    description = "Applies a general-purpose code review pass for pull requests."

    def run(self, context: AgentContext) -> AgentResult:
        system_prompt = (
            "You are a senior software engineer reviewing a pull request. Focus on correctness, "
            "maintainability, and code safety. Keep the output practical and concise."
        )
        prompt = (
            f"Repository: {context.repo}\n"
            f"Event: {context.event_name}\n"
            f"PR number: {context.pr_number}\n"
            "Review the change for likely correctness risks, maintainability issues, and any engineering concerns."
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
                "checks": ["risk review", "maintainability scan", "behavioral summary"],
                "uses_openai": self.llm.is_configured(),
            },
        )

import os
import unittest
from unittest.mock import patch

from agents.base import AgentContext
from agents.code_review_agent import CodeReviewAgent
from agents.documentation_agent import DocumentationAgent
from agents.llm import OpenAIClient
from agents.registry import AgentRegistry
from agents.security_agent import SecurityAgent


class TestAgentRegistry(unittest.TestCase):
    def test_registry_contains_expected_agents(self):
        registry = AgentRegistry.from_agents([
            DocumentationAgent,
            CodeReviewAgent,
            SecurityAgent,
        ])

        self.assertEqual(
            registry.list_agents(),
            ["code-review-agent", "documentation-agent", "security-agent"],
        )

    def test_run_returns_result(self):
        registry = AgentRegistry.from_agents([
            DocumentationAgent,
        ])
        context = AgentContext(repo="demo/repo", event_name="pull_request", pr_number=42)

        result = registry.run("documentation-agent", context)

        self.assertEqual(result.agent_name, "documentation-agent")
        self.assertEqual(result.status, "queued")
        self.assertIn("API is not configured", result.summary)

    def test_openai_client_handles_missing_key_gracefully(self):
        with patch.dict(os.environ, {}, clear=True):
            client = OpenAIClient()
            self.assertFalse(client.is_configured())
            self.assertIn("OPENAI_API_KEY", client.generate("hello"))


if __name__ == "__main__":
    unittest.main()

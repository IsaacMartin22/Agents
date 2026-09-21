from __future__ import annotations

import argparse
import json
from typing import Optional

from .base import AgentContext
from .code_review_agent import CodeReviewAgent
from .documentation_agent import DocumentationAgent
from .registry import AgentRegistry
from .security_agent import SecurityAgent


def build_registry() -> AgentRegistry:
    return AgentRegistry.from_agents([
        DocumentationAgent,
        CodeReviewAgent,
        SecurityAgent,
    ])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run or inspect the repository's agent registry.")
    parser.add_argument("--list", action="store_true", help="List available agents")
    parser.add_argument("--run", action="store_true", help="Run a named agent")
    parser.add_argument("--agent", help="Agent name to run", default="documentation-agent")
    parser.add_argument("--event", help="Event name for the agent context", default="manual")
    parser.add_argument("--repo", help="Repository identifier", default="demo/repo")
    parser.add_argument("--sha", help="Commit or SHA to associate with the run", default="")
    parser.add_argument("--ref", help="Git ref for the run", default="")
    parser.add_argument("--pr-number", type=int, default=None, help="Pull request number, if applicable")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    registry = build_registry()

    if args.list:
        for name, description in registry.available_agents().items():
            print(f"{name}: {description}")
        return 0

    if args.run:
        context = AgentContext(
            repo=args.repo,
            event_name=args.event,
            ref=args.ref,
            sha=args.sha,
            pr_number=args.pr_number,
            payload={"agent": args.agent},
            metadata={"source": "cli"},
        )

        result = registry.run(args.agent, context)
        print(json.dumps({
            "agent": result.agent_name,
            "status": result.status,
            "summary": result.summary,
            "details": result.details,
        }, indent=2, sort_keys=True))
        return 0

    print("No command specified. Use --list or --run.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

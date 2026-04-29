from __future__ import annotations

import re

from app.agents.base import Agent
from app.models import Event


class IntakeAgent(Agent):
    name = "intake-agent"
    subscribes_to = ("run.started",)

    async def handle(self, ctx: "RunContext", event: Event) -> list[Event]:
        prompt = str(event.payload["prompt"])
        sentences = [item.strip() for item in re.split(r"[。\n!?；;]+", prompt) if item.strip()]
        acceptance_criteria = sentences[:5]
        if "可观测" not in "".join(acceptance_criteria):
            acceptance_criteria.append("提供全链路日志、阶段追踪与失败定位能力")
        if "部署" not in "".join(acceptance_criteria):
            acceptance_criteria.append("输出可直接落地的 CI/CD 与 GitOps 配置")

        capability_map = {
            "多智能体": "event-driven multi-agent orchestration",
            "长链": "long-chain execution planning",
            "代码": "code scaffold generation",
            "部署": "GitOps delivery generation",
            "测试": "quality gate planning",
            "日志": "traceable execution log",
            "仓库": "repository-wide impact analysis",
        }
        capabilities = [value for key, value in capability_map.items() if key in prompt]
        if not capabilities:
            capabilities = [
                "repository-wide impact analysis",
                "multi-agent planning",
                "production delivery templates",
            ]

        llm_note = await ctx.llm.complete(
            "You summarize software-delivery requirements for a long-context agent platform.",
            prompt,
        )

        requirements = {
            "problem_statement": sentences[0] if sentences else prompt[:120],
            "acceptance_criteria": acceptance_criteria,
            "key_capabilities": capabilities,
            "llm_note": llm_note,
        }
        ctx.run.state["requirements"] = requirements
        body = "\n".join(f"- {item}" for item in acceptance_criteria)
        ctx.write_artifact(
            "analysis/requirements.md",
            f"# Requirement Brief\n\n## Problem Statement\n{requirements['problem_statement']}\n\n## Acceptance Criteria\n{body}\n\n## Capability Signals\n"
            + "\n".join(f"- {item}" for item in capabilities)
            + f"\n\n## Long-Context Note\n{llm_note}\n",
            title="Requirement Brief",
            kind="markdown",
        )
        return [Event.create("requirements.parsed", self.name, requirements)]


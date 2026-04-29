from __future__ import annotations

from app.agents.base import Agent
from app.models import Event


class TestDesignerAgent(Agent):
    name = "test-designer-agent"
    subscribes_to = ("scaffold.generated",)

    async def handle(self, ctx: "RunContext", event: Event) -> list[Event]:
        architecture = ctx.run.state["architecture"]
        files = list(event.payload.get("files", []))
        criteria = ctx.run.state["requirements"]["acceptance_criteria"]
        content = (
            "# Quality Plan\n\n"
            "## Mandatory Gates\n"
            "- unit tests for the health endpoint and critical path orchestration\n"
            "- lint and compile checks on every pull request\n"
            "- golden-file validation for generated deployment manifests\n"
            "- replay test for event traces and final summaries\n\n"
            "## Scenario Coverage\n"
            + "\n".join(f"- {item}" for item in criteria)
            + "\n\n## Generated Surface\n"
            + "\n".join(f"- {item}" for item in files[:12])
            + f"\n\n## Stack Notes\n- stack: {architecture['stack']}\n"
        )
        ctx.write_artifact("quality/TESTPLAN.md", content, title="Quality Plan", kind="markdown")
        return [Event.create("tests.generated", self.name, {"quality_plan": "created"})]


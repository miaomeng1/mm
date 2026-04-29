from __future__ import annotations

from app.agents.base import Agent
from app.models import Event
from app.services.validators import ValidatorSuite


class GuardAgent(Agent):
    name = "guard-agent"
    subscribes_to = ("delivery.generated",)

    def __init__(self, validators: ValidatorSuite) -> None:
        self.validators = validators

    async def handle(self, ctx: "RunContext", event: Event) -> list[Event]:
        del event
        report = self.validators.validate(ctx.run.state)
        ctx.run.state["guard_report"] = report
        ctx.run.summary = (
            "MimoForge completed a long-context delivery run with "
            f"{len(ctx.run.artifacts)} artifacts, stack `{ctx.run.state['architecture']['stack']}`, "
            f"and validator verdict `{report['verdict']}`."
        )
        ctx.write_artifact(
            "quality/GUARD_REPORT.md",
            "# Guard Report\n\n## Verdict\n"
            f"- {report['verdict']}\n\n## Checks\n"
            + "\n".join(f"- {item}" for item in report["checks"])
            + "\n\n## Issues\n"
            + ("\n".join(f"- {item}" for item in report["issues"]) if report["issues"] else "- none"),
            title="Guard Report",
            kind="markdown",
        )
        return [Event.create("run.completed", self.name, report)]


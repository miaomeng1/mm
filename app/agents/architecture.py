from __future__ import annotations

from app.agents.base import Agent
from app.models import Event
from app.utils import slugify


class ArchitectureAgent(Agent):
    name = "architecture-agent"
    subscribes_to = ("repo.mapped",)

    async def handle(self, ctx: "RunContext", event: Event) -> list[Event]:
        del event
        requirements = ctx.run.state["requirements"]
        repo_context = ctx.run.state["repo_context"]
        prompt = ctx.run.prompt.lower()
        preferred = (ctx.run.preferred_stack or "").lower()

        stack = "fastapi"
        if preferred in {"fastapi", "go-gin", "spring-boot"}:
            stack = preferred
        elif "java" in prompt or "spring" in prompt:
            stack = "spring-boot"
        elif "go" in prompt or "gin" in prompt or "golang" in prompt:
            stack = "go-gin"
        elif isinstance(repo_context, dict):
            languages = repo_context.get("languages", {})
            if isinstance(languages, dict):
                if "Java" in languages:
                    stack = "spring-boot"
                elif "Go" in languages:
                    stack = "go-gin"

        service_name = slugify(ctx.run.project_name)
        architecture = {
            "stack": stack,
            "service_name": service_name,
            "north_star": "turn million-token context into executable software delivery decisions",
            "modules": [
                "Requirement ingestion and acceptance criteria extraction",
                "Repository-wide context mapping and impact inference",
                "Stack-aware scaffold generation",
                "Quality plan synthesis and risk gating",
                "GitHub Actions + ArgoCD delivery pack",
            ],
            "moats": [
                "single-pass ingestion of PRD, repo tree, CI logs, ADRs, and manifests",
                "event-driven agent isolation with replayable traces",
                "cross-stack scaffolding for Python, Go, and Java delivery paths",
            ],
            "success_metrics": [
                "requirement coverage ratio",
                "cross-file impact recall",
                "deployment template pass rate",
                "mean time to first runnable artifact",
            ],
            "key_capabilities": requirements["key_capabilities"],
        }
        ctx.run.state["architecture"] = architecture

        ctx.write_artifact(
            "plans/solution_blueprint.md",
            "# Solution Blueprint\n\n"
            f"## Stack\n- selected: {stack}\n- service_name: {service_name}\n\n"
            "## Modules\n"
            + "\n".join(f"- {item}" for item in architecture["modules"])
            + "\n\n## Competitive Moat\n"
            + "\n".join(f"- {item}" for item in architecture["moats"])
            + "\n\n## Success Metrics\n"
            + "\n".join(f"- {item}" for item in architecture["success_metrics"])
            + "\n",
            title="Solution Blueprint",
            kind="markdown",
        )
        return [Event.create("architecture.designed", self.name, architecture)]


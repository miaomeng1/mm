from __future__ import annotations

from app.agents.base import Agent
from app.models import Event
from app.services.project_writer import ProjectWriter, ScaffoldSpec
from app.utils import slugify


class ScaffoldAgent(Agent):
    name = "scaffold-agent"
    subscribes_to = ("architecture.designed",)

    def __init__(self, writer: ProjectWriter) -> None:
        self.writer = writer

    async def handle(self, ctx: "RunContext", event: Event) -> list[Event]:
        architecture = event.payload
        requirements = ctx.run.state["requirements"]
        project_slug = slugify(ctx.run.project_name)
        spec = ScaffoldSpec(
            project_name=ctx.run.project_name,
            service_name=str(architecture["service_name"]),
            stack=str(architecture["stack"]),
            project_slug=project_slug,
            acceptance_criteria=list(requirements["acceptance_criteria"]),
            key_capabilities=list(requirements["key_capabilities"]),
        )
        files = self.writer.build(spec)
        for path, content in files.items():
            ctx.write_artifact(path, content, title=path.split("/")[-1], kind="code")

        generated_files = sorted(files.keys())
        ctx.run.state["generated_files"] = generated_files
        return [Event.create("scaffold.generated", self.name, {"files": generated_files})]


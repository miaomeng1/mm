from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import uuid4

from app.config import Settings
from app.models import Artifact, Event, RunRecord
from app.store import RunStore
from app.utils import utc_now


@dataclass(slots=True)
class RunContext:
    settings: Settings
    store: RunStore
    llm: Any
    run: RunRecord
    output_dir: Path

    def write_artifact(self, relative_path: str, content: str, title: str, kind: str) -> None:
        target = self.output_dir / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        preview = content[:240]

        artifact = Artifact(path=relative_path, title=title, kind=kind, preview=preview)
        self.run.artifacts = [item for item in self.run.artifacts if item.path != relative_path]
        self.run.artifacts.append(artifact)
        self.run.updated_at = utc_now()
        self.store.save_run(self.run)


class Orchestrator:
    def __init__(self, settings: Settings, store: RunStore, llm: Any, agents: list[Any]) -> None:
        self.settings = settings
        self.store = store
        self.llm = llm
        self.handlers: dict[str, list[Any]] = defaultdict(list)
        for agent in agents:
            for event_type in agent.subscribes_to:
                self.handlers[event_type].append(agent)

    async def execute(
        self,
        project_name: str,
        prompt: str,
        target_repo: str | None = None,
        preferred_stack: str | None = None,
    ) -> RunRecord:
        now = utc_now()
        run = RunRecord(
            id=str(uuid4()),
            project_name=project_name,
            prompt=prompt,
            target_repo=target_repo,
            preferred_stack=preferred_stack,
            status="running",
            created_at=now,
            updated_at=now,
            summary="",
            state={},
        )
        ctx = RunContext(
            settings=self.settings,
            store=self.store,
            llm=self.llm,
            run=run,
            output_dir=self.store.artifact_root(run.id),
        )
        self.store.save_run(run)

        queue: deque[Event] = deque(
            [
                Event.create(
                    "run.started",
                    "orchestrator",
                    {
                        "project_name": project_name,
                        "prompt": prompt,
                        "target_repo": target_repo,
                        "preferred_stack": preferred_stack,
                    },
                )
            ]
        )

        try:
            while queue:
                event = queue.popleft()
                run.events.append(event)
                run.updated_at = utc_now()
                self.store.save_run(run)

                for handler in self.handlers.get(event.type, []):
                    produced = await handler.handle(ctx, event)
                    queue.extend(produced)

            run.status = "completed"
            run.updated_at = utc_now()
            self.store.save_run(run)
            return run
        except Exception as exc:
            run.status = "failed"
            run.summary = f"Run failed: {exc}"
            run.events.append(
                Event.create(
                    "run.failed",
                    "orchestrator",
                    {"error": str(exc)},
                )
            )
            run.updated_at = utc_now()
            self.store.save_run(run)
            raise


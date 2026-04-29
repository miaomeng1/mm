from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any
from uuid import uuid4

from app.utils import utc_now


@dataclass(slots=True)
class Event:
    id: str
    type: str
    source: str
    payload: dict[str, Any]
    created_at: str

    @classmethod
    def create(cls, event_type: str, source: str, payload: dict[str, Any] | None = None) -> "Event":
        return cls(
            id=str(uuid4()),
            type=event_type,
            source=source,
            payload=payload or {},
            created_at=utc_now(),
        )


@dataclass(slots=True)
class Artifact:
    path: str
    title: str
    kind: str
    preview: str


@dataclass(slots=True)
class RunRecord:
    id: str
    project_name: str
    prompt: str
    target_repo: str | None
    preferred_stack: str | None
    status: str
    created_at: str
    updated_at: str
    summary: str
    events: list[Event] = field(default_factory=list)
    artifacts: list[Artifact] = field(default_factory=list)
    state: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "project_name": self.project_name,
            "prompt": self.prompt,
            "target_repo": self.target_repo,
            "preferred_stack": self.preferred_stack,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "summary": self.summary,
            "events": [asdict(event) for event in self.events],
            "artifacts": [asdict(artifact) for artifact in self.artifacts],
            "state": self.state,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RunRecord":
        return cls(
            id=data["id"],
            project_name=data["project_name"],
            prompt=data["prompt"],
            target_repo=data.get("target_repo"),
            preferred_stack=data.get("preferred_stack"),
            status=data["status"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            summary=data.get("summary", ""),
            events=[Event(**event) for event in data.get("events", [])],
            artifacts=[Artifact(**artifact) for artifact in data.get("artifacts", [])],
            state=data.get("state", {}),
        )


from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from app.models import Event

if TYPE_CHECKING:
    from app.orchestrator import RunContext


class Agent(ABC):
    name: str
    subscribes_to: tuple[str, ...]

    @abstractmethod
    async def handle(self, ctx: "RunContext", event: Event) -> list[Event]:
        raise NotImplementedError

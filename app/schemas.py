from __future__ import annotations

from pydantic import BaseModel, Field


class RunCreate(BaseModel):
    project_name: str = Field(min_length=3, max_length=80)
    prompt: str = Field(min_length=30, max_length=12000)
    target_repo: str | None = None
    preferred_stack: str | None = None


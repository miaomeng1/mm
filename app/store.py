from __future__ import annotations

import json
from pathlib import Path

from app.models import RunRecord


class RunStore:
    def __init__(self, runs_dir: Path, generated_dir: Path) -> None:
        self.runs_dir = runs_dir
        self.generated_dir = generated_dir
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        self.generated_dir.mkdir(parents=True, exist_ok=True)

    def save_run(self, run: RunRecord) -> None:
        path = self.runs_dir / f"{run.id}.json"
        path.write_text(
            json.dumps(run.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def load_run(self, run_id: str) -> RunRecord | None:
        path = self.runs_dir / f"{run_id}.json"
        if not path.exists():
            return None
        return RunRecord.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def list_runs(self) -> list[RunRecord]:
        runs: list[RunRecord] = []
        for path in sorted(self.runs_dir.glob("*.json")):
            runs.append(RunRecord.from_dict(json.loads(path.read_text(encoding="utf-8"))))
        runs.sort(key=lambda item: item.updated_at, reverse=True)
        return runs

    def artifact_root(self, run_id: str) -> Path:
        path = self.generated_dir / run_id
        path.mkdir(parents=True, exist_ok=True)
        return path


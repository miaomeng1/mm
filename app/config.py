from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Settings:
    app_name: str
    data_dir: Path
    runs_dir: Path
    generated_dir: Path
    enable_llm: bool
    llm_base_url: str | None
    llm_api_key: str | None
    llm_model: str


def load_settings(root: Path | None = None) -> Settings:
    project_root = root or Path(__file__).resolve().parents[1]
    data_dir = Path(os.getenv("MIMOFORGE_DATA_DIR", project_root / "data")).resolve()
    runs_dir = data_dir / "runs"
    generated_dir = data_dir / "generated"
    runs_dir.mkdir(parents=True, exist_ok=True)
    generated_dir.mkdir(parents=True, exist_ok=True)

    enable_llm = os.getenv("MIMOFORGE_ENABLE_LLM", "false").lower() == "true"
    return Settings(
        app_name="MimoForge",
        data_dir=data_dir,
        runs_dir=runs_dir,
        generated_dir=generated_dir,
        enable_llm=enable_llm,
        llm_base_url=os.getenv("MIMOFORGE_LLM_BASE_URL"),
        llm_api_key=os.getenv("MIMOFORGE_LLM_API_KEY"),
        llm_model=os.getenv("MIMOFORGE_LLM_MODEL", "gpt-4.1-mini"),
    )


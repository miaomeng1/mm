from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from app.bootstrap import build_orchestrator
from app.schemas import RunCreate

settings, store, orchestrator = build_orchestrator()
static_dir = Path(__file__).resolve().parent / "static"

app = FastAPI(title="MimoForge", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    return (static_dir / "index.html").read_text(encoding="utf-8")


@app.get("/api/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}


@app.get("/api/runs")
async def list_runs() -> list[dict[str, object]]:
    return [run.to_dict() for run in store.list_runs()]


@app.get("/api/runs/{run_id}")
async def get_run(run_id: str) -> dict[str, object]:
    run = store.load_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="run not found")
    return run.to_dict()


@app.get("/api/runs/{run_id}/artifacts/{artifact_path:path}", response_class=PlainTextResponse)
async def get_artifact(run_id: str, artifact_path: str) -> str:
    run = store.load_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="run not found")

    root = store.artifact_root(run_id).resolve()
    target = (root / artifact_path).resolve()
    if root not in target.parents and target != root:
        raise HTTPException(status_code=400, detail="invalid artifact path")
    if not target.exists():
        raise HTTPException(status_code=404, detail="artifact not found")
    return target.read_text(encoding="utf-8")


@app.post("/api/runs")
async def create_run(payload: RunCreate) -> dict[str, object]:
    run = await orchestrator.execute(
        project_name=payload.project_name,
        prompt=payload.prompt,
        target_repo=payload.target_repo,
        preferred_stack=payload.preferred_stack,
    )
    return run.to_dict()

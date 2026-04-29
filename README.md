# MimoForge

MimoForge is a GitHub-ready demo for a long-context, multi-agent software-delivery platform designed around the exact value proposition of a million-token model. Instead of stopping at code snippets, it turns a natural-language requirement plus an optional linked repository into a full delivery pack: requirement brief, repository context summary, solution blueprint, runnable starter code, quality plan, GitHub Actions workflow, ArgoCD manifest, and guard report.

![status](https://img.shields.io/badge/status-demo-orange)
![python](https://img.shields.io/badge/python-3.11+-blue)
![license](https://img.shields.io/badge/license-MIT-green)

## Why This Project Is Competitive

Most AI coding demos are still local optimizers: they see part of a prompt, emit part of a patch, and fail once the problem spans multiple modules, documents, environments, and deployment constraints. MimoForge is built around the opposite assumption: real engineering work is fundamentally long-context and multi-stage.

Its moat is not just "multi-agent". The moat is:

- one execution chain that can unify PRD, repo context, CI logs, architecture notes, and deploy manifests
- event-driven specialization across seven agents with replayable traces
- runnable scaffold generation for multiple stacks
- quality and GitOps artifacts as first-class outputs instead of afterthoughts

## Core Features

1. Event-driven seven-agent pipeline:
   `Intake -> ContextMap -> Architecture -> Scaffold -> TestDesigner -> Delivery -> Guard`
2. Long-context software-delivery framing:
   the system is explicitly optimized for repository-wide and lifecycle-wide reasoning.
3. Multi-stack artifact generation:
   built-in starters for `FastAPI`, `Go + Gin`, and `Spring Boot`.
4. GitHub-ready ops outputs:
   `GitHub Actions`, `Kubernetes`, `ArgoCD`, and release checklist templates.
5. Demo-friendly control plane:
   a polished web UI displays event timeline and generated artifacts.

## Architecture

```text
Natural-language prompt
        |
        v
  IntakeAgent ----------------------+
        |                           |
        v                           |
  ContextMapAgent <-- linked repo --+
        |
        v
  ArchitectureAgent
        |
        v
  ScaffoldAgent
        |
        v
  TestDesignerAgent
        |
        v
  DeliveryAgent
        |
        v
  GuardAgent
        |
        v
  Artifacts + Run Summary + Trace
```

## Quick Start

### Local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install .
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open `http://127.0.0.1:8000`.

### Docker

```bash
docker compose up --build
```

## API

### `POST /api/runs`

```json
{
  "project_name": "Enterprise Delivery Copilot",
  "prompt": "我想做一个面向复杂软件工程团队的多智能体交付平台，要求支持长链推理、仓库级别上下文分析、代码骨架生成、测试规划、GitHub Actions、ArgoCD 自动部署，并且需要清晰日志和失败回放。",
  "target_repo": "/path/to/existing/repo",
  "preferred_stack": "fastapi"
}
```

### `GET /api/runs`

Lists historical runs.

### `GET /api/runs/{run_id}`

Returns the full run timeline, summary, state, and artifact index.

### `GET /api/runs/{run_id}/artifacts/{artifact_path}`

Returns the raw content of a generated artifact.

## Repository Structure

```text
MimoForge/
├── app/
│   ├── agents/
│   ├── services/
│   ├── static/
│   ├── bootstrap.py
│   ├── main.py
│   └── orchestrator.py
├── docs/
│   ├── architecture.md
│   └── mimo_application.md
├── tests/
├── .github/workflows/ci.yml
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Example Outputs

Each run writes a structured artifact pack under `data/generated/<run_id>/`:

- `analysis/requirements.md`
- `analysis/repo_context.md`
- `plans/solution_blueprint.md`
- `scaffold/<project>/...`
- `quality/TESTPLAN.md`
- `quality/GUARD_REPORT.md`
- `delivery/github-actions.yml`
- `delivery/argocd-application.yaml`
- `delivery/release-checklist.md`

## Tests

```bash
python -m unittest discover -s tests -p "test_*.py"
python -m compileall app tests
```

## Application Narrative

If you are using this repository for the Xiaomi MIMO million-token application, start with [docs/mimo_application.md](docs/mimo_application.md). It contains a submission-ready narrative in Chinese explaining:

- what problem the project solves
- why million-token context is necessary
- what the technical architecture is
- where the innovation and moat come from
- how the project can evolve after receiving access

## Notes

- By default, the app uses a mock synthesis provider for deterministic demos.
- If you want to plug in a real OpenAI-compatible model endpoint, fill in `.env.example`.
- The project is intentionally designed to be understandable in one sitting while still feeling like a real software-delivery control plane, not just a landing page around prompt engineering.


# MimoForge Architecture

## System Shape

MimoForge is built as an event-driven software-delivery control plane.

1. `IntakeAgent` extracts problem statements, acceptance criteria, and long-context signals.
2. `ContextMapAgent` scans a linked repository and compresses the codebase into planning signals.
3. `ArchitectureAgent` chooses a delivery stack and defines the system moat.
4. `ScaffoldAgent` emits runnable starter code and deployment manifests.
5. `TestDesignerAgent` translates product goals into quality gates.
6. `DeliveryAgent` produces GitHub Actions and ArgoCD templates.
7. `GuardAgent` validates the run and emits a final verdict.

## Why Long Context Matters

Most code-generation demos only reason over the current prompt. Real software delivery needs a unified view across:

- PRD and acceptance criteria
- Existing repository topology
- Historical deployment failures
- CI logs and flaky tests
- Kubernetes manifests and GitOps policies
- ADRs, coding conventions, and team standards

MimoForge is designed to use that combined context in one execution chain rather than fragmenting it into shallow prompt hops.

## Repository Layout

- `app/main.py`: FastAPI entrypoint and HTTP API.
- `app/orchestrator.py`: event queue, run state, artifact persistence.
- `app/agents/`: seven specialized agents.
- `app/services/`: repository analysis, scaffold generation, validation.
- `app/static/`: lightweight single-page dashboard.
- `docs/mimo_application.md`: GitHub-ready application narrative for the MIMO token program.


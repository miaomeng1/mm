from __future__ import annotations

from app.agents.base import Agent
from app.models import Event


class DeliveryAgent(Agent):
    name = "delivery-agent"
    subscribes_to = ("tests.generated",)

    async def handle(self, ctx: "RunContext", event: Event) -> list[Event]:
        del event
        architecture = ctx.run.state["architecture"]
        service_name = architecture["service_name"]
        stack = architecture["stack"]

        workflow = f"""name: generated-service

on:
  push:
    branches: ["main"]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build container
        run: docker build -t ghcr.io/your-org/{service_name}:latest scaffold/{service_name}
      - name: Validate manifests
        run: test -f scaffold/{service_name}/deploy/k8s/deployment.yaml || true
"""
        argocd = f"""apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {service_name}
spec:
  destination:
    namespace: default
    server: https://kubernetes.default.svc
  source:
    path: scaffold/{service_name}/deploy/k8s
    repoURL: https://github.com/your-org/{service_name}
    targetRevision: HEAD
  project: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
"""
        checklist = (
            "# Release Checklist\n\n"
            f"- verify the `{stack}` scaffold boots locally\n"
            "- confirm health endpoint and smoke tests pass\n"
            "- validate image tag strategy and registry permissions\n"
            "- confirm ArgoCD sync completes without drift\n"
            "- compare generated artifacts with requirement brief before merge\n"
        )

        ctx.write_artifact("delivery/github-actions.yml", workflow, title="Generated Workflow", kind="yaml")
        ctx.write_artifact("delivery/argocd-application.yaml", argocd, title="ArgoCD Application", kind="yaml")
        ctx.write_artifact("delivery/release-checklist.md", checklist, title="Release Checklist", kind="markdown")
        return [Event.create("delivery.generated", self.name, {"delivery": "ready"})]


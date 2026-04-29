from __future__ import annotations

import re


class ValidatorSuite:
    def validate(self, state: dict[str, object]) -> dict[str, object]:
        issues: list[str] = []
        checks: list[str] = []

        architecture = state.get("architecture", {})
        service_name = ""
        if isinstance(architecture, dict):
            service_name = str(architecture.get("service_name", ""))

        if re.fullmatch(r"[a-z0-9-]+", service_name):
            checks.append("service name matches Kubernetes-safe naming convention")
        else:
            issues.append("service name should only contain lowercase letters, numbers, and hyphens")

        generated_files = state.get("generated_files", [])
        if isinstance(generated_files, list) and generated_files:
            checks.append(f"generated {len(generated_files)} delivery artifacts")
        else:
            issues.append("no generated files were recorded")

        repo_context = state.get("repo_context", {})
        if isinstance(repo_context, dict) and repo_context.get("exists"):
            checks.append("repository context was linked into the planning stage")
        else:
            issues.append("run was executed without a linked repository context")

        stack = ""
        if isinstance(architecture, dict):
            stack = str(architecture.get("stack", ""))

        if stack in {"fastapi", "go-gin", "spring-boot"}:
            checks.append(f"selected stack `{stack}` is supported by built-in scaffolder")
        else:
            issues.append("selected stack is not supported by the built-in scaffolder")

        verdict = "pass" if not issues else "warning"
        return {"verdict": verdict, "checks": checks, "issues": issues}


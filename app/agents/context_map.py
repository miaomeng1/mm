from __future__ import annotations

from app.agents.base import Agent
from app.models import Event
from app.services.repo_analyzer import RepoAnalyzer


class ContextMapAgent(Agent):
    name = "context-map-agent"
    subscribes_to = ("requirements.parsed",)

    def __init__(self, analyzer: RepoAnalyzer) -> None:
        self.analyzer = analyzer

    async def handle(self, ctx: "RunContext", event: Event) -> list[Event]:
        del event
        repo_context = self.analyzer.analyze(ctx.run.target_repo)
        ctx.run.state["repo_context"] = repo_context

        language_lines = "\n".join(
            f"- {name}: {count} files" for name, count in dict(repo_context.get("languages", {})).items()
        ) or "- no repository linked"
        tree_lines = "\n".join(f"- {item}" for item in list(repo_context.get("tree_excerpt", []))[:20]) or "- n/a"
        signal_lines = "\n".join(f"- {item}" for item in list(repo_context.get("signals", []))) or "- n/a"
        ctx.write_artifact(
            "analysis/repo_context.md",
            f"# Repository Context\n\n## Repo\n- name: {repo_context.get('repo_name')}\n- exists: {repo_context.get('exists')}\n- files: {repo_context.get('file_count')}\n\n## Languages\n{language_lines}\n\n## Signals\n{signal_lines}\n\n## Tree Excerpt\n{tree_lines}\n",
            title="Repository Context",
            kind="markdown",
        )
        return [Event.create("repo.mapped", self.name, repo_context)]


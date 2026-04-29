from __future__ import annotations

from collections import Counter
from pathlib import Path


IGNORED_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    ".venv",
    "venv",
}

EXTENSION_LANGUAGE_MAP = {
    ".py": "Python",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".go": "Go",
    ".java": "Java",
    ".kt": "Kotlin",
    ".rs": "Rust",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".json": "JSON",
    ".md": "Markdown",
}


class RepoAnalyzer:
    def analyze(self, repo_path: str | None) -> dict[str, object]:
        if not repo_path:
            return {
                "exists": False,
                "repo_name": "no-linked-repository",
                "file_count": 0,
                "languages": {},
                "key_files": [],
                "tree_excerpt": [],
                "signals": [],
            }

        root = Path(repo_path).expanduser().resolve()
        if not root.exists():
            return {
                "exists": False,
                "repo_name": root.name,
                "file_count": 0,
                "languages": {},
                "key_files": [],
                "tree_excerpt": [],
                "signals": [f"target repo not found: {root}"],
            }

        language_counter: Counter[str] = Counter()
        key_files: list[str] = []
        tree_excerpt: list[str] = []
        signals: list[str] = []
        file_count = 0

        for path in root.rglob("*"):
            if any(part in IGNORED_DIRS for part in path.parts):
                continue
            if path.is_dir():
                continue

            file_count += 1
            rel = path.relative_to(root).as_posix()
            if len(tree_excerpt) < 80:
                tree_excerpt.append(rel)

            language = EXTENSION_LANGUAGE_MAP.get(path.suffix.lower())
            if language:
                language_counter[language] += 1

            if path.name in {"README.md", "package.json", "pyproject.toml", "go.mod", "pom.xml", "Dockerfile"}:
                key_files.append(rel)

        if (root / "package.json").exists():
            signals.append("contains frontend or node-based tooling")
        if (root / "pyproject.toml").exists() or (root / "requirements.txt").exists():
            signals.append("contains Python application surface")
        if (root / "go.mod").exists():
            signals.append("contains Go modules")
        if (root / "pom.xml").exists():
            signals.append("contains Java build configuration")
        if any("k8s" in item or "helm" in item for item in tree_excerpt):
            signals.append("contains deployment manifests")

        return {
            "exists": True,
            "repo_name": root.name,
            "file_count": file_count,
            "languages": dict(language_counter.most_common()),
            "key_files": key_files[:20],
            "tree_excerpt": tree_excerpt,
            "signals": signals,
        }


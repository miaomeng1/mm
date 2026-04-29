from __future__ import annotations

from app.agents.architecture import ArchitectureAgent
from app.agents.context_map import ContextMapAgent
from app.agents.delivery import DeliveryAgent
from app.agents.guard import GuardAgent
from app.agents.intake import IntakeAgent
from app.agents.scaffold import ScaffoldAgent
from app.agents.test_designer import TestDesignerAgent
from app.config import Settings, load_settings
from app.llm import load_llm_provider
from app.orchestrator import Orchestrator
from app.services.project_writer import ProjectWriter
from app.services.repo_analyzer import RepoAnalyzer
from app.services.validators import ValidatorSuite
from app.store import RunStore


def build_orchestrator(settings: Settings | None = None) -> tuple[Settings, RunStore, Orchestrator]:
    resolved = settings or load_settings()
    store = RunStore(resolved.runs_dir, resolved.generated_dir)
    llm = load_llm_provider(resolved)
    analyzer = RepoAnalyzer()
    writer = ProjectWriter()
    validators = ValidatorSuite()
    agents = [
        IntakeAgent(),
        ContextMapAgent(analyzer),
        ArchitectureAgent(),
        ScaffoldAgent(writer),
        TestDesignerAgent(),
        DeliveryAgent(),
        GuardAgent(validators),
    ]
    orchestrator = Orchestrator(resolved, store, llm, agents)
    return resolved, store, orchestrator


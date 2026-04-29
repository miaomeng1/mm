from __future__ import annotations

import asyncio
import tempfile
import unittest
from pathlib import Path

from app.bootstrap import build_orchestrator
from app.config import Settings


class OrchestratorTestCase(unittest.TestCase):
    def test_end_to_end_run_creates_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            settings = Settings(
                app_name="MimoForge",
                data_dir=root / "data",
                runs_dir=root / "data" / "runs",
                generated_dir=root / "data" / "generated",
                enable_llm=False,
                llm_base_url=None,
                llm_api_key=None,
                llm_model="mock",
            )
            _, store, orchestrator = build_orchestrator(settings)
            run = asyncio.run(
                orchestrator.execute(
                    project_name="Repo Control Plane",
                    prompt="构建一个多智能体软件交付平台，要求支持仓库级上下文、代码脚手架生成、测试规划和 GitOps 自动部署。",
                    target_repo=None,
                    preferred_stack="fastapi",
                )
            )

            self.assertEqual(run.status, "completed")
            self.assertGreaterEqual(len(run.events), 7)
            self.assertTrue(any(item.path == "analysis/requirements.md" for item in run.artifacts))
            self.assertTrue((store.artifact_root(run.id) / "quality/GUARD_REPORT.md").exists())


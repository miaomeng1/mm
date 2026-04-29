from __future__ import annotations

import unittest

from app.services.project_writer import ProjectWriter, ScaffoldSpec


class ProjectWriterTestCase(unittest.TestCase):
    def test_fastapi_scaffold_contains_expected_files(self) -> None:
        writer = ProjectWriter()
        spec = ScaffoldSpec(
            project_name="MimoForge Service",
            service_name="mimoforge-service",
            stack="fastapi",
            project_slug="mimoforge-service",
            acceptance_criteria=["产出健康检查接口", "生成部署清单"],
            key_capabilities=["multi-agent orchestration"],
        )
        files = writer.build(spec)
        self.assertIn("scaffold/mimoforge-service/app/main.py", files)
        self.assertIn("scaffold/mimoforge-service/deploy/k8s/deployment.yaml", files)
        self.assertIn("fastapi", files["scaffold/mimoforge-service/requirements.txt"])


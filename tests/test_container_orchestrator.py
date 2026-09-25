from __future__ import annotations
import unittest
import tempfile
import os
from core.container_orchestrator import LinuxContainerOrchestrator
from core.stealth_profile import LinuxStealthProfileGenerator

class TestLinuxContainerOrchestrator(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.orchestrator = LinuxContainerOrchestrator(
            base_data_dir=self.temp_dir,
            memory_limit="512m",
            cpu_quota=0.75
        )
        self.profile = LinuxStealthProfileGenerator.create_profile("docker_test_01")

    def tearDown(self):
        try:
            import shutil
            shutil.rmtree(self.temp_dir)
        except Exception:
            pass

    def test_build_docker_run_command(self):
        cmd = self.orchestrator.build_docker_run_command(self.profile, cdp_port=9230)
        self.assertIn("docker", cmd)
        self.assertIn("run", cmd)
        self.assertIn("--memory", cmd)
        self.assertIn("512m", cmd)
        self.assertIn("--cpus", cmd)
        self.assertIn("0.75", cmd)
        self.assertIn("127.0.0.1:9230:9222", cmd)

    def test_build_local_chromium_command(self):
        cmd = self.orchestrator.build_local_chromium_command(self.profile, cdp_port=9231, url="https://example.com")
        self.assertIn("--remote-debugging-port=9231", cmd)
        self.assertIn("--headless=new", cmd)
        self.assertIn("https://example.com", cmd)

    def test_get_free_port(self):
        port = LinuxContainerOrchestrator.get_free_port(9200)
        self.assertGreaterEqual(port, 9200)

if __name__ == "__main__":
    unittest.main()

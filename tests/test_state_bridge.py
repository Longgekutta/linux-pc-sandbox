from __future__ import annotations
import unittest
import tempfile
import os
import json
from bridge.state_bridge import StateBridge
from bridge.shared_schema import PCBrowserProfile
from core.stealth_profile import LinuxStealthProfileGenerator

class TestLinuxStateBridge(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.bridge = StateBridge(base_profile_dir=self.temp_dir)
        self.profile = LinuxStealthProfileGenerator.create_profile("sync_test_01")

        # Save profile
        p_dir = self.bridge.get_profile_dir(self.profile.profile_id)
        os.makedirs(p_dir, exist_ok=True)
        with open(os.path.join(p_dir, "profile.json"), "w", encoding="utf-8") as f:
            json.dump(self.profile.to_dict(), f, indent=2)

    def tearDown(self):
        try:
            import shutil
            shutil.rmtree(self.temp_dir)
        except Exception:
            pass

    def test_export_and_import_json(self):
        bundle_file = os.path.join(self.temp_dir, "test_bundle.json")
        out_path = self.bridge.export_profile_bundle(self.profile.profile_id, bundle_file)
        self.assertTrue(os.path.isfile(out_path))

        imported = self.bridge.import_profile_bundle(out_path, target_profile_id="restored_worker")
        self.assertEqual(imported.profile_id, "restored_worker")
        self.assertEqual(imported.platform, "linux")
        self.assertEqual(imported.gpu.gl_renderer, self.profile.gpu.gl_renderer)
        self.assertEqual(imported.hardware_concurrency, self.profile.hardware_concurrency)

    def test_export_and_import_zip(self):
        zip_file = os.path.join(self.temp_dir, "test_bundle.zip")
        out_path = self.bridge.export_profile_bundle(self.profile.profile_id, zip_file)
        self.assertTrue(os.path.isfile(out_path))

        imported = self.bridge.import_profile_bundle(out_path, target_profile_id="restored_zip_worker")
        self.assertEqual(imported.profile_id, "restored_zip_worker")
        self.assertEqual(imported.platform, "linux")

if __name__ == "__main__":
    unittest.main()

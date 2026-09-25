from __future__ import annotations
import unittest
from core.stealth_profile import LinuxStealthProfileGenerator
from bridge.shared_schema import PCBrowserProfile

class TestLinuxStealthProfile(unittest.TestCase):

    def test_create_profile(self):
        p = LinuxStealthProfileGenerator.create_profile(
            profile_id="test_worker_01",
            proxy_host="10.0.0.1",
            proxy_port=8080,
            use_proxy=True,
            email="bot@test.com"
        )
        self.assertEqual(p.profile_id, "test_worker_01")
        self.assertEqual(p.platform, "linux")
        self.assertEqual(p.account.email, "bot@test.com")
        self.assertTrue(p.proxy.enabled)
        self.assertEqual(p.proxy.port, 8080)
        self.assertTrue(any(brand in (p.gpu.gl_vendor + p.gpu.gl_renderer) for brand in ["NVIDIA", "Intel", "Google"]))
        self.assertGreaterEqual(p.hardware_concurrency, 8)
        self.assertGreaterEqual(p.device_memory_gb, 16)

    def test_build_stealth_script(self):
        p = LinuxStealthProfileGenerator.create_profile("stealth_test")
        script = LinuxStealthProfileGenerator.build_linux_stealth_script(p)
        self.assertIn("navigator, 'webdriver'", script)
        self.assertIn("Linux x86_64", script)
        self.assertIn(str(p.hardware_concurrency), script)
        self.assertIn(str(p.device_memory_gb), script)
        self.assertIn("UNMASKED_RENDERER_WEBGL", script)
        self.assertIn("window.chrome", script)
        self.assertIn("MAX_TEXTURE_SIZE", script)
        self.assertIn("AudioBuffer.prototype.getChannelData", script)
        self.assertIn("CanvasRenderingContext2D.prototype.getImageData", script)
        self.assertIn("availHeight", script)
        self.assertIn("Notification", script)
        self.assertIn("navigator.getBattery", script)

if __name__ == "__main__":
    unittest.main()

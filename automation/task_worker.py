from __future__ import annotations
"""
Task Worker Module - Linux PC Sandbox
Executes headless maintenance tasks, session warm-ups, fingerprint health checks,
and state sync across distributed cloud Linux nodes.
"""

import time
import random
from typing import Dict, Any, List, Optional
from bridge.shared_schema import PCBrowserProfile
from automation.headless_driver import LinuxHeadlessDriver

class LinuxTaskWorker:
    """
    Automated background worker for Linux PC sandboxes.
    Performs profile warm-ups, browsing simulations, and bot detection checks.
    """

    WARMUP_TARGETS = [
        "https://en.wikipedia.org/wiki/Main_Page",
        "https://news.ycombinator.com/",
        "https://httpbin.org/headers",
        "https://example.com"
    ]

    def __init__(self, driver: LinuxHeadlessDriver):
        self.driver = driver

    def verify_stealth_integrity(self) -> Dict[str, Any]:
        """
        Verify that anti-detect hooks are successfully active in the running Chromium page.
        Audits: webdriver removal, platform, hardware concurrency, and WebGL masking.
        """
        script = """
        (() => {
            let glVendor = 'none';
            let glRenderer = 'none';
            try {
                const canvas = document.createElement('canvas');
                const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                if (gl) {
                    const dbg = gl.getExtension('WEBGL_debug_renderer_info');
                    if (dbg) {
                        glVendor = gl.getParameter(dbg.UNMASKED_VENDOR_WEBGL);
                        glRenderer = gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL);
                    }
                }
            } catch (e) {}

            return {
                webdriver: navigator.webdriver,
                platform: navigator.platform,
                hardwareConcurrency: navigator.hardwareConcurrency,
                deviceMemory: navigator.deviceMemory,
                pluginsLength: navigator.plugins.length,
                glVendor: glVendor,
                glRenderer: glRenderer,
                userAgent: navigator.userAgent
            };
        })()
        """
        res = self.driver.evaluate(script)
        if not isinstance(res, dict):
            return {
                "success": False,
                "error": "Failed to evaluate audit script in browser context"
            }

        # Validate against known leaks
        is_webdriver_hidden = res.get("webdriver") is None
        is_platform_linux = "Linux" in str(res.get("platform", ""))
        is_mesa_hidden = "llvmpipe" not in str(res.get("glRenderer", "")).lower() and "mesa" not in str(res.get("glRenderer", "")).lower()

        return {
            "success": True,
            "profile_id": self.driver.profile.profile_id,
            "webdriver_hidden": is_webdriver_hidden,
            "platform_valid": is_platform_linux,
            "mesa_cloaked": is_mesa_hidden,
            "gl_vendor": res.get("glVendor"),
            "gl_renderer": res.get("glRenderer"),
            "concurrency": res.get("hardwareConcurrency"),
            "plugins_count": res.get("pluginsLength"),
            "raw_audit": res
        }

    def warm_up_session(
        self,
        urls: Optional[List[str]] = None,
        duration_per_url: float = 3.0
    ) -> List[Dict[str, Any]]:
        """
        Visit warm-up targets, scroll pages naturally, and generate organic browsing context.
        """
        targets = urls or self.WARMUP_TARGETS
        results = []

        self.driver.inject_stealth()

        for target in targets:
            start_t = time.time()
            ok = self.driver.navigate(target, wait_seconds=duration_per_url)

            # Simulate natural scroll
            if ok:
                scroll_script = f"window.scrollTo(0, {random.randint(200, 800)});"
                self.driver.evaluate(scroll_script)
                time.sleep(1.0)

            elapsed = round(time.time() - start_t, 2)
            results.append({
                "url": target,
                "success": ok,
                "elapsed_seconds": elapsed
            })

        return results

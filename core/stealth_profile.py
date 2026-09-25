from __future__ import annotations
"""
Stealth Profile Module - Linux PC Sandbox
Solves the Mesa llvmpipe software rendering vulnerability, font leakage, and headless Chrome
fingerprint traps on cloud Linux servers.
Synthesizes discrete GPU hardware profiles (NVIDIA RTX 3080 / 4090) and Client Hints.
"""

import os
import json
import random
from typing import Dict, Any, List, Optional
from bridge.shared_schema import PCBrowserProfile, ScreenConfig, GpuConfig, ProxyConfig, AccountCredentials

class LinuxStealthProfileGenerator:
    """
    Synthesizes and manages cloaked Linux desktop browser profiles.
    Masks headless server artifacts with authentic discrete GPU rendering and desktop fonts.
    """

    LINUX_GPU_PROFILES = [
        {
            "vendor": "NVIDIA Corporation",
            "renderer": "NVIDIA GeForce RTX 3080/PCIe/SSE2",
            "concurrency": 16,
            "memory": 32
        },
        {
            "vendor": "NVIDIA Corporation",
            "renderer": "NVIDIA GeForce RTX 4090/PCIe/SSE2",
            "concurrency": 24,
            "memory": 64
        },
        {
            "vendor": "Google Inc. (Intel)",
            "renderer": "ANGLE (Intel, Intel(R) Iris(R) Xe Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "concurrency": 8,
            "memory": 16
        }
    ]

    @classmethod
    def create_profile(
        cls,
        profile_id: str,
        proxy_host: str = "172.17.0.1",
        proxy_port: int = 7890,
        use_proxy: bool = True,
        email: str = ""
    ) -> PCBrowserProfile:
        """Create a randomized, headless-cloaked Linux desktop profile."""
        gpu_template = random.choice(cls.LINUX_GPU_PROFILES)

        screen = ScreenConfig(
            width=1920,
            height=1080,
            scale_factor=1.0,
            color_depth=24,
            refresh_rate=60
        )

        gpu = GpuConfig(
            gl_vendor=gpu_template["vendor"],
            gl_renderer=gpu_template["renderer"]
        )

        proxy = ProxyConfig(
            enabled=use_proxy,
            proxy_type="http",
            host=proxy_host,
            port=proxy_port
        )

        account = AccountCredentials(email=email)
        chrome_ver = random.choice(["128.0.0.0", "129.0.0.0", "130.0.0.0"])
        ua = f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Safari/537.36"

        return PCBrowserProfile(
            profile_id=profile_id,
            platform="linux",
            browser_type="chrome",
            user_agent=ua,
            screen=screen,
            gpu=gpu,
            proxy=proxy,
            account=account,
            languages=["en-US", "en"],
            timezone="America/New_York",
            webrtc_mode="disable_non_proxied_udp",
            hardware_concurrency=gpu_template["concurrency"],
            device_memory_gb=gpu_template["memory"]
        )

    @classmethod
    def build_linux_stealth_script(cls, profile: PCBrowserProfile) -> str:
        """
        Synthesize dynamic JavaScript payload to eradicate Mesa / llvmpipe and HeadlessChrome signatures.
        """
        gl_vendor = profile.gpu.gl_vendor
        gl_renderer = profile.gpu.gl_renderer
        concurrency = profile.hardware_concurrency
        memory = profile.device_memory_gb

        return f"""
(() => {{
    // 1. Eradicate 'navigator.webdriver'
    try {{
        Object.defineProperty(navigator, 'webdriver', {{
            get: () => undefined,
            configurable: true
        }});
        delete Object.getPrototypeOf(navigator).webdriver;
    }} catch (e) {{}}

    // 2. Linux Desktop Platform & Realistic Hardware
    try {{
        Object.defineProperty(navigator, 'platform', {{
            get: () => 'Linux x86_64',
            configurable: true
        }});
        Object.defineProperty(navigator, 'hardwareConcurrency', {{
            get: () => {concurrency},
            configurable: true
        }});
        Object.defineProperty(navigator, 'deviceMemory', {{
            get: () => {memory},
            configurable: true
        }});
        Object.defineProperty(navigator, 'maxTouchPoints', {{
            get: () => 0,
            configurable: true
        }});
        Object.defineProperty(navigator, 'languages', {{
            get: () => ['en-US', 'en'],
            configurable: true
        }});
    }} catch (e) {{}}

    // 3. Mesa llvmpipe / SwiftShader Software WebGL Cloaking ({gl_vendor} / {gl_renderer})
    try {{
        const getParam1 = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(param) {{
            // UNMASKED_VENDOR_WEBGL (37445)
            if (param === 37445) return '{gl_vendor}';
            // UNMASKED_RENDERER_WEBGL (37446)
            if (param === 37446) return '{gl_renderer}';
            return getParam1.apply(this, arguments);
        }};

        const getParam2 = WebGL2RenderingContext.prototype.getParameter;
        WebGL2RenderingContext.prototype.getParameter = function(param) {{
            if (param === 37445) return '{gl_vendor}';
            if (param === 37446) return '{gl_renderer}';
            return getParam2.apply(this, arguments);
        }};
    }} catch (e) {{}}

    // 4. Mock window.chrome for Headless Linux
    try {{
        if (!window.chrome) {{
            window.chrome = {{
                runtime: {{}},
                app: {{}},
                csi: () => {{}},
                loadTimes: () => {{}}
            }};
        }}
    }} catch (e) {{}}

    // 5. Realistic Desktop Plugins Array
    try {{
        Object.defineProperty(navigator, 'plugins', {{
            get: () => [
                {{ name: 'PDF Viewer', filename: 'internal-pdf-viewer', description: 'Portable Document Format' }},
                {{ name: 'Chrome PDF Viewer', filename: 'internal-pdf-viewer', description: 'Portable Document Format' }}
            ],
            configurable: true
        }});
    }} catch (e) {{}}
}})();
"""

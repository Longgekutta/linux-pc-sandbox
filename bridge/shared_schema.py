from __future__ import annotations
"""
Shared PC Browser Profile Schema - Cross-Platform Data Contract
Defines the unified, platform-neutral browser profile data structures shared between
windows-pc-sandbox and linux-pc-sandbox.
Enables seamless session transfer, cookie/credential portability, and cluster orchestration.
"""

import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict

@dataclass
class ScreenConfig:
    width: int = 1920
    height: int = 1080
    scale_factor: float = 1.0
    color_depth: int = 24
    refresh_rate: int = 60

@dataclass
class GpuConfig:
    gl_vendor: str = "Google Inc. (NVIDIA)"
    gl_renderer: str = "ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0, D3D11)"
    gl_version: str = "WebGL 2.0 (OpenGL ES 3.0 Chromium)"
    shading_language_version: str = "WebGL GLSL ES 3.00 (OpenGL ES GLSL ES 3.0 Chromium)"

@dataclass
class ProxyConfig:
    enabled: bool = False
    proxy_type: str = "http"  # "http", "socks5", "direct"
    host: str = "172.17.0.1"
    port: int = 7890
    username: Optional[str] = None
    password: Optional[str] = None
    bypass_list: Optional[str] = None

    def to_chrome_arg(self) -> str:
        if not self.enabled:
            return ""
        if self.proxy_type == "socks5":
            return f"--proxy-server=socks5://{self.host}:{self.port}"
        return f"--proxy-server=http://{self.host}:{self.port}"

@dataclass
class AccountCredentials:
    email: str = ""
    password: str = ""
    recovery_email: Optional[str] = None
    totp_secret: Optional[str] = None
    notes: Optional[str] = None

@dataclass
class PCBrowserProfile:
    """
    Unified Cross-Platform PC Browser Profile.
    Valid across both Windows PC Sandbox and Linux Cloud Native Sandbox.
    """
    profile_id: str
    platform: str  # "windows" or "linux"
    browser_type: str = "chrome"  # "chrome", "edge", "brave", "firefox"
    user_agent: str = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    screen: ScreenConfig = field(default_factory=ScreenConfig)
    gpu: GpuConfig = field(default_factory=GpuConfig)
    proxy: ProxyConfig = field(default_factory=ProxyConfig)
    account: AccountCredentials = field(default_factory=AccountCredentials)
    languages: List[str] = field(default_factory=lambda: ["en-US", "en"])
    timezone: str = "America/New_York"
    webrtc_mode: str = "disable_non_proxied_udp"
    hardware_concurrency: int = 8
    device_memory_gb: int = 16
    extra_flags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PCBrowserProfile:
        screen_data = data.get("screen", {})
        gpu_data = data.get("gpu", {})
        proxy_data = data.get("proxy", {})
        account_data = data.get("account", {})

        return cls(
            profile_id=data["profile_id"],
            platform=data.get("platform", "linux"),
            browser_type=data.get("browser_type", "chrome"),
            user_agent=data.get("user_agent", cls.__dataclass_fields__["user_agent"].default),
            screen=ScreenConfig(**screen_data) if isinstance(screen_data, dict) else ScreenConfig(),
            gpu=GpuConfig(**gpu_data) if isinstance(gpu_data, dict) else GpuConfig(),
            proxy=ProxyConfig(**proxy_data) if isinstance(proxy_data, dict) else ProxyConfig(),
            account=AccountCredentials(**account_data) if isinstance(account_data, dict) else AccountCredentials(),
            languages=data.get("languages", ["en-US", "en"]),
            timezone=data.get("timezone", "America/New_York"),
            webrtc_mode=data.get("webrtc_mode", "disable_non_proxied_udp"),
            hardware_concurrency=data.get("hardware_concurrency", 8),
            device_memory_gb=data.get("device_memory_gb", 16),
            extra_flags=data.get("extra_flags", [])
        )

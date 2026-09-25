from __future__ import annotations
import unittest
from core.cloud_network_router import LinuxCloudNetworkRouter
from bridge.shared_schema import ProxyConfig

class TestLinuxCloudNetworkRouter(unittest.TestCase):

    def test_chrome_network_args(self):
        proxy = ProxyConfig(
            enabled=True,
            proxy_type="socks5",
            host="127.0.0.1",
            port=10808,
            bypass_list="<-loopback>"
        )
        args = LinuxCloudNetworkRouter.get_chrome_network_args(proxy)
        self.assertIn("--proxy-server=socks5://127.0.0.1:10808", args)
        self.assertIn("--proxy-bypass-list=<-loopback>", args)
        self.assertIn("--enforce-webrtc-ip-permission-check", args)
        self.assertIn("--dns-over-https-mode=secure", args)

    def test_chrome_network_args_direct(self):
        proxy = ProxyConfig(enabled=False)
        args = LinuxCloudNetworkRouter.get_chrome_network_args(proxy)
        for arg in args:
            self.assertFalse(arg.startswith("--proxy-server="))

    def test_proxy_opener(self):
        proxy = ProxyConfig(
            enabled=True,
            proxy_type="http",
            host="127.0.0.1",
            port=7890
        )
        opener = LinuxCloudNetworkRouter.get_proxy_opener(proxy)
        self.assertIsNotNone(opener)

if __name__ == "__main__":
    unittest.main()

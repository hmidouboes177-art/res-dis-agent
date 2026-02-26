"""浏览器配置项，供多个脚本复用。"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

CFG_FILE = Path(__file__).resolve().parent / "cfg.env"


def _read_cfg_file(path: Path) -> Dict[str, str]:
    """读取简单的 KEY=VALUE 配置文件。"""
    config: Dict[str, str] = {}
    if not path.exists():
        return config

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]

        config[key] = value

    return config


_CONFIG = _read_cfg_file(CFG_FILE)

# 用户指纹（Chrome 持久化数据目录）
USER_DATA_DIR = _CONFIG.get("USER_DATA_DIR", "/root/reddit-new/chrome_data")


def get_proxy_config() -> Optional[Dict[str, str]]:
    """按配置文件生成 Playwright 代理配置。"""
    server = _CONFIG.get("PROXY_SERVER", "")
    if not server:
        return None

    proxy: Dict[str, str] = {"server": server}

    username = _CONFIG.get("PROXY_USERNAME", "")
    password = _CONFIG.get("PROXY_PASSWORD", "")
    if username:
        proxy["username"] = username
    if password:
        proxy["password"] = password

    return proxy

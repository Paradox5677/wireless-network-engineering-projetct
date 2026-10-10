"""配置加载（已给，直接使用）。"""
import json
from pathlib import Path
from typing import Any

# 仓库根目录下的默认配置
_REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = _REPO_ROOT / "config" / "default.json"


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    """加载实验配置。

    Args:
        path: JSON 配置文件路径。为 None 时使用 config/default.json。

    Returns:
        配置字典，键包括 duration_slots, slot_ms, num_users, packet_size_bits,
        arrival_rate_pps, channel{base_rate_bps, std_db}, queue_max_size, seeds。
    """
    cfg_path = Path(path) if path is not None else DEFAULT_CONFIG_PATH
    with open(cfg_path, "r", encoding="utf-8") as f:
        config: dict[str, Any] = json.load(f)
    return config

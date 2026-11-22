"""第 2 周任务：性能指标（Jain 公平性指数）。"""
from __future__ import annotations

from typing import Sequence


def jain_fairness(values: Sequence[float]) -> float:
    """计算 Jain 公平性指数。

    公式：J = (sum x_i)^2 / (n * sum x_i^2)，取值范围 (0, 1]，越接近 1 越公平。

    规格：
    - values 为空时返回 1.0。
    - 所有值均为 0 时返回 1.0（无流量视为公平）。
    - 输入可包含 0，但不应包含负数；出现负数抛出 ValueError。

    Args:
        values: 各用户的吞吐量或其他非负指标。

    Returns:
        Jain 公平性指数，范围 (0, 1]。
    """
    if not values:
        return 1.0
    if any(v < 0 for v in values):
        raise ValueError("输入值不能为负数")
    elif all(v == 0 for v in values):
        return 1.0
    # 计算 Jain 公平性指数
    n = len(values)
    sum_values = sum(values)
    sum_squares = sum(v ** 2 for v in values)
    jain_index = (sum_values ** 2) / (n * sum_squares)
    return jain_index
    # raise NotImplementedError("第 2 周任务：实现 Jain 公平性指数")

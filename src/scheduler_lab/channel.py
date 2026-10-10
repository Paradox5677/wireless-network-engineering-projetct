"""第 3 周任务：时变信道（每时隙每用户独立的慢衰落速率）。"""
from __future__ import annotations

import numpy as np


class TimeVaryingChannel:
    """时变信道速率模型。

    规格：
    - 对每个 (slot, user_id)，速率 rate = base_rate_bps * 10 ** (z / 10)，
      其中 z ~ N(0, std_db ** 2)，不同 (slot, user) 之间独立同分布。
    - rate() 必须是纯函数：同一实例、相同 (slot, user_id) 参数始终返回相同值
      （提示：可在 __init__ 中用 rng 预先生成 shape 为
      (duration_slots, num_users) 的速率表）。
    - rate 恒为正数。
    - slot 超出 [0, duration_slots) 或 user_id 超出 [0, num_users) 时抛出
      IndexError。

    Args:
        num_users: 用户数。
        duration_slots: 仿真总时隙数。
        rng: 随机数生成器（由 Simulator 用 seed 创建，保证可复现）。
        base_rate_bps: 平均参考速率（比特/秒）。
        std_db: 对数正态衰落的标准差（dB）。
    """

    def __init__(
        self,
        *,
        num_users: int,
        duration_slots: int,
        rng: np.random.Generator,
        base_rate_bps: float,
        std_db: float,
    ) -> None:
        # 已给：保存构造参数。速率表的生成在你实现 rate() 时自行完成。
        self._num_users = num_users
        self._duration_slots = duration_slots
        self._rng = rng
        self._base_rate_bps = base_rate_bps
        self._std_db = std_db

    def rate(self, slot: int, user_id: int) -> float:
        """返回指定时隙、指定用户的瞬时可用速率（比特/秒）。"""
        raise NotImplementedError("第 3 周任务：实现时变信道速率")

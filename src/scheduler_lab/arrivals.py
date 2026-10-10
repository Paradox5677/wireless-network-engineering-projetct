"""第 2 周任务：泊松流量到达过程。"""
from __future__ import annotations

from typing import Sequence

import numpy as np

from scheduler_lab.packet import Packet


def generate_poisson_traffic(
    rng: np.random.Generator,
    *,
    num_users: int,
    duration_slots: int,
    slot_s: float,
    rate_pps: float | Sequence[float],
    packet_size_bits: float,
) -> list[Packet]:
    """生成多用户独立泊松到达的数据包序列。

    规格：
    - 用户 u 的到达总数 n_u ~ Poisson(rate_pps[u] * duration_slots * slot_s)。
    - 每个包的 arrival_slot 在 [0, duration_slots) 内均匀随机取整数。
    - 所有包的 size_bits 等于 packet_size_bits。
    - 返回列表按 arrival_slot 升序排列，同 slot 内按 user_id 升序。
    - rate_pps 可以是标量（所有用户相同）或长度为 num_users 的序列。
    - 到达总数为 0 时返回空列表。

    Args:
        rng: 随机数生成器（由 Simulator 用 seed 创建，保证可复现）。
        num_users: 用户数。
        duration_slots: 仿真总时隙数。
        slot_s: 单个时隙的时长（秒）。
        rate_pps: 每用户每秒到达包数。
        packet_size_bits: 固定包长（比特）。

    Returns:
        按 (arrival_slot, user_id) 排序的 Packet 列表。
    """
    raise NotImplementedError("第 2 周任务：实现泊松到达过程")

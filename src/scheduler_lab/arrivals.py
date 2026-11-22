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
    """生成多用户独立泊松到达的数据包序列。简化模型，一次性生成所有到达包。

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
    packets: list[Packet] = []
    # 将标量和序列区分开
    if isinstance(rate_pps, (int, float, np.integer, np.floating)):
        rates = [float(rate_pps)] * num_users
    else:
        if len(rate_pps) != num_users:
            raise ValueError("rate_pps 的长度必须等于 num_users")
        rates = [float(rate) for rate in rate_pps]

    for u in range(num_users):
        # 为每个用户生成泊松到达的包
        rate = rates[u]
        n_u = rng.poisson(rate * duration_slots * slot_s)  # 该用户的到达总数
        for _ in range(n_u):
            # 生成一个包
            arrival_slot = rng.integers(0, duration_slots)  # 均匀随机选择到达时隙
            packet = Packet(
                user_id=u,
                arrival_slot=arrival_slot,
                size_bits=packet_size_bits,
            )
            packets.append(packet)
    packets.sort(key=lambda p: (p.arrival_slot, p.user_id))  # 按到达时隙和用户 ID 排序
    return packets
    # raise NotImplementedError("第 2 周任务：实现泊松到达过程")
    """
    按照时隙动态生成到达包的方式可以使用以下方法，需要每个时隙进行一次包生成：
    1. 对于当前时隙 t，从泊松分布中采样得到每个用户在该时隙的到达包数 n_u_t。
    2. 对于每个用户 u，生成 n_u_t 个包，设置 arrival_slot = t，user_id = u，size_bits = packet_size_bits。
    3. 将所有生成的包按 (arrival_slot, user_id) 排序。
    这种方法可以在仿真过程中动态生成包，而不是一次性生成所有包。
    """
    """
    def generate_poisson_traffic_dynamic(
        rng: np.random.Generator,
        *,
        num_users: int,
        current_slot: int,
        slot_s: float,
        rate_pps: float | Sequence[float],
        packet_size_bits: float,
    ) -> list[Packet]:
        packets: list[Packet] = []
        # 把标量和序列区分开
        if isinstance(rate_pps, (int, float)):
            rate = float(rate_pps)
        else:
            rate = [float(r) for r in rate_pps]
        for u in range(num_users):
            # 为每个用户在当前时隙生成泊松到达的包
            n_u_t = rng.poisson(rate * slot_s)  # 该用户在当前时隙的到达包数
            for _ in range(n_u_t):
                # 生成一个包
                packet = Packet(
                    user_id=u,
                    arrival_slot=current_slot,
                    size_bits=packet_size_bits,
                )
                packets.append(packet)
        packets.sort(key=lambda p: (p.arrival_slot, p.user_id))  # 按到达时隙和用户 ID 排序
        return packets
    """
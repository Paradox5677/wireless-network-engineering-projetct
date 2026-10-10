"""数据包定义（已给，直接使用）。"""
from dataclasses import dataclass


@dataclass
class Packet:
    """一个数据包。

    Attributes:
        user_id: 所属用户编号，范围 [0, num_users)。
        arrival_slot: 到达的时隙编号，范围 [0, duration_slots)。
        size_bits: 包长（比特）。当前仿真中包长固定，但字段保持可变以便扩展。
    """

    user_id: int
    arrival_slot: int
    size_bits: float

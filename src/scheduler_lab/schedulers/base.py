"""调度器接口与调度器可见的用户状态（已给，直接使用）。"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class UserState:
    """调度器在每个时隙可见的用户状态。

    Attributes:
        user_id: 用户编号。
        rate_bps: 该用户本时隙的瞬时可用速率（比特/秒）。
        queue_bits: 该用户队列中当前待发送的总比特数（0 表示队空）。
        hol_delay_slots: 队头包的 HOL 时延（当前时隙 - 队头包到达时隙），
            队空时为 0。
        avg_throughput_bps: 该用户到目前为止的平均吞吐量（比特/秒）。
    """

    user_id: int
    rate_bps: float
    queue_bits: float
    hol_delay_slots: int
    avg_throughput_bps: float


class Scheduler(ABC):
    """调度器抽象基类。

    约定：
    - ``name`` 为调度器名称字符串（用于实验结果标注）。
    - ``select_user`` 每时隙被调用一次，输入为包含所有用户的 UserState 列表。
    - 只能从 queue_bits > 0 的用户中选择；若所有用户队列为空，返回 None。
    - 平局（如速率相同）时选择 user_id 较小的用户，保证结果可复现。
    - ``reset`` 在每次实验（每个 seed）开始前调用，用于清空内部状态
      （例如 RR 的轮转指针）。
    """

    name: str

    @abstractmethod
    def reset(self) -> None:
        """清空调度器内部状态，使每次实验从相同初始状态开始。"""

    @abstractmethod
    def select_user(self, users: list[UserState]) -> int | None:
        """从队列非空的用户中选择一个服务对象。

        Returns:
            被选中的 user_id；所有用户队列为空时返回 None。
        """

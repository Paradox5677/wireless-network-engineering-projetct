"""第 3 周任务：Max-Rate（最大瞬时速率）调度器。"""
from __future__ import annotations

from scheduler_lab.schedulers.base import Scheduler, UserState


class MaxRateScheduler(Scheduler):
    """最大瞬时速率调度器（Max-Rate / Max-C/I）。

    规格：
    - name = "max-rate"。
    - 从 queue_bits > 0 的用户中选择 rate_bps 最大者。
    - 速率相同时选择 user_id 较小者（保证结果确定可复现）。
    - 所有用户队列为空时返回 None。
    - 无内部状态，reset() 为空操作。
    """

    name = "max-rate"

    def reset(self) -> None:
        raise NotImplementedError("第 3 周任务：实现 reset（可为空操作）")

    def select_user(self, users: list[UserState]) -> int | None:
        raise NotImplementedError("第 3 周任务：实现 Max-Rate 选择")

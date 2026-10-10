"""第 2 周任务：Round Robin 调度器。"""
from __future__ import annotations

from scheduler_lab.schedulers.base import Scheduler, UserState


class RoundRobinScheduler(Scheduler):
    """轮询调度器。

    规格：
    - name = "round-robin"。
    - 内部维护指针 next_index，指向下一个候选用户（初始为 0）。
    - select_user 从 next_index 开始循环扫描（回到末尾后折返到 0），
      选出第一个 queue_bits > 0 的用户；选中后将 next_index 设为
      (选中 user_id + 1) % num_users。
    - 若所有用户队列为空，返回 None，且不修改 next_index。
    - reset() 将 next_index 归零。
    """

    name = "round-robin"

    def __init__(self) -> None:
        self._next_index = 0

    def reset(self) -> None:
        raise NotImplementedError("第 2 周任务：实现 reset")

    def select_user(self, users: list[UserState]) -> int | None:
        raise NotImplementedError("第 2 周任务：实现 RR 轮询选择")

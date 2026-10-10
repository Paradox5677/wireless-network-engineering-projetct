"""第 1 周任务：FIFO 数据包队列。

先读懂下面的接口规格，再独立实现，最后用 `pytest -m week1` 验收。
实现前所有方法都会抛出 NotImplementedError。
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scheduler_lab.packet import Packet


class QueueEmptyError(Exception):
    """对空队列执行 pop / peek 时抛出。"""


class PacketQueue:
    """先进先出（FIFO）数据包队列。

    规格：
    - 队列内部按到达顺序保存 Packet，push 追加到队尾，pop 从队头移除并返回。
    - ``max_size`` 为 None 表示无界；为正整数表示容量上限，队满时 push 返回
      False 且不修改队列（不覆盖、不丢弃已有包）。
    - ``bits`` 返回队列中所有包 size_bits 之和。
    - 空队列执行 pop / peek 抛出 QueueEmptyError。
    """

    def __init__(self, max_size: int | None = None) -> None:
        if max_size is not None and max_size <= 0:
            raise ValueError("max_size 必须为正整数或 None")
        self._max_size = max_size
        self._items: list[Packet] = []
        # TODO(第1周): 按需补充你自己的状态字段

    def push(self, packet: "Packet") -> bool:
        """将包追加到队尾。队满时返回 False，成功返回 True。"""
        raise NotImplementedError("第 1 周任务：实现 push")

    def pop(self) -> "Packet":
        """移除并返回队头包。空队列抛出 QueueEmptyError。"""
        raise NotImplementedError("第 1 周任务：实现 pop")

    def peek(self) -> "Packet":
        """返回队头包但不移除。空队列抛出 QueueEmptyError。"""
        raise NotImplementedError("第 1 周任务：实现 peek")

    def is_empty(self) -> bool:
        """队列为空返回 True。"""
        raise NotImplementedError("第 1 周任务：实现 is_empty")

    def __len__(self) -> int:
        """返回队列中包的数量。"""
        raise NotImplementedError("第 1 周任务：实现 __len__")

    @property
    def bits(self) -> float:
        """队列中所有包 size_bits 之和，空队列为 0。"""
        raise NotImplementedError("第 1 周任务：实现 bits")

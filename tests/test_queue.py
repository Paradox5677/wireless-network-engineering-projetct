"""第 1 周验收：FIFO 队列。

运行: pytest -m week1
"""
import pytest

from scheduler_lab.packet import Packet
from scheduler_lab.queue import PacketQueue, QueueEmptyError


def make_packet(user_id: int = 0, slot: int = 0, size_bits: float = 1000.0) -> Packet:
    return Packet(user_id=user_id, arrival_slot=slot, size_bits=size_bits)


@pytest.mark.week1
def test_new_queue_is_empty():
    q = PacketQueue()
    assert q.is_empty()
    assert len(q) == 0
    assert q.bits == 0


@pytest.mark.week1
def test_fifo_order():
    q = PacketQueue()
    p1 = make_packet(slot=1)
    p2 = make_packet(slot=2)
    p3 = make_packet(slot=3)

    assert q.push(p1) is True
    assert q.push(p2) is True
    assert q.push(p3) is True

    assert len(q) == 3
    assert q.peek() is p1          # peek 不移除
    assert len(q) == 3
    assert q.pop() is p1           # 先进先出
    assert q.pop() is p2
    assert q.pop() is p3
    assert q.is_empty()


@pytest.mark.week1
def test_bits_accumulates_packet_sizes():
    q = PacketQueue()
    q.push(make_packet(size_bits=1000))
    q.push(make_packet(size_bits=2500))
    assert q.bits == 3500
    q.pop()
    assert q.bits == 2500
    q.pop()
    assert q.bits == 0


@pytest.mark.week1
def test_empty_pop_raises():
    q = PacketQueue()
    with pytest.raises(QueueEmptyError):
        q.pop()
    with pytest.raises(QueueEmptyError):
        q.peek()


@pytest.mark.week1
def test_bounded_queue_rejects_when_full():
    q = PacketQueue(max_size=2)
    p1, p2, p3 = make_packet(slot=1), make_packet(slot=2), make_packet(slot=3)
    assert q.push(p1) is True
    assert q.push(p2) is True
    assert q.push(p3) is False      # 队满：拒绝且不覆盖
    assert len(q) == 2
    assert q.pop() is p1            # 原有顺序未被破坏
    assert q.push(p3) is True       # 腾出空间后可再入队
    assert q.pop() is p2
    assert q.pop() is p3


@pytest.mark.week1
def test_invalid_max_size():
    with pytest.raises(ValueError):
        PacketQueue(max_size=0)

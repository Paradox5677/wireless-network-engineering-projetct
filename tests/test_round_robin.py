"""第 2 周验收：Round Robin 调度器。

运行: pytest -m week2
"""
import pytest

from scheduler_lab.schedulers.base import UserState
from scheduler_lab.schedulers.round_robin import RoundRobinScheduler


def state(user_id: int, rate: float = 1e6, queue_bits: float = 1000.0) -> UserState:
    return UserState(
        user_id=user_id,
        rate_bps=rate,
        queue_bits=queue_bits,
        hol_delay_slots=0,
        avg_throughput_bps=0.0,
    )


@pytest.mark.week2
def test_rr_cycles_over_users_with_traffic():
    rr = RoundRobinScheduler()
    rr.reset()
    # 用户 1 队列为空，应被跳过
    users = [state(0), state(1, queue_bits=0.0), state(2)]
    assert rr.select_user(users) == 0
    assert rr.select_user(users) == 2   # 跳过空队列的用户 1
    assert rr.select_user(users) == 0   # 循环回用户 0
    assert rr.select_user(users) == 2


@pytest.mark.week2
def test_rr_returns_none_when_all_empty():
    rr = RoundRobinScheduler()
    rr.reset()
    users = [state(0, queue_bits=0.0), state(1, queue_bits=0.0)]
    assert rr.select_user(users) is None
    assert rr.select_user(users) is None  # 连续空队列不破坏状态


@pytest.mark.week2
def test_rr_resumes_cycle_after_idle_period():
    rr = RoundRobinScheduler()
    rr.reset()
    users = [state(0), state(1), state(2)]
    assert rr.select_user(users) == 0
    # 一段时间全空（队列排空），期间指针不应被重置或跳变
    empty = [state(0, queue_bits=0.0), state(1, queue_bits=0.0), state(2, queue_bits=0.0)]
    assert rr.select_user(empty) is None
    # 恢复有流量后，应从用户 1 继续轮转
    assert rr.select_user(users) == 1


@pytest.mark.week2
def test_rr_reset_restores_initial_pointer():
    rr = RoundRobinScheduler()
    rr.reset()
    users = [state(0), state(1), state(2)]
    rr.select_user(users)
    rr.select_user(users)
    rr.reset()
    assert rr.select_user(users) == 0

"""第 3 周验收：时变信道、Max-Rate 调度器。

运行: pytest -m week3
"""
import numpy as np
import pytest

from scheduler_lab.channel import TimeVaryingChannel
from scheduler_lab.schedulers.base import UserState
from scheduler_lab.schedulers.max_rate import MaxRateScheduler


def make_channel(seed: int = 0, **overrides) -> TimeVaryingChannel:
    params = dict(
        num_users=4,
        duration_slots=500,
        rng=np.random.default_rng(seed),
        base_rate_bps=2e6,
        std_db=3.0,
    )
    params.update(overrides)
    return TimeVaryingChannel(**params)


@pytest.mark.week3
def test_rate_is_pure_function():
    ch = make_channel()
    first = ch.rate(slot=10, user_id=2)
    assert ch.rate(slot=10, user_id=2) == first   # 同参数必须同返回值
    # 打乱查询顺序后仍然一致
    ch.rate(slot=0, user_id=0)
    ch.rate(slot=499, user_id=3)
    assert ch.rate(slot=10, user_id=2) == first


@pytest.mark.week3
def test_rate_positive_and_sane_magnitude():
    ch = make_channel()
    samples = [ch.rate(s, u) for s in range(0, 500, 10) for u in range(4)]
    assert all(r > 0 for r in samples)
    mean = float(np.mean(samples))
    # 对数正态衰落下均值应在 base_rate_bps 的合理邻域内
    assert 0.6 * 2e6 < mean < 1.6 * 2e6


@pytest.mark.week3
def test_rate_reproducible_with_same_seed():
    a = make_channel(seed=7).rate(slot=99, user_id=1)
    b = make_channel(seed=7).rate(slot=99, user_id=1)
    assert a == b


@pytest.mark.week3
def test_rate_out_of_range_raises():
    ch = make_channel()
    with pytest.raises(IndexError):
        ch.rate(slot=500, user_id=0)
    with pytest.raises(IndexError):
        ch.rate(slot=0, user_id=4)


def state(user_id: int, rate: float, queue_bits: float = 1000.0) -> UserState:
    return UserState(
        user_id=user_id,
        rate_bps=rate,
        queue_bits=queue_bits,
        hol_delay_slots=0,
        avg_throughput_bps=0.0,
    )


@pytest.mark.week3
def test_max_rate_selects_highest_rate_among_backlogged():
    mr = MaxRateScheduler()
    mr.reset()
    users = [
        state(0, rate=1.0e6),
        state(1, rate=5.0e6, queue_bits=0.0),  # 队列为空，必须被跳过
        state(2, rate=3.0e6),
        state(3, rate=2.0e6, queue_bits=0.0),  # 队列为空
    ]
    # 最高速率的用户 1 队列为空 -> 应选次高的用户 2
    assert mr.select_user(users) == 2
    # 用户 1 开始有流量 -> 应选用户 1
    users[1] = state(1, rate=5.0e6)
    assert mr.select_user(users) == 1


@pytest.mark.week3
def test_max_rate_tie_breaks_to_smaller_user_id():
    mr = MaxRateScheduler()
    mr.reset()
    users = [state(0, rate=2.0e6), state(1, rate=2.0e6), state(2, rate=2.0e6)]
    assert mr.select_user(users) == 0


@pytest.mark.week3
def test_max_rate_none_when_all_empty():
    mr = MaxRateScheduler()
    mr.reset()
    users = [state(0, rate=1.0e6, queue_bits=0.0)]
    assert mr.select_user(users) is None

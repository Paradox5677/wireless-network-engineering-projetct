"""第 2 周验收：泊松到达过程与 Jain 公平性。

运行: pytest -m week2
"""
import numpy as np
import pytest

from scheduler_lab.arrivals import generate_poisson_traffic
from scheduler_lab.metrics import jain_fairness


@pytest.mark.week2
def test_traffic_count_within_reasonable_range():
    rng = np.random.default_rng(0)
    packets = generate_poisson_traffic(
        rng,
        num_users=5,
        duration_slots=1000,
        slot_s=0.001,
        rate_pps=100.0,
        packet_size_bits=1000,
    )
    # 期望总数 = 100 pps * 1 s * 5 用户 = 500，泊松标准差约 22，留宽裕余量
    assert 350 <= len(packets) <= 650


@pytest.mark.week2
def test_traffic_fields_and_ordering():
    rng = np.random.default_rng(1)
    packets = generate_poisson_traffic(
        rng,
        num_users=3,
        duration_slots=500,
        slot_s=0.001,
        rate_pps=[50.0, 100.0, 150.0],
        packet_size_bits=1200,
    )
    assert packets, "到达列表不应为空"
    for p in packets:
        assert 0 <= p.user_id < 3
        assert 0 <= p.arrival_slot < 500
        assert p.size_bits == 1200
    # 按 (arrival_slot, user_id) 排序
    keys = [(p.arrival_slot, p.user_id) for p in packets]
    assert keys == sorted(keys)


@pytest.mark.week2
def test_traffic_reproducible_with_same_seed():
    kwargs = dict(
        num_users=4,
        duration_slots=800,
        slot_s=0.001,
        rate_pps=80.0,
        packet_size_bits=1000,
    )
    a = generate_poisson_traffic(np.random.default_rng(42), **kwargs)
    b = generate_poisson_traffic(np.random.default_rng(42), **kwargs)
    assert a == b


@pytest.mark.week2
def test_zero_rate_returns_empty():
    rng = np.random.default_rng(0)
    packets = generate_poisson_traffic(
        rng,
        num_users=2,
        duration_slots=100,
        slot_s=0.001,
        rate_pps=0.0,
        packet_size_bits=1000,
    )
    assert packets == []


@pytest.mark.week2
def test_jain_fairness_equal_values():
    assert jain_fairness([100.0, 100.0, 100.0]) == pytest.approx(1.0)
    assert jain_fairness([2.5, 2.5]) == pytest.approx(1.0)


@pytest.mark.week2
def test_jain_fairness_single_winner():
    assert jain_fairness([1.0, 0.0, 0.0]) == pytest.approx(1.0 / 3.0)


@pytest.mark.week2
def test_jain_fairness_known_value():
    # (1+2)^2 / (3*(1+4)) = 9/15 = 0.6
    assert jain_fairness([1.0, 2.0, 0.0]) == pytest.approx(0.6)


@pytest.mark.week2
def test_jain_fairness_edge_cases():
    assert jain_fairness([]) == 1.0
    assert jain_fairness([0.0, 0.0, 0.0]) == 1.0
    with pytest.raises(ValueError):
        jain_fairness([-1.0, 2.0])

"""第 4 周验收：仿真器冒烟测试与对比实验脚本。

运行: pytest -m week4
"""
import pytest

from scheduler_lab.schedulers.max_rate import MaxRateScheduler
from scheduler_lab.schedulers.round_robin import RoundRobinScheduler
from scheduler_lab.simulator import Simulator


def small_config(**overrides) -> dict:
    config = {
        "duration_slots": 200,
        "slot_ms": 1.0,
        "num_users": 4,
        "packet_size_bits": 1000,
        "arrival_rate_pps": [80, 80, 40, 40],
        "channel": {"base_rate_bps": 2000000, "std_db": 1.0},
        "queue_max_size": 50,
        "seeds": [0, 1],
    }
    config.update(overrides)
    return config


@pytest.mark.week4
def test_simulator_runs_and_returns_valid_result():
    sim = Simulator(small_config(), RoundRobinScheduler(), seed=0)
    res = sim.run()

    assert res.scheduler_name == "round-robin"
    assert res.seed == 0
    assert res.slots == 200
    assert len(res.per_user_throughput_bps) == 4
    assert res.total_throughput_bps >= 0
    assert 0.0 < res.jain_fairness <= 1.0
    assert res.mean_hol_delay_slots >= 0.0
    assert res.decision_time_s >= 0.0
    # 总吞吐量应等于各用户吞吐量之和
    assert res.total_throughput_bps == pytest.approx(
        sum(res.per_user_throughput_bps), rel=1e-9
    )
    # 负载下 RR 应有实际吞吐量（否则说明服务逻辑有问题）
    assert res.total_throughput_bps > 0


@pytest.mark.week4
def test_simulator_reproducible_with_same_seed():
    cfg = small_config()
    a = Simulator(cfg, RoundRobinScheduler(), seed=1).run()
    b = Simulator(cfg, RoundRobinScheduler(), seed=1).run()
    assert a.per_user_throughput_bps == pytest.approx(b.per_user_throughput_bps)
    assert a.mean_hol_delay_slots == pytest.approx(b.mean_hol_delay_slots)


@pytest.mark.week4
def test_simulator_no_traffic_means_zero_throughput():
    cfg = small_config(arrival_rate_pps=[0, 0, 0, 0])
    res = Simulator(cfg, MaxRateScheduler(), seed=0).run()
    assert res.total_throughput_bps == 0.0
    assert res.jain_fairness == pytest.approx(1.0)
    assert res.mean_hol_delay_slots == 0.0


@pytest.mark.week4
def test_simulator_max_rate_at_least_rr_throughput():
    """相同种子下 Max-Rate 的吞吐量不应低于 RR（两者信道一致）。"""
    cfg = small_config(duration_slots=500)
    rr = Simulator(cfg, RoundRobinScheduler(), seed=0).run()
    mr = Simulator(cfg, MaxRateScheduler(), seed=0).run()
    # 同 seed 应生成相同的流量与信道轨迹
    assert mr.total_throughput_bps >= rr.total_throughput_bps * 0.99

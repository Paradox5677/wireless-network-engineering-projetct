"""第 2-3 周任务：离散时间调度仿真器主循环。

接口（ExperimentResult 与 Simulator.__init__）已给，run() 由你实现。
实现顺序建议：先在纸上按下面的伪代码写出每步用到的模块，再逐段编码。
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from scheduler_lab.schedulers.base import Scheduler


@dataclass
class ExperimentResult:
    """一次仿真实验的汇总结果（已给）。"""

    scheduler_name: str
    seed: int
    slots: int
    per_user_throughput_bps: list[float] = field(default_factory=list)
    total_throughput_bps: float = 0.0
    mean_hol_delay_slots: float = 0.0
    jain_fairness: float = 1.0
    decision_time_s: float = 0.0


class Simulator:
    """单调度器、单随机种子的时隙级仿真。

    仿真规格（run() 必须遵循）：
    - 时隙内事件顺序：包到达入队 → 采样信道 → 构造 UserState → 调度决策 → 服务。
      即同一时隙到达的包可以被同一时隙服务。
    - 服务模型：每时隙最多服务被选中用户的 1 个包；仅当
      rate_bps * slot_s >= 队头包 size_bits 时发送成功（pop 并计入已送达
      比特），否则本时隙不传输（信道容量不足，队头 HOL 继续累积）。
    - HOL 时延：hol = 当前时隙 - 队头包的 arrival_slot，队空记 0；
      mean_hol_delay_slots 为所有时隙、所有用户 HOL 的平均值。
    - avg_throughput_bps（写入 UserState）= 该用户已送达比特 / (已仿真时长秒)，
      已仿真时长为 0 时记 0。
    - 各用户吞吐量 = 已送达比特 / (duration_slots * slot_s)。
    - decision_time_s 为 scheduler.select_user 调用的累计耗时（perf_counter）。
    - jain_fairness 由各用户吞吐量调用 metrics.jain_fairness 计算。
    - 每次 run() 开始时用 seed 创建 np.random.default_rng，
      并调用 scheduler.reset()，保证结果可复现、与调用顺序无关。
    - 队列满时新到达的包被丢弃（push 返回 False 即可，无需额外处理）。

    伪代码::

        rng = np.random.default_rng(seed)
        scheduler.reset()
        traffic = generate_poisson_traffic(rng, ...)      # arrivals.py
        channel = TimeVaryingChannel(rng=rng, ...)        # channel.py
        queues = [PacketQueue(queue_max_size) for _ in range(num_users)]
        delivered = [0.0] * num_users
        hol_sum = 0.0
        decision_time = 0.0
        arrival_ptr = 0   # traffic 已按 arrival_slot 排序，用指针扫描

        for slot in range(duration_slots):
            1. 将 arrival_slot == slot 的包 push 进对应用户队列（arrival_ptr 后移）
            2. rates[u] = channel.rate(slot, u)  for all u
            3. 构造 UserState（rate_bps / queue_bits / hol / avg_throughput）
            4. t0 = perf_counter(); uid = scheduler.select_user(states)
               decision_time += perf_counter() - t0
            5. 若 uid 不为 None 且 rates[uid] * slot_s >= 队头包 size：
               pop，delivered[uid] += size_bits
            6. 累加本时隙所有用户的 HOL 到 hol_sum

        汇总并返回 ExperimentResult
    """

    def __init__(self, config: dict[str, Any], scheduler: Scheduler, seed: int) -> None:
        self.config = config
        self.scheduler = scheduler
        self.seed = seed

    def run(self) -> ExperimentResult:
        """执行一次完整仿真并返回汇总结果。"""
        raise NotImplementedError("第 3 周任务：按伪代码实现仿真主循环")

    # ------------------------------------------------------------------
    # 提示：可以自行添加私有辅助方法，例如 _build_user_states()、
    # _service_slot() 等，把主循环拆短，便于调试。
    #
    # 需要的模块：
    #   from scheduler_lab.arrivals import generate_poisson_traffic
    #   from scheduler_lab.channel import TimeVaryingChannel
    #   from scheduler_lab.metrics import jain_fairness
    #   from scheduler_lab.packet import Packet
    #   from scheduler_lab.queue import PacketQueue
    #   from scheduler_lab.schedulers.base import UserState
    # ------------------------------------------------------------------

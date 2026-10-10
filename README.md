# 无线资源调度练习项目（第一个月）

面向"华为无线通信算法研究岗"学习路线的第一个月实践项目。
目标：脱离 AI 独立实现一个含队列、到达过程、时变信道和调度策略的离散时间调度仿真器。

## 项目结构

```
engineering/
├── README.md                  # 本文件：任务清单与验收标准
├── pytest.ini                 # pytest 配置（按周分组的 marker）
├── requirements.txt
├── conftest.py                # 将 src/ 加入 sys.path
├── config/
│   └── default.json           # 默认实验配置（用户数、到达率、信道参数、随机种子）
├── src/scheduler_lab/
│   ├── packet.py              # [已给] 数据包定义
│   ├── config.py              # [已给] 配置加载
│   ├── queue.py               # [第1周] FIFO 队列          → 实现
│   ├── arrivals.py            # [第2周] 泊松到达过程        → 实现
│   ├── channel.py             # [第3周] 时变信道            → 实现
│   ├── metrics.py             # [第2周] Jain 公平性         → 实现
│   ├── simulator.py           # [第2-3周] 仿真主循环        → 实现 run()
│   └── schedulers/
│       ├── base.py            # [已给] Scheduler 接口与 UserState
│       ├── round_robin.py     # [第2周] RR 调度器           → 实现
│       └── max_rate.py        # [第3周] Max-Rate 调度器     → 实现
├── scripts/
│   └── run_experiment.py      # [第4周] 多种子对比实验（对比循环已给，画图待补）
└── tests/                     # [已给] 每周验收测试，先写测试再实现
```

标记说明：

- **[已给]**：由本骨架提供，直接使用，不必重写（但要读懂）。
- **[第X周]**：留给你独立实现，文件内有接口规格说明（docstring），先看规格、再写测试预期、最后实现。
  实现前这些方法会抛出 `NotImplementedError`，对应周的测试会失败，这是预期行为。

## 环境搭建

```powershell
cd D:\code\engineering
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 四周任务与验收

| 周次 | 任务 | 验收命令 |
|------|------|----------|
| 第 1 周 | 实现 `queue.py` FIFO 队列；学会用 pytest 和断点调试 | `pytest -m week1` |
| 第 2 周 | 实现 `arrivals.py` 到达过程、`round_robin.py` RR 调度器、`metrics.py` 公平性 | `pytest -m week2` |
| 第 3 周 | 实现 `channel.py` 时变信道、`max_rate.py` 调度器、`simulator.py` 主循环 | `pytest -m week3` |
| 第 4 周 | 补全 `scripts/run_experiment.py` 画图；多种子对比 RR 与 Max-Rate；无 AI 复述并解释结果 | `pytest -m week4` |

全部测试：

```powershell
pytest -v
```

## 独立编程守则（重要）

按照学习路线第六节，本项目的使用方式如下：

1. **先自己写**：每个周任务先独立编码 30～45 分钟，遇到问题先查文档、报错信息和调试器。
2. **只问提示，不索要实现**：向 AI 提问时只允许问"错误原因""思路提示"，不允许让 AI 直接给出完整实现。
3. **测试先行**：`tests/` 里的验收标准已经写好，实现前先读懂测试在约束什么行为。
4. **最后才 Code Review**：测试全部通过后，再让 AI 审查代码结构、复杂度和遗漏的边界情况。
5. **每周末无 AI 小项目**：选一个 2～3 小时的独立小实现（不借助生成式 AI），写在自己的笔记里。

## 第 4 周实验验收标准

- 相同配置、相同随机种子集合下对比 RR 与 Max-Rate。
- 报告指标：总吞吐量、每用户吞吐量、Jain 公平性、平均 HOL 时延、调度器决策耗时。
- 能口头解释：为什么 Max-Rate 吞吐量更高但公平性更差？RR 的公平性为什么是 1.0？

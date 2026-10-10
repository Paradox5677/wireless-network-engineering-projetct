"""第 4 周：多种子对比实验脚本。

已给部分：配置加载、调度器注册、多种子循环、汇总均值、结果打印与 CSV 保存。
待你补全（第 4 周）：用 matplotlib 绘制吞吐量与公平性对比图并保存到 results/。

用法::

    python scripts/run_experiment.py
    python scripts/run_experiment.py --config config/default.json
"""
from __future__ import annotations

import argparse
import csv
import statistics
import sys
from pathlib import Path

# 允许直接 `python scripts/run_experiment.py` 运行，无需安装包
_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from scheduler_lab.config import load_config
from scheduler_lab.schedulers.max_rate import MaxRateScheduler
from scheduler_lab.schedulers.round_robin import RoundRobinScheduler
from scheduler_lab.simulator import Simulator, ExperimentResult

SCHEDULERS = {
    RoundRobinScheduler.name: RoundRobinScheduler,
    MaxRateScheduler.name: MaxRateScheduler,
}

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"


def run_all(config: dict) -> list[ExperimentResult]:
    """对每个调度器 × 每个 seed 运行一次仿真。"""
    results: list[ExperimentResult] = []
    for name, scheduler_cls in SCHEDULERS.items():
        for seed in config["seeds"]:
            sim = Simulator(config, scheduler_cls(), seed=seed)
            results.append(sim.run())
    return results


def summarize(results: list[ExperimentResult]) -> dict[str, dict[str, float]]:
    """按调度器汇总各指标的均值。"""
    summary: dict[str, dict[str, float]] = {}
    for name in SCHEDULERS:
        rows = [r for r in results if r.scheduler_name == name]
        summary[name] = {
            "total_throughput_bps": statistics.mean(r.total_throughput_bps for r in rows),
            "jain_fairness": statistics.mean(r.jain_fairness for r in rows),
            "mean_hol_delay_slots": statistics.mean(r.mean_hol_delay_slots for r in rows),
            "decision_time_s": statistics.mean(r.decision_time_s for r in rows),
        }
    return summary


def save_csv(results: list[ExperimentResult], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["scheduler", "seed", "total_throughput_bps", "jain_fairness",
             "mean_hol_delay_slots", "decision_time_s"]
        )
        for r in results:
            writer.writerow(
                [r.scheduler_name, r.seed, r.total_throughput_bps, r.jain_fairness,
                 r.mean_hol_delay_slots, r.decision_time_s]
            )


def plot_results(summary: dict[str, dict[str, float]], path: Path) -> None:
    """TODO(第4周): 绘制对比图。

    要求：
    - 两张子图：左图为各调度器总吞吐量（柱状图），右图为 Jain 公平性（柱状图）。
    - x 轴为调度器名称，柱顶标注数值（保留 2 位小数）。
    - 保存为 path（PNG）。
    - 提示：import matplotlib.pyplot as plt，plt.subplots(1, 2)，
      中文标签如需显示可只用英文标签避免字体问题。
    """
    raise NotImplementedError("第 4 周任务：用 matplotlib 绘制吞吐量/公平性对比图")


def main() -> None:
    parser = argparse.ArgumentParser(description="RR vs Max-Rate 多种子对比实验")
    parser.add_argument("--config", default=None, help="JSON 配置文件路径")
    parser.add_argument("--no-plot", action="store_true", help="跳过绘图")
    args = parser.parse_args()

    config = load_config(args.config)
    results = run_all(config)
    summary = summarize(results)

    print(f"{'scheduler':<14}{'throughput(bps)':>18}{'fairness':>12}"
          f"{'HOL(slots)':>13}{'decision(s)':>13}")
    for name, m in summary.items():
        print(f"{name:<14}{m['total_throughput_bps']:>18.1f}{m['jain_fairness']:>12.4f}"
              f"{m['mean_hol_delay_slots']:>13.2f}{m['decision_time_s']:>13.6f}")

    save_csv(results, RESULTS_DIR / "raw_results.csv")
    print(f"原始结果已保存到 {RESULTS_DIR / 'raw_results.csv'}")

    if not args.no_plot:
        plot_results(summary, RESULTS_DIR / "comparison.png")
        print(f"对比图已保存到 {RESULTS_DIR / 'comparison.png'}")


if __name__ == "__main__":
    main()

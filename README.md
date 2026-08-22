# 四足机器人极限跑酷复现

本仓库记录基于 Isaac Lab 的四足机器人跑酷策略复现，包括教师策略、深度视觉学生策略、正式评测、完整运行日志和演示视频。

## 评测结果

已在 NVIDIA GeForce RTX 4090 24 GB 上完成 Teacher 与 Student 的正式评测。

评测使用 256 个并行环境和 1,500 个仿真步。

| 策略 | 平均奖励 | 平均回合长度 | 路点完成率 | 边缘违规 |
|---|---:|---:|---:|---:|
| 教师策略 | 26.11 ± 7.24 | 924.49 ± 257.87 | 0.99 ± 0.04 | 0.16 ± 0.42 |
| 学生策略 | 19.63 ± 8.78 | 893.85 ± 314.61 | 0.88 ± 0.28 | 0.15 ± 0.41 |

完整评测配置、文件校验值、原始日志和演示视频见[结果汇总](results/official_checkpoints/README.md)。

## 主要结论

- 教师策略的平均路点完成率达到 0.99，能够稳定完成完整障碍路线。
- 学生策略保留了教师策略约 96.7% 的平均回合长度，平均路点完成率达到 0.88。
- 学生策略的平均奖励比教师策略低约 24.8%，但深度视觉策略仍能完成大部分跑酷任务。
- 两种策略的边缘违规水平接近，差异远小于各自的标准差。

## 安装方法

先进入 Isaac Lab 所在目录，再克隆并安装本项目：

```bash
git clone <你的仓库地址>
cd Isaaclab_Parkour
pip install -e .
cd parkour_tasks
pip install -e .
```

## 训练教师策略

```bash
python scripts/rsl_rl/train.py --task Isaac-Extreme-Parkour-Teacher-Unitree-Go2-v0 --seed 1 --headless
```

## 训练学生策略

```bash
python scripts/rsl_rl/train.py --task Isaac-Extreme-Parkour-Student-Unitree-Go2-v0 --seed 1 --headless
```

## 运行教师策略

```bash
python scripts/rsl_rl/play.py --task Isaac-Extreme-Parkour-Teacher-Unitree-Go2-Play-v0 --num_envs 16
```

## 评测教师策略

```bash
python scripts/rsl_rl/evaluation.py --task Isaac-Extreme-Parkour-Teacher-Unitree-Go2-Eval-v0 --checkpoint <教师检查点路径> --headless
```

## 运行学生策略

```bash
python scripts/rsl_rl/play.py --task Isaac-Extreme-Parkour-Student-Unitree-Go2-Play-v0 --num_envs 16
```

## 评测学生策略

```bash
python scripts/rsl_rl/evaluation.py --task Isaac-Extreme-Parkour-Student-Unitree-Go2-Eval-v0 --checkpoint <学生检查点路径> --headless
```

## 仿真部署

教师策略：

```bash
python scripts/rsl_rl/demo.py --task Isaac-Extreme-Parkour-Teacher-Unitree-Go2-Play-v0
```

学生策略：

```bash
python scripts/rsl_rl/demo.py --task Isaac-Extreme-Parkour-Student-Unitree-Go2-Play-v0
```

## 相机控制

- 按 `1` 或 `2`：切换到指定环境。
- 按 `8`：相机向前移动。
- 按 `4`：相机向左移动。
- 按 `6`：相机向右移动。
- 按 `5`：相机向后移动。
- 按 `0`：启用鼠标自由相机。
- 按 `1`：退出自由相机。

## 结果文件

- [Teacher 演示视频](https://github.com/std-song/Isaaclab_Parkour_Reproduction/blob/codex/official-checkpoint-results/results/official_checkpoints/teacher_parkour.mp4)
- [Student 演示视频](https://github.com/std-song/Isaaclab_Parkour_Reproduction/blob/codex/official-checkpoint-results/results/official_checkpoints/student_parkour.mp4)
- [Teacher 完整评测日志](https://github.com/std-song/Isaaclab_Parkour_Reproduction/blob/codex/official-checkpoint-results/results/official_checkpoints/teacher_evaluation.log)
- [Student 完整评测日志](https://github.com/std-song/Isaaclab_Parkour_Reproduction/blob/codex/official-checkpoint-results/results/official_checkpoints/student_evaluation.log)
- [中文评测汇总](https://github.com/std-song/Isaaclab_Parkour_Reproduction/blob/codex/official-checkpoint-results/results/official_checkpoints/README.md)
- [机器可读指标与校验值](https://github.com/std-song/Isaaclab_Parkour_Reproduction/blob/codex/official-checkpoint-results/results/official_checkpoints/metrics.json)

## 兼容性说明

本分支包含 Isaac Lab 2.1 所需的观测维度处理和无界面深度相机配置修改，用于正确加载并评测学生策略检查点。

## 致谢

最后感谢 [Isaaclab_Parkour](https://github.com/CAI23sbP/Isaaclab_Parkour) 提供的开源实现与官方检查点。

# ASAP - Active Symbolic Accelerated Platform

**主动符号加速平台** —— 基于 SISSO + MACE 的主动学习材料发现工作流

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Conda](https://img.shields.io/badge/conda-forge-sissopp-green.svg)](https://anaconda.org/conda-forge/sissopp)

> 💡 **第一次使用？** 请从 [START_HERE.md](START_HERE.md) 开始！  
> 📚 **命令参考：** [scripts/COMMAND_REFERENCE.md](scripts/COMMAND_REFERENCE.md)

---

## 📋 项目简介

ASAP (Active Symbolic Accelerated Platform) 是一个用于材料发现的自动化工作流平台，结合了：

- **SISSO** (Sure Independence Screening and Sparsifying Operator) — 符号回归生成可解释的数学公式
- **MACE** (Machine Learning Force Fields) — 高效的机器学习势函数用于能量计算
- **主动学习** — 智能选择最有价值的候选材料进行计算

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🔬 **符号回归** | SISSO 生成可解释的物理描述符公式 |
| 🤖 **机器学习势函数** | MACE 提供高效的能量和力计算 |
| 🎯 **主动学习** | UCB 采集函数智能选择候选材料 |
| 🔄 **动态映射** | 实时更新 MACE 能量 → g_pbx 映射关系 |
| 📊 **不确定性量化** | 随机森林估计预测不确定性 |
| 🚀 **一键安装** | Conda 环境自动配置 |
| 📝 **配置驱动** | INPUT 文件轻松调整所有参数 |

---

## 🚀 快速开始

### 1. 安装

```bash
# 克隆或下载项目后
cd sisso_mace_al_workflow
./install/install.sh
```

### 2. 配置

编辑 `config/INPUT` 文件，设置你的数据路径和参数：

```bash
# 训练数据路径
TRAIN_DATA = scripts/sisso/nested_CV/data.csv

# 候选数据库
CANDIDATE_DB = data/benchmark/design.db

# MACE 模型
MACE_MODEL = mace_model/2023-12-03-mace-128-L1_epoch-199.model

# 输出目录
OUTPUT_DIR = asap_output
```

### 3. 运行

```bash
# 激活环境
conda activate asap

# 运行工作流
asap -r

# 查看帮助
asap -h
```

### 4. 查看结果

```bash
# 输出目录包含：
ls asap_output/
# - model_info.json              # 模型性能信息
# - active_learning_history.csv  # 主动学习历史
# - sisso_initial/               # 初始 SISSO 模型
# - sisso_final/                 # 最终 SISSO 模型
# - sisso_al/                    # 迭代过程中的模型
```

---

## 📦 安装说明

### 系统要求

| 组件 | 要求 |
|------|------|
| **操作系统** | Linux (Ubuntu 20.04+), macOS, Windows (WSL2) |
| **Python** | 3.9 - 3.11 |
| **内存** | 至少 16GB RAM（推荐 32GB） |
| **存储** | 至少 10GB 可用空间 |
| **GPU** | 可选（NVIDIA CUDA 用于加速 MACE） |

### 安装步骤

详细安装指南请查看 [install/INSTALL.md](install/INSTALL.md)

**快速安装:**
```bash
./install/install.sh
```

### 验证安装

```bash
conda activate asap
asap -c
```

---

## ⚙️ 配置参数

所有参数在 `config/INPUT` 文件中配置。主要参数分类：

### 数据路径（必填）

| 参数 | 说明 |
|------|------|
| `TRAIN_DATA` | 训练数据 CSV 文件路径 |
| `CANDIDATE_DB` | 候选材料 ASE 数据库路径 |
| `MACE_MODEL` | MACE 模型文件路径 |
| `OUTPUT_DIR` | 输出目录 |

### SISSO 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `N_DIM` | 2 | 描述符维度 (1-3) |
| `MAX_RUNG` | 2 | 公式层级 (0-3) |
| `N_SIS_SELECT` | 50 | SIS 筛选特征数 |

### 主动学习参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `AL_N_ITERATIONS` | 30 | 迭代次数 |
| `AL_BATCH_SIZE` | 5 | 每批选择材料数 |
| `AL_UCB_KAPPA` | 0.1 | UCB 探索参数 |

### MACE 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `MACE_DEVICE` | cpu | 计算设备 (cpu/cuda) |
| `MACE_RELAX` | False | 是否进行结构弛豫 |

详细配置说明请查看 `config/INPUT` 文件中的注释。

---

## 📊 输出结果

### 输出目录结构

```
asap_output/
├── model_info.json                 # 模型性能总结
├── active_learning_history.csv     # 主动学习历史
├── sisso_initial/                  # 初始 SISSO 模型
│   ├── model.json
│   └── descriptors.txt
├── sisso_final/                    # 最终 SISSO 模型
│   ├── model.json
│   └── descriptors.txt
└── sisso_al/                       # 迭代模型
    ├── iter_0/
    ├── iter_1/
    └── ...
```

### model_info.json 示例

```json
{
  "workflow": "SISSO + MACE Active Learning",
  "timestamp": "2026-03-28T12:00:00",
  "initial_model": {
    "r2_test": 0.7143,
    "rmse_test": 0.6014
  },
  "final_model": {
    "r2_test": 0.7531,
    "rmse_test": 0.5590
  },
  "improvement": {
    "r2_change": 0.0388,
    "rmse_change": -0.0424
  },
  "active_learning": {
    "n_iterations": 30,
    "n_calculated": 150,
    "train_size_increase": 150
  }
}
```

---

## 📖 使用文档

| 文档 | 说明 |
|------|------|
| [README.md](README.md) | 项目说明（本文件） |
| [install/INSTALL.md](install/INSTALL.md) | 详细安装指南 |
| [USAGE.md](USAGE.md) | 使用说明和参数详解 |
| [docs/QUICKSTART.md](docs/QUICKSTART.md) | 快速入门教程 |

---

## 🔧 命令行工具

ASAP 提供简洁的命令行接口：

```bash
# 查看帮助
asap -h

# 检查环境和依赖
asap -c

# 运行工作流
asap -r

# 使用指定配置文件
asap -r /path/to/INPUT

# 显示版本
asap -v
```

---

## 🎓 配置示例

### 快速测试配置

用于快速验证安装（~5 分钟）:

```
AL_N_ITERATIONS = 5
AL_BATCH_SIZE = 3
MACE_RELAX = False
QUICK_TEST = True
```

### 标准生产配置

推荐用于正式计算（~1-2 小时）:

```
AL_N_ITERATIONS = 30
AL_BATCH_SIZE = 5
MACE_RELAX = False
QUICK_TEST = False
```

### 高精度配置

追求最高精度（需要 GPU，~数小时）:

```
AL_N_ITERATIONS = 50
AL_BATCH_SIZE = 10
MACE_RELAX = True
MACE_DEVICE = cuda
```

---

## 🐛 故障排除

### 常见问题

**Q: MACE 计算速度慢？**

A: 
- 关闭结构弛豫：`MACE_RELAX = False`
- 使用 GPU：`MACE_DEVICE = cuda`
- 减少批次大小：`AL_BATCH_SIZE = 3`

**Q: SISSO 训练失败？**

A:
- 检查数据文件路径是否正确
- 确保特征列名称与数据文件匹配
- 尝试减少 `N_DIM` 或 `MAX_RUNG`

**Q: 内存不足？**

A:
- 减少候选材料数量
- 使用更小的 `AL_BATCH_SIZE`
- 增加系统内存或使用 swap

详细故障排除请查看 [install/INSTALL.md](install/INSTALL.md) 的常见问题部分。

---

## 📚 依赖版本

| 包名 | 版本 | 来源 |
|------|------|------|
| Python | 3.10 | python.org |
| sissopp | >=1.2 | conda-forge |
| mace-ml | >=0.3 | conda-forge |
| ase | >=3.22 | conda-forge |
| pandas | >=2.0 | conda-forge |
| numpy | >=1.24 | conda-forge |
| scikit-learn | >=1.3 | conda-forge |
| matplotlib | >=3.7 | conda-forge |

---

## 🙏 致谢

- **SISSO 开发团队** — [CompRhysGroup/sisso++](https://github.com/CompRhysGroup/sisso++)
- **MACE 开发团队** — [ACEsuit/mace](https://github.com/ACEsuit/mace)

---

## 📝 许可证

本项目基于学术论文代码整理，请遵守原论文的引用规范。

---

## 📧 联系方式

如有问题，请查看文档或提交 issue。

**引用本软件:**

```bibtex
@article{sisso-mace-workflow2025,
  title={Materials-discovery workflow guided by symbolic regression for identifying acid-stable oxides for electrocatalysis},
  journal={npj Computational Materials},
  year={2025},
  doi={10.1038/s41524-025-01596-4}
}
```

---

<div align="center">

**Made with ❤️ by NewtonYe**

[📄 论文](https://www.nature.com/articles/s41524-025-01596-4) | [📚 文档](docs/) | [🐛 问题](issues) | [📦 发布说明](install/RELEASE_NOTES.md)

</div>

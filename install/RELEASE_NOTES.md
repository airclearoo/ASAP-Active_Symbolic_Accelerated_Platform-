# ASAP v1.0.0 发布说明

**发布日期**: 2026-03-28  
**版本**: 1.0.0  
**作者**: NewtonYe

---

## 🎉 发布信息

ASAP (Active Symbolic Accelerated Platform) v1.0.0 正式发布！

这是一个基于 SISSO + MACE 的主动学习材料发现工作流平台，实现了论文《Materials-discovery workflow guided by symbolic regression for identifying acid-stable oxides for electrocatalysis》(npj Computational Materials, 2025) 中描述的方法。

---

## ✨ 核心功能

- 🔬 **符号回归** — SISSO 生成可解释的物理描述符公式
- 🤖 **机器学习势函数** — MACE 提供高效的能量计算
- 🎯 **主动学习** — UCB 采集函数智能选择候选材料
- 🔄 **动态映射** — 实时更新 MACE 能量 → g_pbx 映射
- 📊 **不确定性量化** — 随机森林估计预测不确定性

---

## 🚀 快速开始

### 安装

```bash
cd sisso_mace_al_workflow
./install.sh
```

### 配置

编辑 `config/INPUT` 文件，设置数据路径和参数。

### 运行

```bash
conda activate asap
python asap.py run
```

---

## 📦 本次发布包含

### 核心文件

| 文件 | 说明 |
|------|------|
| `asap.py` | 主入口脚本 |
| `workflow_active_learning_mace_fixed.py` | 主工作流脚本 |
| `config/INPUT` | 用户配置文件 |
| `config/config_loader.py` | 配置加载器 |

### 安装脚本

| 文件 | 说明 |
|------|------|
| `install.sh` | 一键安装脚本 |
| `run.sh` | 运行脚本 |

### 文档

| 文件 | 说明 |
|------|------|
| `README.md` | 项目说明 |
| `INSTALL.md` | 安装指南 |
| `USAGE.md` | 使用说明 |
| `docs/QUICKSTART.md` | 快速入门 |
| `MANIFEST.md` | 文件清单 |
| `PACKAGING_SUMMARY.md` | 包装总结 |

### 项目配置

| 文件 | 说明 |
|------|------|
| `.gitignore` | Git 忽略配置 |
| `LICENSE` | MIT 许可证 |
| `CITATION.cff` | 引用配置 |
| `pyproject.toml` | Python 项目配置 |

### 测试

| 文件 | 说明 |
|------|------|
| `tests/test_config_loader.py` | 配置加载器测试 |

---

## 📋 系统要求

| 组件 | 要求 |
|------|------|
| **操作系统** | Linux/macOS/WSL2 |
| **Python** | 3.9 - 3.11 |
| **内存** | 16GB+ RAM |
| **存储** | 10GB+ |
| **Conda** | Miniconda/Anaconda |

---

## 🔧 命令行工具

```bash
# 显示帮助
python asap.py info

# 检查环境
python asap.py check

# 运行工作流
python asap.py run

# 使用自定义配置
python asap.py run /path/to/INPUT
```

---

## 📊 配置参数

主要配置参数在 `config/INPUT` 文件中：

### 数据路径（必填）
- `TRAIN_DATA` - 训练数据
- `CANDIDATE_DB` - 候选数据库
- `MACE_MODEL` - MACE 模型
- `OUTPUT_DIR` - 输出目录

### SISSO 参数
- `N_DIM` - 描述符维度 (1-3)
- `MAX_RUNG` - 公式层级 (0-3)
- `ALLOWED_OPS` - 数学运算

### 主动学习参数
- `AL_N_ITERATIONS` - 迭代次数
- `AL_BATCH_SIZE` - 批次大小
- `AL_UCB_KAPPA` - UCB 探索参数

### MACE 参数
- `MACE_DEVICE` - 计算设备 (cpu/cuda)
- `MACE_RELAX` - 结构弛豫开关

---

## 📈 配置预设

### 快速测试
```
AL_N_ITERATIONS = 5
AL_BATCH_SIZE = 3
MACE_RELAX = False
QUICK_TEST = True
```

### 标准生产（推荐）
```
AL_N_ITERATIONS = 30
AL_BATCH_SIZE = 5
MACE_RELAX = False
QUICK_TEST = False
```

### 高精度
```
AL_N_ITERATIONS = 50
AL_BATCH_SIZE = 10
MACE_RELAX = True
MACE_DEVICE = cuda
```

---

## 🐛 已知问题

暂无已知问题。

---

## 📚 文档

- [README.md](README.md) - 项目说明
- [INSTALL.md](INSTALL.md) - 安装指南
- [USAGE.md](USAGE.md) - 使用说明
- [docs/QUICKSTART.md](docs/QUICKSTART.md) - 快速入门

---

## 🔗 相关资源

- **论文**: https://www.nature.com/articles/s41524-025-01596-4
- **SISSO**: https://github.com/CompRhysGroup/sisso++
- **MACE**: https://github.com/ACEsuit/mace
- **ASE**: https://wiki.fysik.dtu.dk/ase/

---

## 📝 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- SISSO 开发团队
- MACE 开发团队
- 论文作者：Materials-discovery workflow guided by symbolic regression

---

## 📧 联系方式

如有问题，请查看文档或提交 issue。

---

<div align="center">

**ASAP v1.0.0** | Made with ❤️ by NewtonYe

</div>

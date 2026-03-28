# ASAP 快速入门指南

5 分钟快速上手 ASAP 工作流

---

## 🎯 本指南适合

- 第一次使用 ASAP 的用户
- 想快速验证安装是否成功
- 想了解基本工作流程

---

## 📦 步骤 1: 安装（3-5 分钟）

```bash
# 进入项目目录
cd sisso_mace_al_workflow

# 运行一键安装脚本
./install/install.sh
```

安装完成后会看到：
```
✓ 所有依赖安装成功!

使用方法:
  1. 激活环境：conda activate asap
  2. 配置参数：编辑 config/INPUT 文件
  3. 运行工作流：python asap.py run
```

---

## ✅ 步骤 2: 验证安装（30 秒）

```bash
conda activate asap
python asap.py check
```

看到以下输出表示安装成功：
```
✓ 所有检查通过！环境配置正确。
```

---

## ⚙️ 步骤 3: 配置（1 分钟）

编辑 `config/INPUT` 文件，确认以下路径正确：

```bash
# 打开配置文件
nano config/INPUT
# 或使用你喜欢的编辑器
vim config/INPUT
```

检查这些关键参数：

```
# 训练数据路径（确保文件存在）
TRAIN_DATA = scripts/sisso/nested_CV/data.csv

# 候选数据库（确保文件存在）
CANDIDATE_DB = data/benchmark/design.db

# MACE 模型（确保文件存在）
MACE_MODEL = mace_model/2023-12-03-mace-128-L1_epoch-199.model

# 输出目录（会自动创建）
OUTPUT_DIR = asap_output
```

**快速测试配置**（首次运行建议）:

```
AL_N_ITERATIONS = 5      # 减少迭代次数，快速测试
AL_BATCH_SIZE = 3        # 减小批次大小
QUICK_TEST = True        # 启用快速测试模式
```

---

## 🚀 步骤 4: 运行（2-10 分钟）

```bash
# 确保环境已激活
conda activate asap

# 运行工作流
python asap.py run
```

运行过程中会看到类似输出：
```
================================================================================
  ASAP - Active Symbolic Accelerated Platform
================================================================================

使用默认配置：config/INPUT

配置参数:
  训练数据：scripts/sisso/nested_CV/data.csv
  候选数据库：data/benchmark/design.db
  MACE 模型：mace_model/2023-12-03-mace-128-L1_epoch-199.model
  输出目录：asap_output
  迭代次数：5
  批次大小：3
  MACE 弛豫：False

验证数据文件...
✓ 所有数据文件存在

================================================================================
开始运行工作流...
================================================================================

步骤 1: 加载数据
  加载训练数据：scripts/sisso/nested_CV/data.csv
    样本数：114
    特征数：14
...
```

---

## 📊 步骤 5: 查看结果（1 分钟）

运行完成后，查看输出目录：

```bash
ls asap_output/
```

输出文件说明：

| 文件/目录 | 说明 |
|-----------|------|
| `model_info.json` | 模型性能总结（R², RMSE 等） |
| `active_learning_history.csv` | 主动学习历史 |
| `sisso_initial/` | 初始 SISSO 模型 |
| `sisso_final/` | 最终 SISSO 模型 |
| `sisso_al/` | 迭代过程中的模型 |

查看模型性能：

```bash
cat asap_output/model_info.json
```

示例输出：
```json
{
  "workflow": "SISSO + MACE Active Learning",
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
  }
}
```

---

## 🎉 完成！

你已经成功运行了 ASAP 工作流！

### 下一步

1. **调整参数** — 编辑 `config/INPUT` 尝试不同配置
2. **正式运行** — 设置 `AL_N_ITERATIONS = 30` 进行完整计算
3. **查看文档** — 阅读 [USAGE.md](../USAGE.md) 和 [install/INSTALL.md](../install/INSTALL.md)

---

## 🔧 常用命令

```bash
# 查看帮助
python asap.py info

# 检查环境
python asap.py check

# 运行工作流
python asap.py run

# 使用自定义配置
python asap.py run /path/to/my_INPUT
```

---

## 🐛 遇到问题？

### 问题：找不到数据文件

**解决**: 检查 `config/INPUT` 中的路径是否正确，确保文件存在：

```bash
ls scripts/sisso/nested_CV/data.csv
ls data/benchmark/design.db
ls mace_model/*.model
```

### 问题：Conda 环境未激活

**解决**: 

```bash
conda activate asap
```

### 问题：MACE 计算很慢

**解决**: 在 `config/INPUT` 中设置：

```
MACE_RELAX = False
```

### 更多帮助

- 详细安装指南：[install/INSTALL.md](../install/INSTALL.md)
- 使用说明：[USAGE.md](../USAGE.md)
- 项目说明：[README.md](../README.md)

---

<div align="center">

**祝你使用愉快！** 🍃

</div>

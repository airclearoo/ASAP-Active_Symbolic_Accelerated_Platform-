# ASAP 使用说明

本文档详细介绍 ASAP 的所有功能、配置参数和使用方法。

---

## 📖 目录

1. [快速开始](#快速开始)
2. [配置参数详解](#配置参数详解)
3. [命令行工具](#命令行工具)
4. [工作流程](#工作流程)
5. [输出结果](#输出结果)
6. [参数调优](#参数调优)
7. [故障排除](#故障排除)

---

## 🚀 快速开始

### 基本流程

```bash
# 1. 激活环境
conda activate asap

# 2. 编辑配置（可选）
nano config/INPUT

# 3. 运行工作流
python asap.py run

# 4. 查看结果
cat asap_output/model_info.json
```

### 配置文件位置

- **默认配置**: `config/INPUT`
- **自定义配置**: 任意路径，运行时指定

---

## ⚙️ 配置参数详解

所有参数在 `config/INPUT` 文件中配置。

### 数据路径（必填）

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `TRAIN_DATA` | 路径 | 训练数据 CSV 文件 | `scripts/sisso/nested_CV/data.csv` |
| `CANDIDATE_DB` | 路径 | 候选材料 ASE 数据库 | `data/benchmark/design.db` |
| `MACE_MODEL` | 路径 | MACE 模型文件 | `mace_model/model.model` |
| `OUTPUT_DIR` | 路径 | 输出目录 | `asap_output` |

### SISSO 参数

| 参数 | 默认值 | 范围 | 说明 |
|------|--------|------|------|
| `PROP_LABEL` | `g_pbx` | - | 目标属性名称 |
| `PROP_UNIT` | `eV/atom` | - | 目标属性单位 |
| `ALLOWED_OPS` | `add,sub,mult,div,inv,sq,sqrt,cbrt,log,abs` | - | 允许的数学运算 |
| `N_DIM` | `2` | 1-3 | 描述符维度 |
| `MAX_RUNG` | `2` | 0-3 | 公式层级 |
| `N_SIS_SELECT` | `50` | ≥10 | SIS 筛选特征数 |
| `N_RESIDUAL` | `5` | ≥1 | 残差维度 |
| `L_BOUND` | `1e-5` | >0 | 系数下界 |
| `U_BOUND` | `1e+5` | >0 | 系数上界 |

#### SISSO 参数说明

**N_DIM（描述符维度）**:
- `1`: 简单线性公式，解释性强
- `2`: 平衡复杂度和解释性（推荐）
- `3`: 复杂公式，可能过拟合

**MAX_RUNG（公式层级）**:
- `0`: 仅原始特征
- `1`: 单层运算（如 `log(IP)`）
- `2`: 双层运算（如 `log(IP/r_cov)`）（推荐）
- `3`: 三层运算，非常复杂

**ALLOWED_OPS（数学运算）**:
- `add`: 加法 (+)
- `sub`: 减法 (-)
- `mult`: 乘法 (×)
- `div`: 除法 (÷)
- `inv`: 倒数 (1/x)
- `sq`: 平方 (x²)
- `sqrt`: 平方根 (√x)
- `cbrt`: 立方根 (∛x)
- `log`: 自然对数 (ln x)
- `abs`: 绝对值 (|x|)

### 主动学习参数

| 参数 | 默认值 | 范围 | 说明 |
|------|--------|------|------|
| `AL_N_ITERATIONS` | `30` | ≥1 | 主动学习迭代次数 |
| `AL_BATCH_SIZE` | `5` | ≥1 | 每批选择的材料数 |
| `AL_UCB_KAPPA` | `0.1` | 0.01-0.5 | UCB 探索参数 |
| `TEST_SIZE` | `0.2` | 0.1-0.5 | 测试集比例 |
| `RANDOM_STATE` | `42` | - | 随机种子 |

#### 主动学习参数说明

**AL_N_ITERATIONS（迭代次数）**:
- `5-10`: 快速测试
- `30`: 标准配置（推荐）
- `50-100`: 高精度计算

**AL_BATCH_SIZE（批次大小）**:
- `1-3`: 精细选择，每次迭代计算量少
- `5`: 平衡选择（推荐）
- `10-20`: 快速完成，但可能错过最优材料

**AL_UCB_KAPPA（探索参数）**:
- `0.01-0.05`: 更多利用（选择预测值好的）
- `0.1`: 平衡探索和利用（推荐）
- `0.2-0.5`: 更多探索（选择不确定性高的）

UCB 公式：`UCB = 预测值 - κ × 不确定性`

### MACE 参数

| 参数 | 默认值 | 选项 | 说明 |
|------|--------|------|------|
| `MACE_DEVICE` | `cpu` | `cpu`, `cuda` | 计算设备 |
| `MACE_RELAX` | `False` | `True`, `False` | 是否进行结构弛豫 |
| `MACE_RELAX_FMAX` | `0.05` | >0 | 弛豫收敛标准 (eV/Å) |
| `MACE_RELAX_STEPS` | `50` | ≥1 | 最大弛豫步数 |

#### MACE 参数说明

**MACE_DEVICE（计算设备）**:
- `cpu`: CPU 计算，兼容性好
- `cuda`: GPU 加速（需要 NVIDIA GPU 和 CUDA）

**MACE_RELAX（结构弛豫）**:
- `True`: 进行结构弛豫，结果更准确，计算慢
- `False`: 直接计算单点能，速度快（推荐用于测试）

### 性能调优参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `RF_N_ESTIMATORS` | `50` | 随机森林树的数量（不确定性估计） |
| `SUPPRESS_WARNINGS` | `True` | 是否启用警告过滤 |
| `MATPLOTLIB_BACKEND` | `Agg` | matplotlib 后端 |

### 调试选项

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `DEBUG_MODE` | `False` | 调试模式（输出详细信息） |
| `QUICK_TEST` | `False` | 快速测试模式 |
| `QUICK_TEST_ITERATIONS` | `5` | 快速测试迭代次数 |

---

## 🛠️ 命令行工具

### 命令列表

```bash
# 显示帮助信息
python asap.py info

# 检查环境和依赖
python asap.py check

# 运行工作流（默认配置）
python asap.py run

# 运行工作流（指定配置文件）
python asap.py run /path/to/INPUT
```

### 使用运行脚本

```bash
# 使用默认配置
./run.sh

# 使用自定义配置
./run.sh /path/to/INPUT
```

---

## 📊 工作流程

ASAP 工作流程包含以下步骤：

```
┌─────────────────────────────────────────────────────────────┐
│  步骤 1: 加载数据                                            │
│  - 读取训练数据 (CSV)                                        │
│  - 读取候选数据库 (ASE .db)                                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤 2: 数据划分                                            │
│  - 训练集 (80%)                                              │
│  - 测试集 (20%)                                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤 3: 训练初始 SISSO 模型                                   │
│  - 生成描述符公式                                            │
│  - 评估模型性能 (R², RMSE)                                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤 4: 初始化 MACE                                         │
│  - 加载预训练模型                                            │
│  - 配置计算设备                                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤 5: 计算候选材料特征                                    │
│  - 从化学式计算 14 个特征                                      │
│  - 原子半径、电负性、电离能等                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤 6: 主动学习循环 (迭代 N 次)                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  6.1 训练当前 SISSO 模型                                  │  │
│  │  6.2 预测候选池                                         │  │
│  │  6.3 计算 UCB 采集函数                                    │  │
│  │  6.4 选择最有价值的材料                                 │  │
│  │  6.5 MACE 计算能量                                        │  │
│  │  6.6 更新映射模型                                       │  │
│  │  6.7 扩展训练集                                         │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤 7: 训练最终模型                                        │
│  - 使用扩展后的训练集                                        │
│  - 输出最终性能指标                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 输出结果

### 输出目录结构

```
asap_output/
├── model_info.json                 # 模型性能总结
├── active_learning_history.csv     # 主动学习历史
├── sisso_initial/                  # 初始 SISSO 模型
│   ├── model.json                  # 模型信息
│   ├── descriptors.txt             # 描述符公式
│   └── predictions.json            # 预测结果
├── sisso_final/                    # 最终 SISSO 模型
│   ├── model.json
│   ├── descriptors.txt
│   └── predictions.json
└── sisso_al/                       # 迭代模型
    ├── iter_0/
    │   ├── model.json
    │   └── descriptors.txt
    ├── iter_1/
    └── ...
```

### model_info.json

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

### active_learning_history.csv

```csv
iteration,formula,predicted,ucb_score
1,Ca2O20,0.0507,-0.0499
1,Ba2O12,0.0499,-0.0492
2,Sr3O15,0.0485,-0.0478
...
```

---

## 🎯 参数调优

### 配置预设

#### 快速测试配置

用于验证安装和快速测试（~5 分钟）:

```
AL_N_ITERATIONS = 5
AL_BATCH_SIZE = 3
MACE_RELAX = False
QUICK_TEST = True
```

#### 标准生产配置

推荐用于正式计算（~1-2 小时）:

```
AL_N_ITERATIONS = 30
AL_BATCH_SIZE = 5
N_DIM = 2
MAX_RUNG = 2
MACE_RELAX = False
QUICK_TEST = False
```

#### 高精度配置

追求最高精度（需要 GPU，~数小时）:

```
AL_N_ITERATIONS = 50
AL_BATCH_SIZE = 10
N_DIM = 2
MAX_RUNG = 2
MACE_RELAX = True
MACE_DEVICE = cuda
RF_N_ESTIMATORS = 100
```

### 性能调优建议

| 问题 | 调整参数 | 效果 |
|------|----------|------|
| 计算太慢 | `AL_N_ITERATIONS ↓`, `AL_BATCH_SIZE ↓`, `MACE_RELAX = False` | 减少计算量 |
| 精度不够 | `AL_N_ITERATIONS ↑`, `N_DIM ↑`, `MAX_RUNG ↑` | 提高模型复杂度 |
| 过拟合 | `N_DIM ↓`, `MAX_RUNG ↓`, `TEST_SIZE ↑` | 简化模型 |
| 探索不足 | `AL_UCB_KAPPA ↑` | 增加探索性 |
| 内存不足 | `AL_BATCH_SIZE ↓`, `RF_N_ESTIMATORS ↓` | 减少内存使用 |

---

## 🐛 故障排除

### 常见问题

#### 问题 1: 找不到 INPUT 配置文件

**错误信息**: `FileNotFoundError: INPUT 配置文件不存在`

**解决**:
```bash
# 检查配置文件是否存在
ls config/INPUT

# 如果不存在，从示例创建
cp config/INPUT.example config/INPUT
```

#### 问题 2: 数据文件路径错误

**错误信息**: `文件缺失：xxx`

**解决**:
```bash
# 检查文件是否存在
ls scripts/sisso/nested_CV/data.csv
ls data/benchmark/design.db
ls mace_model/*.model

# 修改 config/INPUT 中的路径
nano config/INPUT
```

#### 问题 3: MACE 计算速度慢

**解决**:
1. 关闭结构弛豫：`MACE_RELAX = False`
2. 使用 GPU：`MACE_DEVICE = cuda`
3. 减少批次大小：`AL_BATCH_SIZE = 3`

#### 问题 4: SISSO 训练失败

**解决**:
1. 检查数据文件格式
2. 确保特征列名称匹配
3. 减少 `N_DIM` 或 `MAX_RUNG`
4. 增加 `N_SIS_SELECT`

#### 问题 5: 内存溢出

**解决**:
1. 减少候选材料数量
2. 使用更小的 `AL_BATCH_SIZE`
3. 减少 `RF_N_ESTIMATORS`
4. 增加系统 swap 空间

### 获取帮助

1. 查看详细文档：[install/INSTALL.md](install/INSTALL.md)
2. 检查日志输出
3. 启用调试模式：`DEBUG_MODE = True`

---

## 📚 相关资源

- **SISSO 文档**: https://github.com/CompRhysGroup/sisso++
- **MACE 文档**: https://github.com/ACEsuit/mace
- **ASE 文档**: https://wiki.fysik.dtu.dk/ase/

---

<div align="center">

**需要更多帮助？** 查看 [README.md](README.md) 或 [install/INSTALL.md](install/INSTALL.md)

</div>

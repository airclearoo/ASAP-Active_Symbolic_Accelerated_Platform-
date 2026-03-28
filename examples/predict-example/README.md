# SISSO 模型预测示例

本目录包含 SISSO 模型预测功能的示例数据和配置。

---

## 📁 目录结构

```
predict-example/
├── data_for_prediction.csv    # 待预测数据（无目标值）
├── INPUT_PREDICT              # 预测配置文件
└── README.md                  # 本文件
```

---

## 📊 数据说明

### data_for_prediction.csv

这是一个用于预测的示例数据文件，包含：

- **34 个材料**
- **14 个特征**（与训练数据一致）
- **无目标值**（g_pbx 列已移除）

**数据格式**:
```csv
oxide,r_s (AA),r_val (AA),e_H (eV),e_L (eV),AN,EA (eV),IP (eV),r_cov (AA),EN (Pauling),N_val,N_unf,CE (eV),max_OS,stdev_OS
AgO,0.8954,0.8805,-8.65078,...
Al2O3,0.784,0.92705,-10.033,...
...
```

**特征列表**:
1. `r_s (AA)` - 原子半径
2. `r_val (AA)` - 价电子半径
3. `e_H (eV)` - HOMO 能量
4. `e_L (eV)` - LUMO 能量
5. `AN` - 平均原子序数
6. `EA (eV)` - 电子亲和能
7. `IP (eV)` - 电离能
8. `r_cov (AA)` - 共价半径
9. `EN (Pauling)` - 电负性
10. `N_val` - 价电子数
11. `N_unf` - 未充满电子数
12. `CE (eV)` - 结合能
13. `max_OS` - 最大氧化态
14. `stdev_OS` - 氧化态标准差

---

## 🚀 使用方法

### 前提条件

确保已有训练好的 SISSO 模型：

```bash
# 如果还没有模型，先运行主动学习
asap -r
```

模型输出目录：
```
asap_output/
├── sisso_initial/    # 初始模型
├── sisso_final/      # 最终模型（推荐用于预测）
└── sisso_al/         # 迭代模型
```

### 方式 1：使用示例配置

```bash
# 进入示例目录
cd examples/predict-example

# 运行预测
asap -p INPUT_PREDICT
```

### 方式 2：自定义配置

1. **复制配置文件**
   ```bash
   cp scripts/config/INPUT_PREDICT my_predict_config
   ```

2. **编辑配置**
   ```bash
   nano my_predict_config
   ```

   修改关键参数：
   ```
   SISSO_MODEL_DIR = asap_output/sisso_final
   PREDICT_DATA = your_data.csv
   OUTPUT_FILE = your_predictions.csv
   ```

3. **运行预测**
   ```bash
   asap -p my_predict_config
   ```

### 方式 3：使用默认配置

```bash
# 确保 scripts/config/INPUT_PREDICT 已正确配置
asap -p
```

---

## 📝 配置文件说明

### INPUT_PREDICT

**必填参数**:

| 参数 | 说明 | 示例 |
|------|------|------|
| `SISSO_MODEL_DIR` | SISSO 模型目录 | `asap_output/sisso_final` |
| `PREDICT_DATA` | 待预测数据文件 | `data_for_prediction.csv` |
| `OUTPUT_FILE` | 输出文件路径 | `predictions.csv` |

**可选参数**:

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `FEATURE_COLS` | 自动检测 | 特征列名称（逗号分隔） |
| `MATERIAL_NAME_COL` | `oxide` | 材料名称列名 |
| `VERBOSE_OUTPUT` | `False` | 是否输出详细信息 |
| `OUTPUT_FORMAT` | `csv` | 输出格式（csv/json） |

---

## 📊 输出结果

### predictions.csv

预测结果文件格式：

```csv
oxide,predicted_g_pbx
AgO,0.525771
Al2O3,0.424261
AlCuO2,0.563483
...
```

**字段说明**:
- `oxide`: 材料名称
- `predicted_g_pbx`: 预测的 g_pbx 值（eV/atom）

### 详细输出（VERBOSE_OUTPUT=True）

```csv
oxide,predicted_g_pbx,feature_r_s (AA),feature_r_val (AA),...
AgO,0.525771,0.8954,0.8805,...
Al2O3,0.424261,0.784,0.92705,...
...
```

---

## 🔧 常见问题

### 问题 1：模型目录不存在

**错误**: `✗ SISSO 模型目录不存在`

**解决**:
```bash
# 检查模型目录
ls asap_output/sisso_final/

# 如果目录不存在，先运行主动学习
asap -r
```

### 问题 2：数据文件缺少特征列

**错误**: `缺少特征列：[...]`

**解决**:
- 确保数据文件包含所有 14 个特征列
- 特征列名称必须与训练数据完全一致
- 参考 `data_for_prediction.csv` 的格式

### 问题 3：预测结果为 NaN

**原因**: 模型加载失败或特征维度不匹配

**解决**:
1. 检查模型目录是否包含 `model.json`
2. 确认特征列数量和顺序正确
3. 启用调试模式查看详细错误：
   ```
   DEBUG_MODE = True
   ```

---

## 📚 相关文档

- [命令参考](../../scripts/COMMAND_REFERENCE.md) - ASAP 命令说明
- [使用说明](../../USAGE.md) - 完整使用指南
- [快速开始](../../START_HERE.md) - 快速入门

---

<div align="center">

**ASAP 预测功能** | Made with ❤️ by NewtonYe

</div>

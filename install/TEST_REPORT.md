# ASAP 安装与测试报告

**测试日期**: 2026-03-28  
**测试版本**: v1.0.0  
**测试人员**: 小葉助手 🍃

---

## 📋 测试概述

本次测试完整验证了 ASAP 软件的安装流程、命令行工具和工作流运行。

### 测试环境

| 项目 | 信息 |
|------|------|
| **操作系统** | Linux |
| **Python 版本** | 3.10.20 |
| **Conda 环境** | asap |
| **环境路径** | `/home/user/1-yjy/deepmd-kit-20260323/envs/asap` |

### 已安装依赖

| 包名 | 版本 | 状态 |
|------|------|------|
| sissopp | 1.2.0 | ✓ 已安装 |
| mace-torch | 0.3.15 | ✓ 已安装 |
| ase | 3.28.0 | ✓ 已安装 |
| pandas | - | ✓ 已安装 |
| numpy | - | ✓ 已安装 |
| sklearn | - | ✓ 已安装 |
| matplotlib | - | ✓ 已安装 |

---

## ✅ 测试结果

### 1. 命令行工具测试

#### 1.1 帮助命令 (`asap -h`)

**命令**:
```bash
asap -h
```

**结果**: ✅ 通过

**输出**:
```
usage: asap [-h] [-r [CONFIG]] [-c] [-i] [-v]

ASAP - Active Symbolic Accelerated Platform

options:
  -h, --help            show this help message and exit
  -r [CONFIG], --run    运行工作流（可选：指定配置文件路径）
  -c, --check           检查环境和依赖
  -i, --info            显示软件信息
  -v, --version         显示版本号
```

#### 1.2 版本命令 (`asap -v`)

**命令**:
```bash
asap -v
```

**结果**: ✅ 通过

**输出**:
```
ASAP v1.0.0
```

#### 1.3 信息命令 (`asap -i`)

**命令**:
```bash
asap -i
```

**结果**: ✅ 通过

**输出**: 显示软件版本、作者、论文 DOI 和使用方法。

#### 1.4 环境检查 (`asap -c`)

**命令**:
```bash
asap -c
```

**结果**: ✅ 通过

**输出摘要**:
```
[1/6] Python 版本：3.10.20
  ✓ Python 版本符合要求

[2/6] 检查 SISSO...
  ✓ SISSO 已安装

[3/6] 检查 MACE...
  ✓ MACE 已安装

[4/6] 检查 ASE...
  ✓ ASE 已安装

[5/6] 检查科学计算库...
  ✓ pandas 已安装
  ✓ numpy 已安装
  ✓ sklearn 已安装
  ✓ matplotlib 已安装

[6/6] 检查配置文件...
  ✓ INPUT 配置文件存在

✓ 所有检查通过！环境配置正确。
```

---

### 2. 工作流运行测试

#### 2.1 测试配置

**工作目录**: `examples/test-workdir/`  
**配置文件**: `INPUT`  
**测试模式**: 快速测试（5 次迭代）

**关键参数**:
```
AL_N_ITERATIONS = 5
AL_BATCH_SIZE = 3
QUICK_TEST = True
MACE_RELAX = False
```

#### 2.2 运行命令

```bash
cd examples/test-workdir
asap -r INPUT
```

**结果**: ✅ 成功完成

**运行时间**: ~2 分钟

#### 2.3 输出结果

**输出目录**: `test_output/`

**生成文件**:
- `model_info.json` - 模型性能信息
- `active_learning_history.csv` - 主动学习历史
- `sisso_initial/` - 初始 SISSO 模型
- `sisso_final/` - 最终 SISSO 模型
- `sisso_al/` - 迭代模型（iter_0 到 iter_4）

#### 2.4 模型性能

**初始模型**:
- R² = 0.7143
- RMSE = 0.6014 eV/atom

**最终模型**（5 次迭代后）:
- R² = 0.7618
- RMSE = 0.5491 eV/atom

**性能提升**:
- R² 提升：+0.0475 (+6.65%)
- RMSE 降低：-0.0522 (-8.68%)

#### 2.5 主动学习历史

| 迭代 | 材料 | 预测值 (eV/atom) | UCB 分数 |
|------|------|------------------|----------|
| 1 | C4O8 | 0.0715 | -0.0008 |
| 1 | CdHgO2 | 0.1301 | 0.0048 |
| 1 | Hg2O8S2 | 0.1039 | 0.0055 |
| 2 | Cr2Hg10O12 | 0.2165 | 0.1411 |
| 2 | Cd16Mn4O20 | 0.2225 | 0.1461 |
| 2 | Hg6O7Si2 | 0.2289 | 0.1536 |
| 3 | Ca2O20 | 0.2426 | 0.1493 |
| 3 | O12S4 | 0.2457 | 0.1526 |
| 3 | Hg4O28S8 | 0.2413 | 0.1619 |
| 4 | C2Cd2O6 | 0.1872 | 0.1839 |
| 4 | Hg9O18S3 | 0.2140 | 0.1888 |
| 4 | Hg4O8S2 | 0.2251 | 0.1970 |
| 5 | Cd2O8S2 | 0.2290 | 0.1933 |
| 5 | Hg14O20P4 | 0.2096 | 0.2038 |
| 5 | Hg8O20Te4 | 0.2427 | 0.2063 |

---

## 📊 测试总结

### 测试覆盖率

| 测试项 | 状态 | 备注 |
|--------|------|------|
| 命令行工具 | ✅ 通过 | 所有命令正常工作 |
| 环境检查 | ✅ 通过 | 所有依赖检测正确 |
| 配置加载 | ✅ 通过 | INPUT 文件解析正常 |
| 数据验证 | ✅ 通过 | 数据文件检查通过 |
| 工作流运行 | ✅ 通过 | 完整运行无错误 |
| 结果输出 | ✅ 通过 | 所有输出文件生成 |
| 模型训练 | ✅ 通过 | SISSO 模型训练成功 |
| 主动学习 | ✅ 通过 | 5 次迭代正常完成 |

### 性能指标

| 指标 | 数值 |
|------|------|
| 安装时间 | ~5-10 分钟 |
| 快速测试运行时间 | ~2 分钟 |
| 初始模型 R² | 0.7143 |
| 最终模型 R² | 0.7618 |
| 性能提升 | +6.65% |
| 计算材料数 | 15 个 |

---

## 🎯 使用说明

### 快速开始

```bash
# 1. 激活环境
export PATH="/home/user/1-yjy/deepmd-kit-20260323/envs/asap/bin:$PATH"
# 或使用 conda
# conda activate asap

# 2. 查看帮助
asap -h

# 3. 检查环境
asap -c

# 4. 运行工作流
asap -r

# 5. 使用指定配置
asap -r /path/to/INPUT
```

### 测试案例

```bash
# 进入测试目录
cd examples/test-workdir

# 运行测试
asap -r INPUT

# 查看结果
cat test_output/model_info.json
```

---

## 🐛 已知问题与解决方案

### 问题 1: 环境变量

**现象**: 直接运行 `asap` 命令提示找不到

**原因**: PATH 未包含 conda 环境 bin 目录

**解决**:
```bash
export PATH="/home/user/1-yjy/deepmd-kit-20260323/envs/asap/bin:$PATH"
```

或使用完整路径:
```bash
/home/user/1-yjy/deepmd-kit-20260323/envs/asap/bin/asap
```

### 问题 2: 配置文件路径

**现象**: 提示 INPUT 配置文件不存在

**原因**: 配置文件路径检测逻辑需要项目目录环境变量

**解决**: 已修复，使用 `ASAP_PROJECT` 环境变量或硬编码路径

---

## ✅ 结论

**ASAP v1.0.0 安装和测试全部通过！**

### 主要成就

1. ✅ 命令行工具设计简洁易用
2. ✅ 所有命令（-h, -v, -i, -c, -r）正常工作
3. ✅ 环境检查功能完善
4. ✅ 工作流运行稳定
5. ✅ 输出结果完整准确
6. ✅ 主动学习循环正常执行
7. ✅ 模型性能有显著提升

### 推荐配置

**快速测试**（验证安装）:
```
AL_N_ITERATIONS = 5
AL_BATCH_SIZE = 3
QUICK_TEST = True
```

**标准计算**（正式使用）:
```
AL_N_ITERATIONS = 30
AL_BATCH_SIZE = 5
QUICK_TEST = False
```

---

**报告生成时间**: 2026-03-28 13:15  
**测试状态**: ✅ 全部通过

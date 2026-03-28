# ASAP 测试指南

本文档指导如何测试 ASAP 的各个功能。

---

## 📋 测试环境

### 方式 1：使用 Conda 环境（推荐）

```bash
# 1. 安装 ASAP
./install/install.sh

# 2. 激活环境
conda activate asap

# 3. 测试命令
asap -h
asap -v
asap -c
asap -r
```

### 方式 2：直接测试（无需安装）

```bash
# 直接运行脚本
python3 scripts/bin/asap -h
python3 scripts/bin/asap -v
python3 scripts/bin/asap -c
python3 scripts/bin/asap -r
```

---

## 🧪 测试命令

### 1. 测试帮助信息

```bash
asap -h
```

**期望输出**:
```
usage: asap [-h] [-r [CONFIG]] [-c] [-i] [-v]

ASAP - Active Symbolic Accelerated Platform

options:
  -h, --help            显示帮助
  -r [CONFIG], --run    运行工作流
  -c, --check           检查环境
  -i, --info            显示信息
  -v, --version         显示版本
```

### 2. 测试版本信息

```bash
asap -v
```

**期望输出**:
```
ASAP v1.0.0
```

### 3. 测试环境检查

```bash
asap -c
```

**期望输出**:
```
======================================================================
  ASAP - Active Symbolic Accelerated Platform
======================================================================

检查环境和依赖...

[1/6] Python 版本：3.10.x
  ✓ Python 版本符合要求

[2/6] 检查 SISSO...
  ✓ SISSO 已安装

[3/6] 检查 MACE...
  ✓ MACE 已安装

...

✓ 所有检查通过！环境配置正确。
```

### 4. 测试运行工作流

```bash
# 使用默认配置
asap -r

# 使用指定配置
asap -r /path/to/INPUT

# 在测试目录
cd examples/test-workdir
asap -r INPUT
```

---

## 📁 测试工作目录

### 位置

```
examples/test-workdir/
├── INPUT           # 测试配置文件
└── README.md       # 使用说明
```

### 测试步骤

1. **进入测试目录**
   ```bash
   cd examples/test-workdir
   ```

2. **检查配置**
   ```bash
   cat INPUT
   ```

3. **运行测试**
   ```bash
   asap -r INPUT
   ```

4. **查看结果**
   ```bash
   ls test_output/
   cat test_output/model_info.json
   ```

---

## 🔧 常见问题

### 问题 1：命令未找到

**错误**: `bash: asap: command not found`

**原因**: Conda 环境未激活

**解决**:
```bash
conda activate asap
asap -h
```

### 问题 2：模块未找到

**错误**: `ModuleNotFoundError: No module named 'sissopp'`

**原因**: 依赖未安装

**解决**:
```bash
conda activate asap
# 如果还没安装，运行安装脚本
./install/install.sh
```

### 问题 3：配置文件不存在

**错误**: `FileNotFoundError: INPUT 配置文件不存在`

**原因**: 配置文件路径错误

**解决**:
```bash
# 使用完整路径
asap -r /full/path/to/INPUT

# 或确保在当前目录
cd /path/to/workdir
asap -r INPUT
```

---

## ✅ 测试清单

安装完成后，运行以下测试：

- [ ] `asap -h` - 显示帮助
- [ ] `asap -v` - 显示版本
- [ ] `asap -c` - 检查环境（所有依赖应显示 ✓）
- [ ] `asap -r` - 运行工作流（使用默认配置）
- [ ] `asap -r examples/test-workdir/INPUT` - 使用指定配置

---

## 📊 性能测试

### 快速测试（~5 分钟）

在 `INPUT` 文件中设置：
```
AL_N_ITERATIONS = 5
AL_BATCH_SIZE = 3
QUICK_TEST = True
```

### 标准测试（~1-2 小时）

```
AL_N_ITERATIONS = 30
AL_BATCH_SIZE = 5
QUICK_TEST = False
```

---

## 📝 测试报告

如果遇到问题，请提供以下信息：

1. **系统信息**
   ```bash
   uname -a
   python3 --version
   conda --version
   ```

2. **环境信息**
   ```bash
   asap -c
   ```

3. **错误信息**
   完整的错误输出

---

**更多帮助**: 查看 [../USAGE.md](../USAGE.md) 和 [INSTALL.md](INSTALL.md)

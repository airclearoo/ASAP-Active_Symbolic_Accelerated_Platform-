# ASAP 命令行工具说明

## 🎯 设计理念

**简洁易用** - 只需记住一个命令 `asap`，配合简单的参数即可。

---

## 📝 命令格式

```bash
asap [选项]
```

---

## 🔧 可用选项

| 选项 | 长格式 | 说明 | 示例 |
|------|--------|------|------|
| `-h` | `--help` | 显示帮助信息 | `asap -h` |
| `-v` | `--version` | 显示版本号 | `asap -v` |
| `-i` | `--info` | 显示软件信息 | `asap -i` |
| `-c` | `--check` | 检查环境和依赖 | `asap -c` |
| `-r` | `--run` | 运行工作流 | `asap -r` |

---

## 💡 常用命令

### 查看帮助

```bash
asap -h
```

### 检查环境

```bash
asap -c
```

输出示例：
```
======================================================================
  ASAP - Active Symbolic Accelerated Platform
======================================================================

检查环境和依赖...

[1/6] Python 版本：3.10.12
  ✓ Python 版本符合要求

[2/6] 检查 SISSO...
  ✓ SISSO 已安装

[3/6] 检查 MACE...
  ✓ MACE 已安装

...

✓ 所有检查通过！环境配置正确。
```

### 运行工作流

```bash
# 使用默认配置（scripts/config/INPUT）
asap -r

# 使用指定配置文件
asap -r /path/to/INPUT

# 在测试目录
cd examples/test-workdir
asap -r INPUT
```

### 查看版本

```bash
asap -v
```

输出：
```
ASAP v1.0.0
```

### 查看软件信息

```bash
asap -i
```

输出示例：
```
======================================================================
  ASAP - Active Symbolic Accelerated Platform
  主动符号加速平台
======================================================================

版本：1.0.0
作者：NewtonYe
论文：npj Computational Materials (2025)
DOI: 10.1038/s41524-025-01596-4

使用方法:
  asap -r              运行工作流
  asap -c              检查环境
  asap -i              显示信息
  asap -h              显示帮助

高级用法:
  asap -r /path/INPUT  使用指定配置文件运行
```

---

## 📁 工作流程

### 标准流程

```bash
# 1. 激活环境
conda activate asap

# 2. 准备工作目录
mkdir my-workdir
cd my-workdir

# 3. 复制配置文件
cp /path/to/asap/scripts/config/INPUT .

# 4. 编辑配置
nano INPUT

# 5. 运行
asap -r INPUT
```

### 快速测试

```bash
conda activate asap
cd examples/test-workdir
asap -r INPUT
```

---

## 🎓 参数说明

### -r / --run

运行工作流。

**用法**:
```bash
asap -r              # 使用默认配置
asap -r INPUT        # 使用指定配置
asap -r /path/INPUT  # 使用绝对路径
```

**功能**:
1. 加载配置文件（INPUT）
2. 验证数据文件
3. 运行 SISSO + MACE 工作流
4. 输出结果到指定目录

### -c / --check

检查环境和依赖。

**检查项**:
- Python 版本
- SISSO 安装
- MACE 安装
- ASE 安装
- 科学计算库（pandas, numpy, sklearn, matplotlib）
- 配置文件

### -i / --info

显示软件信息，包括：
- 版本号
- 作者信息
- 论文 DOI
- 使用方法

### -h / --help

显示帮助信息，列出所有可用选项和示例。

### -v / --version

显示版本号。

---

## 🐛 故障排除

### 命令未找到

```bash
bash: asap: command not found
```

**解决**:
```bash
# 确保已激活 conda 环境
conda activate asap

# 如果还没安装
./install/install.sh
```

### 权限错误

```bash
Permission denied
```

**解决**:
```bash
chmod +x scripts/bin/asap
```

### 配置错误

```bash
FileNotFoundError: INPUT 配置文件不存在
```

**解决**:
```bash
# 检查文件是否存在
ls -la INPUT

# 使用完整路径
asap -r /full/path/to/INPUT
```

---

## 📚 相关文档

- [START_HERE.md](../START_HERE.md) - 快速开始
- [USAGE.md](../USAGE.md) - 使用说明
- [INSTALL.md](INSTALL.md) - 安装指南
- [TEST_GUIDE.md](TEST_GUIDE.md) - 测试指南

---

<div align="center">

**ASAP v1.0.0** | Made with ❤️ by NewtonYe

</div>

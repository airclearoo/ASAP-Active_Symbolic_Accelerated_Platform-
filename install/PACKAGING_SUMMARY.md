# ASAP 软件包装总结

本文档总结了将工作流脚本包装为成熟软件所做的改进。

---

## 📦 包装概览

原始工作流脚本 `workflow_active_learning_mace_fixed.py` 已经可以正常运行。本次包装工作的目标是将其打造为一个**成熟的、可发布的软件**，便于在其他电脑上安装和使用。

---

## ✨ 新增功能

### 1. 配置系统

**新增文件**:
- `config/INPUT` - 用户配置文件
- `config/INPUT.example` - 配置示例
- `config/config_loader.py` - 配置加载器

**改进**:
- ✅ 所有配置参数从代码中分离到 INPUT 文件
- ✅ 支持注释和清晰的参数分组
- ✅ 类型自动转换（布尔值、整数、浮点数、列表）
- ✅ 路径支持相对路径和绝对路径

**用户只需编辑 INPUT 文件即可配置所有参数**，无需修改 Python 代码。

### 2. 命令行接口

**新增文件**:
- `asap.py` - 主入口脚本

**命令**:
```bash
python asap.py info     # 显示帮助信息
python asap.py check    # 检查环境和依赖
python asap.py run      # 运行工作流
python asap.py run <config>  # 使用自定义配置
```

### 3. 优化的安装脚本

**改进的 install.sh**:
- ✅ 更清晰的步骤提示
- ✅ 交互式环境选择（删除/保留/退出）
- ✅ 完整的依赖验证
- ✅ 更好的错误处理和颜色输出
- ✅ 环境名称从 `sisso-mace` 改为 `asap`（更简洁）

### 4. 完善的文档系统

**新增/更新的文档**:

| 文档 | 说明 | 状态 |
|------|------|------|
| `README.md` | 项目主文档 | ✅ 重写 |
| `INSTALL.md` | 安装指南 | ✅ 重写 |
| `USAGE.md` | 使用说明 | ✅ 重写 |
| `docs/QUICKSTART.md` | 快速入门 | ✅ 新增 |
| `MANIFEST.md` | 文件清单 | ✅ 新增 |
| `PACKAGING_SUMMARY.md` | 包装总结 | 本文件 |

### 5. 项目标准化

**新增文件**:
- `.gitignore` - Git 忽略配置
- `LICENSE` - MIT 许可证
- `CITATION.cff` - 引用配置（GitHub 标准）
- `pyproject.toml` - Python 项目配置
- `tests/test_config_loader.py` - 单元测试

---

## 📁 目录结构变化

### 新增目录

```
config/          # 配置目录
tests/           # 测试目录
```

### 新增文件

```
asap.py                          # 主入口
config/INPUT                     # 配置文件
config/INPUT.example             # 配置示例
config/config_loader.py          # 配置加载器
.gitignore                       # Git 忽略
LICENSE                          # 许可证
CITATION.cff                     # 引用配置
pyproject.toml                   # 项目配置
tests/test_config_loader.py      # 测试
PACKAGING_SUMMARY.md             # 包装总结
```

### 更新的文件

```
install.sh                       # 优化安装脚本
run.sh                           # 更新运行脚本
README.md                        # 重写项目说明
INSTALL.md                       # 重写安装指南
USAGE.md                         # 重写使用说明
docs/QUICKSTART.md               # 重写快速入门
MANIFEST.md                      # 更新文件清单
```

---

## 🚀 使用方法

### 在新电脑上安装

```bash
# 1. 克隆或下载项目
git clone https://github.com/NewtonYe/asap.git
cd asap

# 2. 运行安装脚本
./install.sh

# 3. 激活环境
conda activate asap

# 4. 配置参数
nano config/INPUT

# 5. 运行工作流
python asap.py run
```

### 配置工作目录

用户只需准备以下文件：

```
workdir/
├── config/
│   └── INPUT              # 复制并修改 config/INPUT.example
├── data/
│   ├── training.csv       # 训练数据
│   └── candidates.db      # 候选数据库
├── models/
│   └── mace.model         # MACE 模型
└── output/                # 输出目录（自动创建）
```

在 INPUT 文件中设置路径：

```
TRAIN_DATA = data/training.csv
CANDIDATE_DB = data/candidates.db
MACE_MODEL = models/mace.model
OUTPUT_DIR = output
```

然后运行：

```bash
python asap.py run
```

---

## 🎯 设计原则

### 1. 配置与代码分离

所有可调参数都在 `config/INPUT` 中，用户无需修改 Python 代码。

### 2. 约定优于配置

提供合理的默认值，用户只需修改必要的参数。

### 3. 渐进式复杂度

- **新手**: 使用默认配置，直接运行
- **进阶**: 调整 INPUT 文件中的参数
- **专家**: 修改 Python 代码

### 4. 自文档化

- INPUT 文件包含详细注释
- 每个参数都有说明和推荐值
- 提供配置预设（快速测试/标准/高精度）

### 5. 错误友好

- 清晰的错误信息
- 详细的验证步骤
- 常见问题解决方案

---

## 📊 配置参数映射

| INPUT 参数 | 原代码变量 | 说明 |
|-----------|-----------|------|
| `TRAIN_DATA` | `DATA_FILE` | 训练数据路径 |
| `CANDIDATE_DB` | `CANDIDATE_DB` | 候选数据库路径 |
| `OUTPUT_DIR` | `OUTPUT_DIR` | 输出目录 |
| `PROP_LABEL` | `SISSO_PARAMS['prop_label']` | 目标属性名 |
| `N_DIM` | `SISSO_PARAMS['n_dim']` | SISSO 维度 |
| `MAX_RUNG` | `SISSO_PARAMS['max_rung']` | 公式层级 |
| `AL_N_ITERATIONS` | `AL_N_ITERATIONS` | 迭代次数 |
| `AL_BATCH_SIZE` | `AL_BATCH_SIZE` | 批次大小 |
| `MACE_DEVICE` | `MACE_DEVICE` | 计算设备 |
| `MACE_RELAX` | `MACE_RELAX` | 结构弛豫 |

---

## 🔧 技术细节

### 配置加载流程

```
asap.py run
    ↓
load_config() → 读取 config/INPUT
    ↓
parse_value() → 类型转换
    ↓
覆盖 workflow_active_learning_mace_fixed.py 中的默认值
    ↓
workflow.main() → 运行工作流
```

### 配置覆盖机制

`asap.py` 在运行前会导入主工作流模块，然后覆盖其全局变量：

```python
import workflow_active_learning_mace_fixed as workflow

# 覆盖配置
workflow.DATA_FILE = config.get('TRAIN_DATA')
workflow.AL_N_ITERATIONS = get_int(config, 'AL_N_ITERATIONS')
# ...
```

这种方式无需修改原工作流脚本，保持了代码的向后兼容性。

---

## 📝 发布准备

### GitHub 发布清单

- [x] README.md - 项目说明
- [x] LICENSE - 许可证
- [x] CITATION.cff - 引用配置
- [x] .gitignore - Git 忽略
- [x] pyproject.toml - 项目配置
- [x] 完善的文档系统
- [x] 一键安装脚本
- [x] 配置驱动设计

### 后续步骤

1. **创建 GitHub 仓库**
   ```bash
   git init
   git add .
   git commit -m "Initial release of ASAP"
   git remote add origin https://github.com/NewtonYe/asap.git
   git push -u origin main
   ```

2. **创建 Zenodo DOI**
   - 访问 https://zenodo.org
   - 关联 GitHub 仓库
   - 获取 DOI 并更新 CITATION.cff

3. **发布到 PyPI**（可选）
   ```bash
   pip install build twine
   python -m build
   twine upload dist/*
   ```

4. **创建 Release**
   - GitHub Releases
   - 添加版本说明
   - 上传二进制包（可选）

---

## 🎓 与原始脚本的兼容性

### 向后兼容

- ✅ 原工作流脚本 `workflow_active_learning_mace_fixed.py` 保持不变
- ✅ 可以直接运行原脚本（使用默认配置）
- ✅ 新的 `asap.py` 只是包装层

### 配置兼容

- ✅ `config.example.py` 保留作为参考
- ✅ INPUT 文件格式更友好，支持注释

---

## 📈 改进总结

| 方面 | 改进前 | 改进后 |
|------|--------|--------|
| 配置方式 | 修改 Python 代码 | 编辑 INPUT 文件 |
| 安装方式 | 手动安装依赖 | 一键安装脚本 |
| 文档 | 基础说明 | 完整文档系统 |
| 命令行 | 无 | 4 个命令 |
| 项目结构 | 简单 | 标准化 |
| 可发布性 | 低 | 高（GitHub 就绪） |

---

## 🙏 致谢

本包装工作基于原始工作流脚本 `workflow_active_learning_mace_fixed.py`，该脚本已经实现了完整的 SISSO + MACE 主动学习工作流。

**论文**: Materials-discovery workflow guided by symbolic regression for identifying acid-stable oxides for electrocatalysis  
**期刊**: npj Computational Materials (2025)  
**DOI**: 10.1038/s41524-025-01596-4

---

<div align="center">

**包装完成时间**: 2026-03-28  
**版本**: 1.0.0  
**作者**: 小葉助手 🍃

</div>

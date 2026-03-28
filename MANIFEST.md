# ASAP 项目文件清单

本文档列出 ASAP 项目的所有文件和目录。

---

## 📁 目录结构

```
sisso_mace_al_workflow/
│
├── 📄 核心文件
│   └── START_HERE.md                        # 快速开始
│
├── 📁 数据目录
│   ├── data/                                # 候选数据库
│   ├── scripts/sisso/                       # 训练数据
│   └── mace_model/                          # MACE 模型
│
├── 📁 scripts/                              # Python 脚本（核心代码）
│   ├── bin/                                 # 可执行命令
│   │   └── asap                             # ASAP 命令行工具
│   ├── python/                              # Python 模块
│   │   ├── workflow_active_learning_mace_fixed.py  # 主工作流
│   │   └── test_installation.py             # 安装测试
│   ├── config/                              # 配置文件
│   │   ├── INPUT                            # 用户配置
│   │   ├── INPUT.example                    # 配置示例
│   │   └── config_loader.py                 # 配置加载器
│   └── tests/                               # 测试
│       └── test_config_loader.py
│
├── 📁 install/                              # 安装相关
│   ├── install.sh                           # 一键安装脚本
│   ├── run.sh                               # 运行脚本
│   ├── INSTALL.md                           # 详细安装指南
│   ├── PACKAGING_SUMMARY.md                 # 包装总结
│   └── RELEASE_NOTES.md                     # 发布说明
│
├── 📁 docs/                                 # 文档目录
│   └── QUICKSTART.md                        # 快速入门指南
│
├── 📁 examples/                             # 示例文件
│   ├── test-workdir/                        # 测试工作目录
│   │   ├── INPUT                            # 测试配置
│   │   └── README.md                        # 使用说明
│   ├── config.example.py                    # Python 配置示例
│   ├── PROJECT_SUMMARY.md                   # 项目总结
│   ├── 创建报告.md                          # 创建报告
│   └── 软件包说明.txt                       # 软件包说明
│
├── 📁 sissopp/                              # SISSO++ 源码
│   └── ...                                  # SISSO++ 源代码
│
├── 📚 文档
│   ├── README.md                            # 项目说明
│   ├── USAGE.md                             # 使用说明
│   ├── MANIFEST.md                          # 文件清单
│   ├── LICENSE                              # 许可证
│   └── CITATION.cff                         # 引用配置
│
└── ⚙️ 项目配置
    ├── pyproject.toml                       # Python 项目配置
    └── .gitignore                           # Git 忽略
```

---

## 🗂️ 目录说明

### 核心目录

| 目录 | 说明 |
|------|------|
| `scripts/` | Python 脚本和配置 |
| `data/` | 数据文件 |
| `scripts/sisso/` | 训练数据 |
| `mace_model/` | MACE 模型 |
| `sissopp/` | SISSO++ 源码 |
| `install/` | 安装脚本和指南 |
| `docs/` | 快速入门 |
| `examples/` | 示例文件 |
| `scripts/tests/` | 测试 |

### 核心文件

| 文件 | 说明 |
|------|------|
| `scripts/bin/asap` | 命令行工具（安装后直接用 `asap` 命令） |
| `scripts/python/workflow_active_learning_mace_fixed.py` | 主工作流 |
| `scripts/config/INPUT` | 用户配置文件 |

### 安装相关

| 文件 | 说明 |
|------|------|
| `install/install.sh` | 一键安装脚本 |
| `install/run.sh` | 运行脚本 |
| `install/INSTALL.md` | 详细安装指南 |

### 文档

| 文件 | 说明 |
|------|------|
| `START_HERE.md` | 30 秒快速开始 |
| `README.md` | 项目说明 |
| `USAGE.md` | 使用说明 |
| `docs/QUICKSTART.md` | 快速入门 |
| `MANIFEST.md` | 文件清单 |
| `LICENSE` | MIT 许可证 |
| `CITATION.cff` | 引用配置 |

### 项目配置

| 文件 | 说明 |
|------|------|
| `pyproject.toml` | Python 项目配置 |
| `.gitignore` | Git 忽略配置 |

---

## 🚀 使用方法

### 安装后

```bash
# 激活环境
conda activate asap

# 查看帮助
asap -h

# 检查环境
asap -c

# 运行工作流
asap -r

# 使用指定配置
asap -r /path/to/INPUT
```

### 在工作目录使用

```bash
# 1. 准备工作目录
mkdir my-workdir
cd my-workdir

# 2. 复制 INPUT 文件
cp /path/to/asap/scripts/config/INPUT .

# 3. 准备数据文件
# 将你的数据文件放在合适位置

# 4. 编辑 INPUT 文件
nano INPUT

# 5. 运行
asap -r INPUT
```

---

## 📦 生成文件（不提交到 Git）

以下文件由工作流生成，不应提交到版本控制：

- `asap_output/` - 输出目录
- `workflow_output*/` - 工作流输出
- `__pycache__/` - Python 缓存
- `*.pyc` - Python 字节码

---

<div align="center">

**版本**: 1.0.0  
**最后更新**: 2026-03-28

</div>

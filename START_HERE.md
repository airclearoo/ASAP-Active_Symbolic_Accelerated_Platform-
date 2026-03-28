# 🚀 快速开始

## 30 秒上手

### 1. 安装

```bash
cd sisso_mace_al_workflow
./install/install.sh
```

### 2. 配置

编辑 `config/INPUT` 文件，确认数据路径正确。

### 3. 运行

```bash
conda activate asap
asap -r
```

---

## 📁 目录说明

| 目录 | 说明 |
|------|------|
| `config/` | 配置文件（编辑 INPUT） |
| `install/` | 安装脚本 |
| `data/` | 数据文件 |
| `docs/` | 文档 |
| `examples/` | 示例 |

---

## 📚 文档

- **快速入门**: [docs/QUICKSTART.md](docs/QUICKSTART.md)
- **使用说明**: [USAGE.md](USAGE.md)
- **安装指南**: [install/INSTALL.md](install/INSTALL.md)
- **项目说明**: [README.md](README.md)

---

## 🔧 常用命令

### 工作流（主动学习）

```bash
asap -r              # 运行工作流
asap -r INPUT        # 使用指定配置
```

### 预测功能

```bash
asap -p              # SISSO 模型预测
asap -p CONFIG       # 使用指定配置
```

### 其他命令

```bash
asap -h              # 查看帮助
asap -c              # 检查环境
asap -v              # 显示版本
```

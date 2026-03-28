# 测试工作目录

这是一个测试用的工作目录示例。

## 📁 目录结构

```
test-workdir/
├── INPUT           # 配置文件（复制并修改）
└── README.md       # 本文件
```

## 🚀 使用方法

### 方式 1：在当前目录测试

```bash
cd examples/test-workdir
asap -r INPUT
```

### 方式 2：在其他目录使用

```bash
# 1. 复制 test-workdir 到你的工作目录
cp -r examples/test-workdir /path/to/your/workdir

# 2. 修改 INPUT 文件中的路径
nano /path/to/your/workdir/INPUT

# 3. 运行
cd /path/to/your/workdir
asap -r INPUT
```

## 📝 配置说明

在 INPUT 文件中修改以下参数：

### 必填参数

```
TRAIN_DATA = /path/to/your/data.csv
CANDIDATE_DB = /path/to/your/design.db
MACE_MODEL = /path/to/your/model.model
OUTPUT_DIR = output
```

### 可选参数

```
# 快速测试（5 分钟）
AL_N_ITERATIONS = 5
AL_BATCH_SIZE = 3
QUICK_TEST = True

# 标准计算（1-2 小时）
AL_N_ITERATIONS = 30
AL_BATCH_SIZE = 5
QUICK_TEST = False

# 高精度计算（需要 GPU）
AL_N_ITERATIONS = 50
AL_BATCH_SIZE = 10
MACE_RELAX = True
MACE_DEVICE = cuda
```

## 🔧 常用命令

```bash
# 查看帮助
asap -h

# 检查环境
asap -c

# 运行工作流
asap -r INPUT

# 使用默认配置
asap -r
```

## 📊 输出结果

运行完成后，OUTPUT_DIR 目录包含：

- `model_info.json` - 模型性能信息
- `active_learning_history.csv` - 主动学习历史
- `sisso_initial/` - 初始 SISSO 模型
- `sisso_final/` - 最终 SISSO 模型
- `sisso_al/` - 迭代模型

## 🐛 故障排除

### 问题：找不到 INPUT 文件

**解决**: 确保 INPUT 文件在当前目录，或使用完整路径：
```bash
asap -r /full/path/to/INPUT
```

### 问题：数据文件不存在

**解决**: 检查 INPUT 中的路径是否正确：
```bash
ls /path/to/your/data.csv
ls /path/to/your/design.db
ls /path/to/your/model.model
```

### 问题：命令未找到

**解决**: 确保已激活 conda 环境：
```bash
conda activate asap
asap -h
```

---

**更多帮助**: 查看 [../../USAGE.md](../../USAGE.md) 和 [../../install/INSTALL.md](../../install/INSTALL.md)

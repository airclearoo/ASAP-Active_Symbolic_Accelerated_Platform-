# ASAP 安装指南

本文档提供详细的安装说明，包括环境要求、依赖安装和验证步骤。

---

## 📋 目录

1. [系统要求](#系统要求)
2. [安装方法](#安装方法)
3. [验证安装](#验证安装)
4. [常见问题](#常见问题)
5. [卸载](#卸载)

---

## 🖥️ 系统要求

### 硬件要求

| 组件 | 最低要求 | 推荐配置 |
|------|----------|----------|
| **CPU** | 4 核 | 8 核以上 |
| **内存** | 16GB RAM | 32GB RAM |
| **存储** | 10GB | 20GB SSD |
| **GPU** | 可选 | NVIDIA GPU (CUDA 11+) |

### 软件要求

| 组件 | 版本 | 说明 |
|------|------|------|
| **操作系统** | Linux/macOS/WSL2 | Ubuntu 20.04+, macOS 12+, Windows WSL2 |
| **Python** | 3.9 - 3.11 | 推荐 3.10 |
| **包管理器** | Conda | Miniconda 或 Anaconda |

---

## 📦 安装方法

### 方法一：一键安装脚本（推荐）

这是最简单的方法，适合大多数用户。

```bash
# 进入项目目录
cd sisso_mace_al_workflow

# 运行安装脚本
./install.sh
```

安装过程：
1. 检测系统和 Conda
2. 创建 Conda 环境 `asap`
3. 安装所有依赖包
4. 验证安装
5. 检查数据文件

安装完成后会看到：
```
✓ 所有依赖安装成功!

使用方法:
  1. 激活环境：conda activate asap
  2. 配置参数：编辑 config/INPUT 文件
  3. 运行工作流：python asap.py run
```

### 方法二：手动安装

如果需要更多控制，可以手动安装。

#### 步骤 1: 创建 Conda 环境

```bash
conda create -n asap python=3.10 -y
```

#### 步骤 2: 激活环境

```bash
conda activate asap
```

#### 步骤 3: 安装 SISSO

```bash
conda install -c conda-forge sissopp -y
```

#### 步骤 4: 安装 MACE

```bash
conda install -c conda-forge mace-ml -y
```

#### 步骤 5: 安装 ASE

```bash
conda install -c conda-forge ase -y
```

#### 步骤 6: 安装科学计算库

```bash
conda install -c conda-forge pandas numpy scikit-learn matplotlib -y
```

#### 步骤 7: 验证安装

```bash
python asap.py check
```

### 方法三：从源码编译（高级）

仅当 conda-forge 版本不满足需求时使用。

#### 编译 SISSO++

```bash
# 安装编译依赖
sudo apt-get install -y cmake g++ libopenmpi-dev openmpi-bin libboost-all-dev

# 进入 sissopp 目录
cd sissopp

# 创建构建目录
mkdir build && cd build

# 配置
cmake .. \
    -DCMAKE_INSTALL_PREFIX=../install \
    -DSISSO_BUILD_PYTHON=ON \
    -DPython3_EXECUTABLE=$(which python)

# 编译
make -j$(nproc)

# 安装
make install
```

---

## ✅ 验证安装

### 快速验证

```bash
conda activate asap
python asap.py check
```

期望输出：
```
================================================================================
  ASAP - Active Symbolic Accelerated Platform
================================================================================

检查环境和依赖...

[1/7] Python 版本：3.10.x
  ✓ Python 版本符合要求

[2/7] 检查 SISSO...
  ✓ SISSO 已安装

[3/7] 检查 MACE...
  ✓ MACE 已安装

[4/7] 检查 ASE...
  ✓ ASE 已安装

[5/7] 检查科学计算库...
  ✓ pandas 已安装
  ✓ numpy 已安装
  ✓ sklearn 已安装
  ✓ matplotlib 已安装

[6/7] 检查配置文件...
  ✓ INPUT 配置文件存在

[7/7] 检查数据文件...
  ✓ TRAIN_DATA: scripts/sisso/nested_CV/data.csv
  ✓ CANDIDATE_DB: data/benchmark/design.db
  ✓ MACE_MODEL: mace_model/2023-12-03-mace-128-L1_epoch-199.model

================================================================================
✓ 所有检查通过！环境配置正确。
================================================================================
```

### 运行测试

```bash
# 使用快速测试配置运行
python asap.py run
```

---

## 🐛 常见问题

### 问题 1: Conda 未找到

**错误信息**: `Conda 未安装`

**解决**:

1. 下载 Miniconda:
   ```bash
   # Linux
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   bash Miniconda3-latest-Linux-x86_64.sh
   
   # macOS
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
   bash Miniconda3-latest-MacOSX-x86_64.sh
   ```

2. 初始化 Conda:
   ```bash
   source ~/.bashrc
   # 或
   source ~/.zshrc
   ```

3. 验证安装:
   ```bash
   conda --version
   ```

### 问题 2: sissopp 导入失败

**错误信息**: `ImportError: No module named 'sissopp'`

**解决**:

```bash
# 重新安装 sissopp
conda activate asap
conda uninstall sissopp -y
conda install -c conda-forge sissopp -y

# 验证
python -c "from sissopp.sklearn import SISSORegressor"
```

### 问题 3: MACE 模型加载失败

**错误信息**: `FileNotFoundError: MACE 模型文件不存在`

**解决**:

1. 检查模型文件路径:
   ```bash
   ls mace_model/*.model
   ```

2. 更新 `config/INPUT` 中的路径:
   ```
   MACE_MODEL = /path/to/your/mace/model.model
   ```

3. 如果模型文件不存在，需要下载或训练 MACE 模型。

### 问题 4: 内存不足

**错误信息**: `MemoryError` 或 `Killed`

**解决**:

1. 减少批次大小:
   ```
   AL_BATCH_SIZE = 3
   ```

2. 减少迭代次数:
   ```
   AL_N_ITERATIONS = 10
   ```

3. 减少随机森林树数量:
   ```
   RF_N_ESTIMATORS = 20
   ```

4. 增加系统 swap:
   ```bash
   sudo fallocate -l 8G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

### 问题 5: 编译失败（源码安装）

**错误信息**: 编译错误或链接错误

**解决**:

1. 安装完整开发环境:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install -y build-essential cmake libopenmpi-dev \
       openmpi-bin libboost-all-dev libeigen3-dev python3-dev
   
   # macOS
   brew install cmake boost open-mpi eigen
   ```

2. 清理并重新编译:
   ```bash
   cd sissopp
   rm -rf build
   mkdir build && cd build
   cmake .. -DCMAKE_INSTALL_PREFIX=../install -DSISSO_BUILD_PYTHON=ON
   make -j$(nproc)
   make install
   ```

### 问题 6: GPU 加速不可用

**错误信息**: MACE 无法使用 CUDA

**解决**:

1. 检查 NVIDIA 驱动:
   ```bash
   nvidia-smi
   ```

2. 检查 CUDA 版本:
   ```bash
   nvcc --version
   ```

3. 安装 CUDA 版本的 MACE:
   ```bash
   conda install -c conda-forge mace-ml-cuda -y
   ```

4. 更新配置:
   ```
   MACE_DEVICE = cuda
   ```

### 问题 7: 数据文件格式错误

**错误信息**: CSV 解析错误或特征列不匹配

**解决**:

1. 检查 CSV 文件格式:
   ```bash
   head -5 scripts/sisso/nested_CV/data.csv
   ```

2. 确保包含所有必需列:
   - `oxide`: 材料名称
   - `g_pbx (eV/atom)`: 目标值
   - 14 个特征列

3. 检查 `config/INPUT` 中的特征列名称是否与数据文件匹配。

---

## 🗑️ 卸载

### 删除 Conda 环境

```bash
conda env remove -n asap
```

### 删除项目文件

```bash
# 删除输出目录
rm -rf asap_output

# 删除整个项目（谨慎！）
cd ..
rm -rf sisso_mace_al_workflow
```

---

## 📚 依赖版本

推荐版本组合:

| 包名 | 版本 | 来源 |
|------|------|------|
| Python | 3.10 | python.org |
| sissopp | ≥1.2 | conda-forge |
| mace-ml | ≥0.3 | conda-forge |
| ase | ≥3.22 | conda-forge |
| pandas | ≥2.0 | conda-forge |
| numpy | ≥1.24 | conda-forge |
| scikit-learn | ≥1.3 | conda-forge |
| matplotlib | ≥3.7 | conda-forge |

---

## 🔗 相关资源

- **Miniconda 下载**: https://docs.conda.io/en/latest/miniconda.html
- **SISSO 文档**: https://github.com/CompRhysGroup/sisso++
- **MACE 文档**: https://github.com/ACEsuit/mace
- **ASE 文档**: https://wiki.fysik.dtu.dk/ase/

---

## 📞 获取帮助

如果遇到问题:

1. 查看本文档的常见问题部分
2. 启用调试模式：`DEBUG_MODE = True`
3. 查看详细日志输出
4. 查阅 [README.md](README.md) 和 [USAGE.md](USAGE.md)

---

<div align="center">

**安装完成后** → 查看 [快速入门](docs/QUICKSTART.md)

</div>

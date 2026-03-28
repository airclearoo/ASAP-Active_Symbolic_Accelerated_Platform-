#!/bin/bash
#===============================================================================
# ASAP - Active Symbolic Accelerated Platform
# 一键安装脚本
#===============================================================================
# 本脚本自动完成环境配置和依赖安装
# 支持：Linux, macOS, Windows (WSL2)
#===============================================================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 打印函数
info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

error() {
    echo -e "${RED}[✗]${NC} $1"
}

header() {
    echo -e "${CYAN}===============================================================================${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}===============================================================================${NC}"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

#===============================================================================
# 欢迎信息
#===============================================================================
header "ASAP - Active Symbolic Accelerated Platform 安装程序"
echo ""
info "本脚本将自动安装 ASAP 所需的所有依赖"
info "预计耗时：5-10 分钟（取决于网络速度）"
echo ""

#===============================================================================
# 系统检测
#===============================================================================
info "检测系统环境..."

OS_TYPE="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS_TYPE="linux"
    info "操作系统：Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS_TYPE="macos"
    info "操作系统：macOS"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    OS_TYPE="windows"
    info "操作系统：Windows (WSL/MinGW)"
else
    warn "未知操作系统：$OSTYPE"
fi

#===============================================================================
# 检查 Conda
#===============================================================================
echo ""
header "步骤 1/5: 检查 Conda"

if command_exists conda; then
    success "Conda 已安装"
    CONDA_PATH=$(which conda)
    info "Conda 路径：$CONDA_PATH"
    
    # 初始化 conda
    if ! conda info --base >/dev/null 2>&1; then
        warn "Conda 未正确初始化，尝试初始化..."
        source $(conda info --base)/etc/profile.d/conda.sh || true
    fi
else
    error "Conda 未安装"
    echo ""
    echo "请先安装 Miniconda 或 Anaconda:"
    echo ""
    echo "  Linux/macOS:"
    echo "    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
    echo "    bash Miniconda3-latest-Linux-x86_64.sh"
    echo ""
    echo "  Windows:"
    echo "    访问 https://docs.conda.io/en/latest/miniconda.html 下载安装"
    echo ""
    echo "安装完成后重新运行此脚本。"
    echo ""
    exit 1
fi

#===============================================================================
# 创建 Conda 环境
#===============================================================================
echo ""
header "步骤 2/5: 创建 Conda 环境"

ENV_NAME="asap"
PYTHON_VERSION="3.10"

info "环境名称：$ENV_NAME"
info "Python 版本：$PYTHON_VERSION"

if conda env list | grep -q "^$ENV_NAME "; then
    warn "环境 '$ENV_NAME' 已存在"
    echo ""
    echo "选项:"
    echo "  1) 删除并重新创建环境（推荐）"
    echo "  2) 使用现有环境"
    echo "  3) 退出"
    echo ""
    read -p "请选择 [1-3]: " choice
    
    case $choice in
        1)
            info "删除旧环境..."
            conda env remove -n $ENV_NAME -y
            info "创建新环境..."
            conda create -n $ENV_NAME python=$PYTHON_VERSION -y
            success "环境创建完成"
            ;;
        2)
            info "使用现有环境"
            ;;
        3)
            info "退出安装"
            exit 0
            ;;
        *)
            error "无效选择"
            exit 1
            ;;
    esac
else
    info "正在创建环境，这可能需要几分钟..."
    conda create -n $ENV_NAME python=$PYTHON_VERSION -y
    success "环境创建完成"
fi

#===============================================================================
# 激活环境
#===============================================================================
echo ""
header "步骤 3/5: 激活环境"

info "激活环境：$ENV_NAME"
source $(conda info --base)/etc/profile.d/conda.sh
conda activate $ENV_NAME
success "环境已激活"

#===============================================================================
# 步骤 4/5: 检查并按需安装依赖（带版本锁定）
#===============================================================================
echo ""
header "步骤 4/5: 检查并安装依赖包 (锁定版本)"

# 内部函数：检查 Python 包及其版本
# 参数: $1=包名, $2=最小版本要求
check_version() {
    python -c "import $1; from packaging import version; \
    curr_v = getattr($1, '__version__', '0.0.0'); \
    exit(0 if version.parse(curr_v) >= version.parse('$2') else 1)" >/dev/null 2>&1
}

# 预检：确保安装了 packaging 库用于版本比对（conda 环境通常自带，若无则装）
if ! python -c "import packaging" >/dev/null 2>&1; then
    pip install packaging >/dev/null 2>&1
fi

# 1. 基础科学计算库 (Conda 安装)
# 根据你的记录：numpy>=1.25.1, pandas>=2.1.1, scikit-learn>=1.3.0
info "[1/5] 检查科学计算基础..."
if check_version "numpy" "1.25.1" && check_version "pandas" "2.1.1" && check_version "sklearn" "1.3.0"; then
    success "基础库 (NumPy/Pandas/Sklearn) 版本达标，跳过"
else
    info "正在安装/更新基础库..."
    conda install -c conda-forge numpy>=1.25.1 pandas>=2.1.1 scikit-learn>=1.3.0 scipy>=1.11.1 matplotlib>=3.7.1 -y
fi

# 2. 安装 SISSO (sissopp)
info "[2/5] 检查 SISSO..."
if python -c "import sissopp" >/dev/null 2>&1; then
    success "SISSO 已安装，跳过"
else
    info "正在从 conda-forge 安装 SISSO..."
    conda install -c conda-forge sissopp -y
fi

# 3. 安装 ASE (锁定 3.22.1)
info "[3/5] 检查 ASE..."
if check_version "ase" "3.22.1"; then
    success "ASE 3.22.1 已就绪，跳过"
else
    info "正在通过 pip 安装 ase==3.22.1..."
    pip install ase==3.22.1
fi

# 4. 安装材料学工具库 (Pymatgen & Matminer)
# 根据你的记录：pymatgen==2023.7.11, matminer>=0.8.0
info "[4/5] 检查 Pymatgen & Matminer..."
if check_version "pymatgen" "2023.7.11" && check_version "matminer" "0.8.0"; then
    success "材料学工具库版本达标，跳过"
else
    info "正在通过 pip 安装材料学工具..."
    pip install pymatgen==2023.7.11 matminer>=0.8.0
fi

# 5. 安装工作流及深度学习 (MACE & Taskblaster)
info "[5/5] 检查 MACE & Taskblaster..."

if python -c "import mace" >/dev/null 2>&1 && python -c "import taskblaster" >/dev/null 2>&1; then
    success "MACE 与 Taskblaster 已就绪，跳过"
else
    echo ""
    warn "检测到需要安装深度学习环境 (PyTorch/MACE)"
    echo "请选择安装版本:"
    echo "  1) CPU 版本 (体积小，适合个人电脑或无显卡服务器)"
    echo "  2) GPU 版本 (支持 CUDA 11.8，适合深度学习服务器)"
    echo "  3) 跳过 (手动安装)"
    echo ""
    read -p "请选择 [1-3]: " torch_choice

    case $torch_choice in
        1)
            info "正在安装 PyTorch (CPU 版)..."
            pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
            ;;
        2)
            info "正在安装 PyTorch (CUDA 11.8 版)..."
            pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
            ;;
        3)
            info "跳过安装，请确保稍后手动配置 torch"
            ;;
        *)
            error "无效选择，默认尝试标准安装"
            pip install torch torchvision torchaudio
            ;;
    esac

    info "正在安装 MACE 及工作流工具..."
    pip install mace-torch taskblaster
fi
echo ""
success "依赖环境校验及安装全部完成！"

echo ""

#===============================================================================
# 验证安装
#===============================================================================
echo ""
header "步骤 5/5: 验证安装"

VERIFY_SUCCESS=true

# 验证 SISSO
info "验证 SISSO..."
if python -c "from sissopp.sklearn import SISSORegressor" 2>/dev/null; then
    success "SISSO 验证通过"
else
    error "SISSO 验证失败"
    VERIFY_SUCCESS=false
fi

# 验证 MACE
info "验证 MACE..."
if python -c "import mace" 2>/dev/null; then
    success "MACE 验证通过"
else
    error "MACE 验证失败"
    VERIFY_SUCCESS=false
fi

# 验证 ASE
info "验证 ASE..."
if python -c "from ase.db import connect" 2>/dev/null; then
    success "ASE 验证通过"
else
    error "ASE 验证失败"
    VERIFY_SUCCESS=false
fi

# 验证其他库
info "验证科学计算库..."
if python -c "import pandas, numpy, sklearn, matplotlib" 2>/dev/null; then
    success "科学计算库验证通过"
else
    error "科学计算库验证失败"
    VERIFY_SUCCESS=false
fi

echo ""

#===============================================================================
# 检查数据文件
#===============================================================================
info "检查数据文件..."

DATA_FILES_OK=true

if [ -f "data/benchmark/design.db" ]; then
    success "候选数据库：data/benchmark/design.db"
else
    warn "缺少文件：data/benchmark/design.db"
    DATA_FILES_OK=false
fi

if [ -f "scripts/sisso/nested_CV/data.csv" ]; then
    success "训练数据：scripts/sisso/nested_CV/data.csv"
else
    warn "缺少文件：scripts/sisso/nested_CV/data.csv"
    DATA_FILES_OK=false
fi

if [ -f "mace_model/2023-12-03-mace-128-L1_epoch-199.model" ]; then
    success "MACE 模型：mace_model/2023-12-03-mace-128-L1_epoch-199.model"
else
    warn "缺少文件：mace_model/2023-12-03-mace-128-L1_epoch-199.model"
    DATA_FILES_OK=false
fi

echo ""

#===============================================================================
# 安装 ASAP 命令
#===============================================================================
echo ""
header "安装 ASAP 命令"

info "配置 ASAP 命令行工具..."

# 获取 conda 基础路径
CONDA_BASE=$(conda info --base)
ASAP_BIN="$CONDA_BASE/envs/$ENV_NAME/bin/asap"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASAP_SCRIPT="$SCRIPT_DIR/../scripts/bin/asap"

# 复制 asap 脚本到 conda 环境
if [ -f "$ASAP_SCRIPT" ]; then
    cp "$ASAP_SCRIPT" "$ASAP_BIN"
    chmod +x "$ASAP_BIN"
    success "ASAP 命令已安装到：$ASAP_BIN"
else
    # 尝试从上级目录查找
    ASAP_SCRIPT_ALT="../scripts/bin/asap"
    if [ -f "$ASAP_SCRIPT_ALT" ]; then
        cp "$ASAP_SCRIPT_ALT" "$ASAP_BIN"
        chmod +x "$ASAP_BIN"
        success "ASAP 命令已安装到：$ASAP_BIN"
    else
        warn "无法找到 asap 脚本，请手动配置"
    fi
fi

echo ""

#===============================================================================
# 完成
#===============================================================================
header "安装完成!"

if [ "$VERIFY_SUCCESS" = true ]; then
    success "所有依赖安装成功!"
    echo ""
    info "使用方法:"
    echo ""
    echo "  1. 激活环境:"
    echo "     conda activate asap"
    echo ""
    echo "  2. 配置参数:"
    echo "     编辑 config/INPUT 文件"
    echo ""
    echo "  3. 运行工作流:"
    echo "     asap -r"
    echo ""
    echo "  4. 检查环境:"
    echo "     asap -c"
    echo ""
    echo "  5. 查看帮助:"
    echo "     asap -h"
    echo ""
else
    warn "安装完成，但部分验证失败"
    echo ""
    echo "请检查上方的错误信息。"
    echo "常见问题解决方案请查看 INSTALL.md"
    echo ""
fi

info "文档:"
echo "  - README.md          - 项目说明"
echo "  - install/INSTALL.md - 详细安装指南"
echo "  - USAGE.md           - 使用说明"
echo "  - docs/QUICKSTART.md - 快速入门"
echo ""

echo "==============================================================================="
success "感谢使用 ASAP!"
echo "==============================================================================="

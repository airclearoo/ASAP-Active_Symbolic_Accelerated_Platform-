#!/bin/bash
#===============================================================================
# ASAP - Active Symbolic Accelerated Platform
# 运行脚本
#===============================================================================

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

header() {
    echo -e "${CYAN}===============================================================================${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}===============================================================================${NC}"
}

header "ASAP - Active Symbolic Accelerated Platform"
echo ""

# 检查 conda
if ! command -v conda >/dev/null 2>&1; then
    echo -e "${YELLOW}警告：Conda 未找到，尝试直接运行...${NC}"
    echo ""
    python asap.py run "$@"
    exit $?
fi

# 检查环境
ENV_NAME="asap"

if conda env list | grep -q "^$ENV_NAME "; then
    echo -e "${GREEN}✓${NC} 找到环境：$ENV_NAME"
    echo ""
    echo -e "${BLUE}正在激活环境并运行工作流...${NC}"
    echo ""
    
    # 激活环境并运行
    source $(conda info --base)/etc/profile.d/conda.sh
    conda activate $ENV_NAME
    asap -r "$@"
else
    echo -e "${YELLOW}⚠${NC} 环境 '$ENV_NAME' 不存在"
    echo ""
    echo "请先运行安装脚本："
    echo "  ./install/install.sh"
    echo ""
    exit 1
fi

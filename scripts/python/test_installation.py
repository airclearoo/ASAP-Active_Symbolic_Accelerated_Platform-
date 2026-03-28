#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
安装验证脚本
检查所有依赖是否正确安装
"""

import sys
import os

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_check(name, status, details=""):
    status_symbol = "✓" if status else "✗"
    status_color = "\033[92m" if status else "\033[91m"
    reset = "\033[0m"
    
    print(f"{status_color}{status_symbol}{reset} {name}", end="")
    if details:
        print(f": {details}")
    else:
        print()
    
    return status

def main():
    print_header("SISSO + MACE 工作流 - 安装验证")
    
    all_ok = True
    
    # 1. Python 版本
    print_header("1. Python 环境")
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    all_ok &= print_check(f"Python 版本", sys.version_info >= (3, 9), python_version)
    
    # 2. 核心依赖
    print_header("2. 核心依赖")
    
    # SISSO
    try:
        import sissopp
        from sissopp.sklearn import SISSORegressor
        all_ok &= print_check("SISSO (sissopp)", True, f"v{sissopp.__version__ if hasattr(sissopp, '__version__') else 'unknown'}")
    except ImportError as e:
        all_ok &= print_check("SISSO (sissopp)", False, str(e))
    
    # MACE
    try:
        import mace
        all_ok &= print_check("MACE (mace-ml)", True)
    except ImportError as e:
        all_ok &= print_check("MACE (mace-ml)", False, str(e))
    
    # ASE
    try:
        import ase
        from ase.db import connect
        all_ok &= print_check("ASE", True, f"v{ase.__version__}")
    except ImportError as e:
        all_ok &= print_check("ASE", False, str(e))
    
    # 3. 科学计算库
    print_header("3. 科学计算库")
    
    try:
        import pandas as pd
        all_ok &= print_check("pandas", True, f"v{pd.__version__}")
    except ImportError as e:
        all_ok &= print_check("pandas", False, str(e))
    
    try:
        import numpy as np
        all_ok &= print_check("numpy", True, f"v{np.__version__}")
    except ImportError as e:
        all_ok &= print_check("numpy", False, str(e))
    
    try:
        import sklearn
        all_ok &= print_check("scikit-learn", True, f"v{sklearn.__version__}")
    except ImportError as e:
        all_ok &= print_check("scikit-learn", False, str(e))
    
    try:
        import matplotlib
        all_ok &= print_check("matplotlib", True, f"v{matplotlib.__version__}")
    except ImportError as e:
        all_ok &= print_check("matplotlib", False, str(e))
    
    # 4. 数据文件
    print_header("4. 数据文件")
    
    data_file = 'scripts/sisso/nested_CV/data.csv'
    all_ok &= print_check(f"训练数据：{data_file}", os.path.exists(data_file))
    
    db_file = 'data/benchmark/design.db'
    all_ok &= print_check(f"候选数据库：{db_file}", os.path.exists(db_file))
    
    model_file = 'mace_model/2023-12-03-mace-128-L1_epoch-199.model'
    all_ok &= print_check(f"MACE 模型：{model_file}", os.path.exists(model_file))
    
    # 5. 功能测试
    print_header("5. 功能测试")
    
    # 测试 SISSO 导入
    try:
        from sissopp.sklearn import SISSORegressor
        sisso = SISSORegressor(
            prop_label='test',
            allowed_ops=["add", "sub", "mult", "div"],
            n_dim=1,
            max_rung=0
        )
        all_ok &= print_check("SISSO 初始化", True)
    except Exception as e:
        all_ok &= print_check("SISSO 初始化", False, str(e))
    
    # 测试数据加载
    try:
        if os.path.exists(data_file):
            df = pd.read_csv(data_file)
            all_ok &= print_check(f"数据加载测试", True, f"{len(df)} 行，{len(df.columns)} 列")
        else:
            all_ok &= print_check("数据加载测试", False, "文件不存在")
    except Exception as e:
        all_ok &= print_check("数据加载测试", False, str(e))
    
    # 总结
    print_header("验证结果")
    
    if all_ok:
        print("\n\033[92m✓ 所有检查通过！系统已准备就绪。\033[0m\n")
        print("下一步:")
        print("  python workflow_active_learning_mace_fixed.py")
        print()
        return 0
    else:
        print("\n\033[91m✗ 部分检查未通过，请查看上面的错误信息。\033[0m\n")
        print("参考文档:")
        print("  - INSTALL.md - 安装指南")
        print("  - USAGE.md   - 使用说明")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())

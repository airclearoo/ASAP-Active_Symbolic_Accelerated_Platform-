#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
================================================================================
ASAP - Active Symbolic Accelerated Platform
主动符号加速平台

基于 SISSO + MACE 的主动学习材料发现工作流

论文：Materials-discovery workflow guided by symbolic regression for 
      identifying acid-stable oxides for electrocatalysis
期刊：npj Computational Materials (2025)
DOI: 10.1038/s41524-025-01596-4

================================================================================
使用方法:
    asap run              # 运行工作流（从当前目录加载 config/INPUT）
    asap run <config>     # 运行工作流（指定 INPUT 文件路径）
    asap check            # 检查环境和依赖
    asap info             # 显示软件信息

================================================================================
"""

import sys
import os
from pathlib import Path

# 添加配置目录到路径
SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR / 'config'
sys.path.insert(0, str(CONFIG_DIR))

from config_loader import load_config, get_bool, get_int, get_float, get_str, get_list


def print_banner():
    """打印软件横幅"""
    print("=" * 80)
    print("  ASAP - Active Symbolic Accelerated Platform")
    print("  主动符号加速平台")
    print("=" * 80)
    print()


def print_info():
    """显示软件信息"""
    print_banner()
    print("版本：1.0.0")
    print("作者：NewtonYe")
    print("论文：npj Computational Materials (2025)")
    print("DOI: 10.1038/s41524-025-01596-4")
    print()
    print("使用方法:")
    print("  asap run              # 运行工作流")
    print("  asap run <config>     # 指定 INPUT 文件")
    print("  asap check            # 检查环境")
    print("  asap info             # 显示此信息")
    print()


def check_environment():
    """检查环境和依赖"""
    print_banner()
    print("检查环境和依赖...")
    print()
    
    all_ok = True
    
    # 检查 Python 版本
    import sys
    print(f"[1/7] Python 版本：{sys.version}")
    if sys.version_info < (3, 9):
        print("  ⚠ 警告：Python 版本过低，建议 3.9+")
    else:
        print("  ✓ Python 版本符合要求")
    print()
    
    # 检查 SISSO
    print("[2/7] 检查 SISSO...")
    try:
        import sissopp
        from sissopp.sklearn import SISSORegressor
        print(f"  ✓ SISSO 已安装 (v{sissopp.__version__ if hasattr(sissopp, '__version__') else 'unknown'})")
    except ImportError as e:
        print(f"  ✗ SISSO 未安装：{e}")
        all_ok = False
    print()
    
    # 检查 MACE
    print("[3/7] 检查 MACE...")
    try:
        import mace
        print(f"  ✓ MACE 已安装")
    except ImportError as e:
        print(f"  ✗ MACE 未安装：{e}")
        all_ok = False
    print()
    
    # 检查 ASE
    print("[4/7] 检查 ASE...")
    try:
        import ase
        from ase.db import connect
        print(f"  ✓ ASE 已安装 (v{ase.__version__})")
    except ImportError as e:
        print(f"  ✗ ASE 未安装：{e}")
        all_ok = False
    print()
    
    # 检查科学计算库
    print("[5/7] 检查科学计算库...")
    required = ['pandas', 'numpy', 'sklearn', 'matplotlib']
    for pkg in required:
        try:
            __import__(pkg)
            print(f"  ✓ {pkg} 已安装")
        except ImportError:
            print(f"  ✗ {pkg} 未安装")
            all_ok = False
    print()
    
    # 检查配置文件
    print("[6/7] 检查配置文件...")
    input_path = CONFIG_DIR / 'INPUT'
    if input_path.exists():
        print(f"  ✓ INPUT 配置文件存在")
    else:
        print(f"  ✗ INPUT 配置文件不存在：{input_path}")
        all_ok = False
    print()
    
    # 检查数据文件（从配置读取）
    print("[7/7] 检查数据文件...")
    try:
        config = load_config()
        data_files = [
            ('TRAIN_DATA', config.get('TRAIN_DATA', '')),
            ('CANDIDATE_DB', config.get('CANDIDATE_DB', '')),
            ('MACE_MODEL', config.get('MACE_MODEL', '')),
        ]
        for name, path in data_files:
            if path:
                if os.path.exists(path):
                    print(f"  ✓ {name}: {path}")
                else:
                    print(f"  ⚠ {name} 未找到：{path}")
    except Exception as e:
        print(f"  ✗ 无法加载配置：{e}")
        all_ok = False
    print()
    
    print("=" * 80)
    if all_ok:
        print("✓ 所有检查通过！环境配置正确。")
    else:
        print("⚠ 部分检查未通过，请查看上方错误信息。")
    print("=" * 80)
    
    return all_ok


def run_workflow(config_path=None):
    """运行工作流"""
    print_banner()
    
    # 加载配置
    if config_path:
        config_dir = Path(config_path).parent
        config_file = Path(config_path).name
        print(f"使用配置文件：{config_path}")
    else:
        config_dir = CONFIG_DIR
        config_file = 'INPUT'
        print(f"使用默认配置：{CONFIG_DIR / 'INPUT'}")
    print()
    
    try:
        config = load_config(config_dir)
    except FileNotFoundError as e:
        print(f"✗ 错误：{e}")
        return False
    except Exception as e:
        print(f"✗ 配置解析错误：{e}")
        return False
    
    print("配置参数:")
    print(f"  训练数据：{config.get('TRAIN_DATA', 'N/A')}")
    print(f"  候选数据库：{config.get('CANDIDATE_DB', 'N/A')}")
    print(f"  MACE 模型：{config.get('MACE_MODEL', 'N/A')}")
    print(f"  输出目录：{config.get('OUTPUT_DIR', 'N/A')}")
    print(f"  迭代次数：{config.get('AL_N_ITERATIONS', 'N/A')}")
    print(f"  批次大小：{config.get('AL_BATCH_SIZE', 'N/A')}")
    print(f"  MACE 弛豫：{config.get('MACE_RELAX', 'N/A')}")
    print()
    
    # 验证必要文件
    print("验证数据文件...")
    required_files = ['TRAIN_DATA', 'CANDIDATE_DB', 'MACE_MODEL']
    missing = []
    for key in required_files:
        path = config.get(key)
        if path and not os.path.exists(path):
            missing.append(f"{key}: {path}")
    
    if missing:
        print("✗ 以下文件缺失:")
        for m in missing:
            print(f"    {m}")
        print()
        print("请检查 INPUT 配置文件中的路径设置。")
        return False
    
    print("✓ 所有数据文件存在")
    print()
    
    # 导入并运行主工作流
    print("=" * 80)
    print("开始运行工作流...")
    print("=" * 80)
    print()
    
    # 设置配置参数为全局变量（供主工作流使用）
    import workflow_active_learning_mace_fixed as workflow
    
    # 覆盖默认配置
    workflow.DATA_FILE = config.get('TRAIN_DATA', workflow.DATA_FILE)
    workflow.CANDIDATE_DB = config.get('CANDIDATE_DB', workflow.CANDIDATE_DB)
    workflow.OUTPUT_DIR = config.get('OUTPUT_DIR', workflow.OUTPUT_DIR)
    
    # SISSO 参数
    workflow.SISSO_PARAMS['prop_label'] = config.get('PROP_LABEL', workflow.SISSO_PARAMS['prop_label'])
    workflow.SISSO_PARAMS['prop_unit'] = config.get('PROP_UNIT', workflow.SISSO_PARAMS['prop_unit'])
    workflow.SISSO_PARAMS['allowed_ops'] = get_list(config, 'ALLOWED_OPS', workflow.SISSO_PARAMS['allowed_ops'])
    workflow.SISSO_PARAMS['n_dim'] = get_int(config, 'N_DIM', workflow.SISSO_PARAMS['n_dim'])
    workflow.SISSO_PARAMS['max_rung'] = get_int(config, 'MAX_RUNG', workflow.SISSO_PARAMS['max_rung'])
    workflow.SISSO_PARAMS['n_sis_select'] = get_int(config, 'N_SIS_SELECT', workflow.SISSO_PARAMS['n_sis_select'])
    workflow.SISSO_PARAMS['n_residual'] = get_int(config, 'N_RESIDUAL', workflow.SISSO_PARAMS['n_residual'])
    workflow.SISSO_PARAMS['l_bound'] = get_float(config, 'L_BOUND', workflow.SISSO_PARAMS['l_bound'])
    workflow.SISSO_PARAMS['u_bound'] = get_float(config, 'U_BOUND', workflow.SISSO_PARAMS['u_bound'])
    
    # 主动学习参数
    workflow.AL_N_ITERATIONS = get_int(config, 'AL_N_ITERATIONS', workflow.AL_N_ITERATIONS)
    workflow.AL_BATCH_SIZE = get_int(config, 'AL_BATCH_SIZE', workflow.AL_BATCH_SIZE)
    workflow.AL_UCB_KAPPA = get_float(config, 'AL_UCB_KAPPA', workflow.AL_UCB_KAPPA)
    workflow.TEST_SIZE = get_float(config, 'TEST_SIZE', workflow.TEST_SIZE)
    workflow.RANDOM_STATE = get_int(config, 'RANDOM_STATE', workflow.RANDOM_STATE)
    
    # MACE 参数
    workflow.MACE_MODEL = config.get('MACE_MODEL', workflow.MACE_MODEL)
    workflow.MACE_DEVICE = config.get('MACE_DEVICE', workflow.MACE_DEVICE)
    workflow.MACE_RELAX = get_bool(config, 'MACE_RELAX', workflow.MACE_RELAX)
    workflow.MACE_RELAX_FMAX = get_float(config, 'MACE_RELAX_FMAX', workflow.MACE_RELAX_FMAX)
    workflow.MACE_RELAX_STEPS = get_int(config, 'MACE_RELAX_STEPS', workflow.MACE_RELAX_STEPS)
    
    # 运行工作流
    try:
        workflow.main()
        return True
    except Exception as e:
        print()
        print("=" * 80)
        print(f"✗ 工作流运行失败：{e}")
        print("=" * 80)
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print_info()
        return
    
    command = sys.argv[1]
    
    if command == 'info':
        print_info()
    
    elif command == 'check':
        success = check_environment()
        sys.exit(0 if success else 1)
    
    elif command == 'run':
        config_path = sys.argv[2] if len(sys.argv) > 2 else None
        success = run_workflow(config_path)
        sys.exit(0 if success else 1)
    
    else:
        print(f"未知命令：{command}")
        print()
        print_info()
        sys.exit(1)


if __name__ == '__main__':
    main()

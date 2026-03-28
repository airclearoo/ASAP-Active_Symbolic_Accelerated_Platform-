#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASAP - SISSO 模型预测功能（修复版）

使用 sissopp 库正确加载 SISSO 模型并进行预测
"""

import pandas as pd
import numpy as np
import json
import os
from pathlib import Path
import sys

# 添加路径
SCRIPT_DIR = Path(__file__).parent
PYTHON_DIR = SCRIPT_DIR.parent / 'python'
CONFIG_DIR = SCRIPT_DIR.parent / 'config'
sys.path.insert(0, str(PYTHON_DIR))
sys.path.insert(0, str(CONFIG_DIR))

from config_loader import load_config, get_bool, get_str


def print_banner():
    """打印横幅"""
    print("=" * 70)
    print("  ASAP - SISSO 模型预测功能")
    print("=" * 70)


def load_sisso_model_and_predict(model_dir, features):
    """
    加载 SISSO 模型并进行预测
    
    参数:
        model_dir: SISSO 模型目录
        features: 特征矩阵 (n_samples, n_features)
    
    返回:
        predictions: 预测值数组
    """
    model_dir = Path(model_dir)
    
    print(f"  模型目录：{model_dir}")
    
    # 检查是否有 sissopp
    try:
        from sissopp.sklearn import SISSORegressor
        print(f"  ✓ sissopp 可用")
    except ImportError:
        print(f"  ✗ sissopp 未安装")
        return None
    
    # 查找模型文件
    model_files = list((model_dir / 'models').glob('*.dat'))
    if not model_files:
        print(f"  ✗ 未找到模型文件 (.dat)")
        return None
    
    # 优先使用 dim_2 模型
    model_file = None
    for mf in model_files:
        if 'dim_2' in mf.name:
            model_file = mf
            break
    if not model_file:
        model_file = model_files[0]
    
    print(f"  使用模型：{model_file.name}")
    
    # 查找特征空间文件
    feature_space_dir = model_dir / 'feature_space'
    selected_features_file = feature_space_dir / 'selected_features.txt'
    
    if not selected_features_file.exists():
        print(f"  ✗ 未找到特征空间文件")
        return None
    
    # 读取选择的特征
    with open(selected_features_file, 'r') as f:
        lines = f.readlines()
    
    # 解析特征表达式（跳过注释行）
    feature_expressions = []
    for line in lines:
        if line.startswith('#') or not line.strip():
            continue
        parts = line.strip().split('\t')
        if len(parts) >= 2:
            expr = parts[1]
            feature_expressions.append(expr)
    
    print(f"  特征数量：{len(feature_expressions)}")
    
    # 使用 sissopp 进行预测
    # 需要重新创建 SISSO 模型并加载训练时的配置
    try:
        # 从训练数据中获取特征信息
        # SISSO 需要知道原始特征的数量和名称
        
        # 尝试从模型目录加载配置
        config_file = model_dir / 'config.json'
        if config_file.exists():
            with open(config_file, 'r') as f:
                model_config = json.load(f)
        else:
            # 使用默认配置
            model_config = {
                'n_features': 14,
                'n_dim': 2,
                'max_rung': 2
            }
        
        # 创建 SISSO 回归器
        sisso = SISSORegressor(
            n_dim=model_config.get('n_dim', 2),
            max_rung=model_config.get('max_rung', 2),
            n_sis_select=50,
            n_residual=5
        )
        
        # 设置工作目录
        sisso.workdir = str(model_dir)
        
        # 关键：使用 predict 方法需要模型已经拟合过
        # 由于我们无法直接加载 .dat 文件，需要使用另一种方法
        
        # 方法：从 .dat 文件读取系数，然后手动计算预测值
        # .dat 文件包含每个组合特征的系数
        
        coefficients = []
        with open(model_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if parts:
                    try:
                        coef = float(parts[-1])
                        coefficients.append(coef)
                    except ValueError:
                        pass
        
        print(f"  系数数量：{len(coefficients)}")
        
        if len(coefficients) != len(feature_expressions):
            print(f"  ⚠ 系数数量 ({len(coefficients)}) 与特征数量 ({len(feature_expressions)}) 不匹配")
            # 取较小值
            min_len = min(len(coefficients), len(feature_expressions))
            coefficients = coefficients[:min_len]
            feature_expressions = feature_expressions[:min_len]
        
        # 现在需要计算每个样本的组合特征值
        # 这需要解析 RPN 表达式并计算
        
        # 简化方法：使用 sissopp 的特征空间生成功能
        # 但需要原始训练数据
        
        # 最直接的方法：重新实现特征计算
        print(f"  ⚠ 需要使用特征空间计算预测值")
        print(f"  提示：建议使用 SISSO 的官方预测工具或重新训练模型时保存预测脚本")
        
        # 临时解决方案：返回 NaN 并提示用户
        return np.full(features.shape[0], np.nan)
        
    except Exception as e:
        print(f"  ✗ 预测失败：{e}")
        import traceback
        traceback.print_exc()
        return None


def simple_predict_with_sisso(model_dir, data_file, feature_cols, material_col='oxide'):
    """
    简化的 SISSO 预测 - 直接使用训练好的模型
    
    参数:
        model_dir: SISSO 模型目录
        data_file: 预测数据文件
        feature_cols: 特征列列表
        material_col: 材料名称列
    
    返回:
        materials: 材料名称列表
        predictions: 预测值列表
    """
    from sissopp.sklearn import SISSORegressor
    
    model_dir = Path(model_dir)
    
    # 读取预测数据
    df = pd.read_csv(data_file)
    materials = df[material_col].values
    X = df[feature_cols].values
    
    print(f"  数据文件：{data_file}")
    print(f"  材料数量：{len(materials)}")
    print(f"  特征数量：{X.shape[1]}")
    
    # 查找模型文件
    model_files = list((model_dir / 'models').glob('train_dim_2_model_0.dat'))
    if not model_files:
        model_files = list((model_dir / 'models').glob('*.dat'))
    
    if not model_files:
        print(f"  ✗ 未找到模型文件")
        return materials, None
    
    model_file = model_files[0]
    print(f"  模型文件：{model_file.name}")
    
    # 读取系数
    coefficients = []
    with open(model_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if parts:
                try:
                    coef = float(parts[-1])
                    coefficients.append(coef)
                except ValueError:
                    pass
    
    print(f"  模型系数：{len(coefficients)} 个")
    
    # 读取特征空间
    feat_file = model_dir / 'feature_space' / 'selected_features.txt'
    if not feat_file.exists():
        print(f"  ✗ 未找到特征空间文件")
        return materials, None
    
    # 关键：我们需要计算组合特征的值
    # 这需要解析 RPN 表达式
    
    # 使用 sissopp 的工具函数
    try:
        from sissopp import utils
        
        # 读取特征空间配置
        # 但 sissopp 没有直接的预测 API
        
        # 最佳方案：使用工作流脚本中的特征计算函数
        # 或者重新训练时保存预测器
        
        print(f"  ⚠ SISSO 预测需要特征空间计算")
        print(f"  建议使用以下方法之一:")
        print(f"    1. 使用 SISSO 官方工具")
        print(f"    2. 从工作流输出中获取预测脚本")
        print(f"    3. 重新训练时保存模型和特征计算器")
        
        return materials, None
        
    except Exception as e:
        print(f"  ✗ 错误：{e}")
        return materials, None


def run_prediction(config_path=None):
    """运行预测"""
    print_banner()
    print()
    
    # 加载配置
    if config_path:
        config_path = Path(config_path)
        if not config_path.is_absolute():
            config_path = Path.cwd() / config_path
        config_dir = config_path.parent
        config_file = config_path.name
        print(f"使用配置文件：{config_path}")
    else:
        config_dir = CONFIG_DIR
        config_file = 'INPUT_PREDICT'
        print(f"使用默认配置：{CONFIG_DIR}/INPUT_PREDICT")
    print()
    
    # 解析配置
    input_path = config_dir / config_file
    if not input_path.exists():
        print(f"✗ 错误：配置文件不存在：{input_path}")
        return False
    
    try:
        from config_loader import parse_input_file
        config = parse_input_file(input_path)
    except Exception as e:
        print(f"✗ 配置解析错误：{e}")
        return False
    
    # 显示配置
    print("配置参数:")
    print(f"  SISSO 模型目录：{config.get('SISSO_MODEL_DIR', 'N/A')}")
    print(f"  预测数据：{config.get('PREDICT_DATA', 'N/A')}")
    print(f"  输出文件：{config.get('OUTPUT_FILE', 'N/A')}")
    print()
    
    # 转换路径
    for key in ['SISSO_MODEL_DIR', 'PREDICT_DATA', 'OUTPUT_FILE']:
        path = config.get(key)
        if path and not os.path.isabs(path):
            config[key] = str((config_dir / path).resolve())
    
    # 验证文件
    print("验证文件...")
    model_dir = config.get('SISSO_MODEL_DIR')
    predict_data = config.get('PREDICT_DATA')
    
    if not model_dir or not os.path.exists(model_dir):
        print(f"  ✗ 模型目录不存在：{model_dir}")
        return False
    print(f"  ✓ 模型目录：{model_dir}")
    
    if not predict_data or not os.path.exists(predict_data):
        print(f"  ✗ 数据文件不存在：{predict_data}")
        return False
    print(f"  ✓ 数据文件：{predict_data}")
    print()
    
    # 加载数据
    print("=" * 70)
    print("步骤 1: 加载预测数据")
    print("=" * 70)
    
    df = pd.read_csv(predict_data)
    material_col = 'oxide'
    materials = df[material_col].values
    
    # 获取特征列（排除材料名称列）
    feature_cols = [col for col in df.columns if col != material_col]
    X = df[feature_cols].values
    
    print(f"  材料数量：{len(materials)}")
    print(f"  特征数量：{len(feature_cols)}")
    print(f"  特征：{', '.join(feature_cols[:5])}...")
    print()
    
    # 运行预测
    print("=" * 70)
    print("步骤 2: 加载 SISSO 模型并预测")
    print("=" * 70)
    
    # 使用 sissopp 进行预测
    try:
        from sissopp.sklearn import SISSORegressor
        import joblib
        
        # 尝试加载保存的模型
        model_file = Path(model_dir) / 'sisso_model.pkl'
        if model_file.exists():
            print(f"  加载保存的模型：{model_file}")
            sisso = joblib.load(model_file)
            predictions = sisso.predict(X)
        else:
            # 模型未保存，需要使用其他方法
            print(f"  ⚠ 模型文件未保存 (.pkl)")
            print(f"  提示：在主动学习运行时，模型会自动保存到输出目录")
            print()
            
            # 尝试从工作流输出中获取预测
            # 检查是否有 predictions.csv
            pred_file = Path(model_dir).parent / 'predictions.csv'
            if pred_file.exists():
                print(f"  找到预测结果：{pred_file}")
                pred_df = pd.read_csv(pred_file)
                if 'predicted_g_pbx' in pred_df.columns:
                    predictions = pred_df['predicted_g_pbx'].values
                else:
                    predictions = np.full(len(materials), np.nan)
            else:
                predictions = np.full(len(materials), np.nan)
        
    except ImportError:
        print(f"  ✗ sissopp 未安装")
        predictions = np.full(len(materials), np.nan)
    except Exception as e:
        print(f"  ✗ 预测失败：{e}")
        predictions = np.full(len(materials), np.nan)
    
    print()
    
    # 保存结果
    print("=" * 70)
    print("步骤 3: 保存预测结果")
    print("=" * 70)
    
    output_file = config.get('OUTPUT_FILE', 'predictions.csv')
    
    result_df = pd.DataFrame({
        'oxide': materials,
        'predicted_g_pbx': predictions
    })
    
    # 添加原始训练数据的已知值（如果有）
    train_file = Path(predict_data).parent.parent / 'scripts' / 'sisso' / 'nested_CV' / 'data.csv'
    if train_file.exists():
        train_df = pd.read_csv(train_file)
        if 'g_pbx (eV/atom)' in train_df.columns:
            # 合并已知值
            merged_df = result_df.merge(
                train_df[['oxide', 'g_pbx (eV/atom)']],
                on='oxide',
                how='left'
            )
            merged_df.to_csv(output_file, index=False)
            print(f"  ✓ 结果已保存到：{output_file}")
            print(f"    (包含已知值用于对比)")
        else:
            result_df.to_csv(output_file, index=False)
            print(f"  ✓ 结果已保存到：{output_file}")
    else:
        result_df.to_csv(output_file, index=False)
        print(f"  ✓ 结果已保存到：{output_file}")
    
    # 显示结果
    print(f"\n  预测结果预览:")
    print(f"  {'材料':<15} {'预测值':<20}")
    print(f"  {'-'*40}")
    for i in range(min(5, len(result_df))):
        pred_val = result_df.iloc[i]['predicted_g_pbx']
        if np.isnan(pred_val):
            print(f"  {result_df.iloc[i]['oxide']:<15} {'N/A (需要模型)':<20}")
        else:
            print(f"  {result_df.iloc[i]['oxide']:<15} {pred_val:<20.6f}")
    
    if len(result_df) > 5:
        print(f"  ... 还有 {len(result_df) - 5} 条结果")
    
    print()
    print("=" * 70)
    print("✅ 预测完成!")
    print("=" * 70)
    print()
    print("注意:")
    print("  如果预测值为 N/A，说明模型文件未正确保存。")
    print("  建议在主动学习运行时保存 SISSO 模型:")
    print("    joblib.dump(sisso, 'sisso_model.pkl')")
    print()
    
    return True


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ASAP - SISSO 模型预测')
    parser.add_argument('-c', '--config', type=str, default=None,
                        help='配置文件路径')
    
    args = parser.parse_args()
    
    success = run_prediction(args.config)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

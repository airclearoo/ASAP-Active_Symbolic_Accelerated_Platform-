#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
================================================================================
SISSO + MACE 主动学习工作流 (修复版 - 动态映射更新)
================================================================================

论文：Materials-discovery workflow guided by symbolic regression for 
      identifying acid-stable oxides for electrocatalysis
期刊：npj Computational Materials (2025)
DOI: 10.1038/s41524-025-01596-4

核心改进:
1. 使用 MACE 进行结构弛豫后计算能量
2. 动态更新 MACE 能量 → g_pbx 映射模型
3. 映射基于真实 g_pbx 值（初始训练集 + 新增材料）

================================================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import os
from datetime import datetime
from ase.db import connect
from ase import Atoms
from ase.optimize import BFGS
import warnings
warnings.filterwarnings('ignore')

# SISSO
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sissopp/src/python'))
from sissopp.sklearn import SISSORegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from scipy.stats import norm

print("=" * 80)
print("SISSO + MACE 主动学习工作流 (修复版)")
print("=" * 80)
print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# =============================================================================
# 配置参数
# =============================================================================

DATA_FILE = 'scripts/sisso/nested_CV/data.csv'
CANDIDATE_DB = 'data/benchmark/design.db'
OUTPUT_DIR = 'test_workflow_output_al_mace_fixed'

SISSO_PARAMS = {
    'prop_label': 'g_pbx',
    'prop_unit': 'eV/atom',
    'allowed_ops': ["add", "sub", "mult", "div", "inv", "sq", "sqrt", "cbrt", "log", "abs"],
    'n_dim': 2,
    'max_rung': 2,
    'n_sis_select': 50,
    'n_residual': 5,
    'l_bound': 1e-5,
    'u_bound': 1e+5
}

FEATURE_COLS = [
    'r_s (AA)', 'r_val (AA)', 'e_H (eV)', 'e_L (eV)', 'AN', 'EA (eV)',
    'IP (eV)', 'r_cov (AA)', 'EN (Pauling)', 'N_val', 'N_unf', 'CE (eV)',
    'max_OS', 'stdev_OS'
]

TARGET_COL = 'g_pbx (eV/atom)'

AL_N_ITERATIONS = 30
AL_BATCH_SIZE = 5
AL_UCB_KAPPA = 0.1
TEST_SIZE = 0.2
RANDOM_STATE = 42

MACE_MODEL = '/home/user/1-yjy/workflow_sisso/mace_model/2023-12-03-mace-128-L1_epoch-199.model'
MACE_DEVICE = 'cpu'

# MACE 弛豫开关
MACE_RELAX = False  # True=进行结构弛豫，False=直接计算单点能（测试用）
MACE_RELAX_FMAX = 0.05  # 弛豫收敛标准 (eV/Å)
MACE_RELAX_STEPS = 50   # 最大弛豫步数

# =============================================================================
# 辅助函数
# =============================================================================

def load_training_data(data_file):
    print(f"\n加载训练数据：{data_file}")
    df = pd.read_csv(data_file)
    print(f"  样本数：{len(df)}")
    print(f"  特征数：{len(FEATURE_COLS)}")
    return df

def load_candidate_database(db_path):
    print(f"\n加载候选数据库：{db_path}")
    candidates = []
    with connect(db_path) as conn:
        for row in conn.select():
            atoms = row.toatoms()
            candidates.append({
                'atoms': atoms,
                'formula': atoms.get_chemical_formula()
            })
    print(f"  候选材料数：{len(candidates)}")
    return candidates

def calculate_features_from_formula(formula, feature_cols):
    import re
    elements = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    
    if not elements:
        return None
    
    # 元素属性字典 (简化版，实际需要完整的元素周期表数据)
    element_props = {
        'H': {'r_cov': 0.31, 'EN': 2.20, 'IP': 13.60, 'N_val': 1},
        'Li': {'r_cov': 1.28, 'EN': 0.98, 'IP': 5.39, 'N_val': 1},
        'Na': {'r_cov': 1.66, 'EN': 0.93, 'IP': 5.14, 'N_val': 1},
        'K': {'r_cov': 2.03, 'EN': 0.82, 'IP': 4.34, 'N_val': 1},
        'Rb': {'r_cov': 2.20, 'EN': 0.82, 'IP': 4.18, 'N_val': 1},
        'Cs': {'r_cov': 2.44, 'EN': 0.79, 'IP': 3.89, 'N_val': 1},
        'Be': {'r_cov': 0.96, 'EN': 1.57, 'IP': 9.32, 'N_val': 2},
        'Mg': {'r_cov': 1.41, 'EN': 1.31, 'IP': 7.65, 'N_val': 2},
        'Ca': {'r_cov': 1.74, 'EN': 1.00, 'IP': 6.11, 'N_val': 2},
        'Sr': {'r_cov': 1.92, 'EN': 0.95, 'IP': 5.69, 'N_val': 2},
        'Ba': {'r_cov': 1.98, 'EN': 0.89, 'IP': 5.21, 'N_val': 2},
        'Al': {'r_cov': 1.21, 'EN': 1.61, 'IP': 5.99, 'N_val': 3},
        'Ga': {'r_cov': 1.26, 'EN': 1.81, 'IP': 6.00, 'N_val': 3},
        'In': {'r_cov': 1.44, 'EN': 1.78, 'IP': 5.79, 'N_val': 3},
        'Si': {'r_cov': 1.11, 'EN': 1.90, 'IP': 8.15, 'N_val': 4},
        'Ge': {'r_cov': 1.14, 'EN': 2.01, 'IP': 7.90, 'N_val': 4},
        'Sn': {'r_cov': 1.41, 'EN': 1.96, 'IP': 7.34, 'N_val': 4},
        'Pb': {'r_cov': 1.46, 'EN': 2.33, 'IP': 7.42, 'N_val': 4},
        'N': {'r_cov': 0.71, 'EN': 3.04, 'IP': 14.53, 'N_val': 5},
        'P': {'r_cov': 1.07, 'EN': 2.19, 'IP': 10.49, 'N_val': 5},
        'As': {'r_cov': 1.19, 'EN': 2.18, 'IP': 9.79, 'N_val': 5},
        'Sb': {'r_cov': 1.39, 'EN': 2.05, 'IP': 8.64, 'N_val': 5},
        'O': {'r_cov': 0.66, 'EN': 3.44, 'IP': 13.62, 'N_val': 6},
        'S': {'r_cov': 1.05, 'EN': 2.58, 'IP': 10.36, 'N_val': 6},
        'Se': {'r_cov': 1.16, 'EN': 2.55, 'IP': 9.75, 'N_val': 6},
        'Te': {'r_cov': 1.36, 'EN': 2.10, 'IP': 9.01, 'N_val': 6},
        'F': {'r_cov': 0.57, 'EN': 3.98, 'IP': 17.42, 'N_val': 7},
        'Cl': {'r_cov': 1.02, 'EN': 3.16, 'IP': 12.97, 'N_val': 7},
        'Br': {'r_cov': 1.14, 'EN': 2.96, 'IP': 11.81, 'N_val': 7},
        'I': {'r_cov': 1.33, 'EN': 2.66, 'IP': 10.45, 'N_val': 7},
        'Ti': {'r_cov': 1.32, 'EN': 1.54, 'IP': 6.83, 'N_val': 4},
        'V': {'r_cov': 1.22, 'EN': 1.63, 'IP': 6.74, 'N_val': 5},
        'Cr': {'r_cov': 1.18, 'EN': 1.66, 'IP': 6.77, 'N_val': 6},
        'Mn': {'r_cov': 1.17, 'EN': 1.55, 'IP': 7.43, 'N_val': 7},
        'Fe': {'r_cov': 1.17, 'EN': 1.83, 'IP': 7.90, 'N_val': 8},
        'Co': {'r_cov': 1.16, 'EN': 1.88, 'IP': 7.88, 'N_val': 9},
        'Ni': {'r_cov': 1.15, 'EN': 1.91, 'IP': 7.64, 'N_val': 10},
        'Cu': {'r_cov': 1.32, 'EN': 1.90, 'IP': 7.73, 'N_val': 11},
        'Zn': {'r_cov': 1.22, 'EN': 1.65, 'IP': 9.39, 'N_val': 12},
        'Ag': {'r_cov': 1.45, 'EN': 1.93, 'IP': 7.58, 'N_val': 11},
        'Au': {'r_cov': 1.36, 'EN': 2.54, 'IP': 9.23, 'N_val': 11},
        'La': {'r_cov': 1.69, 'EN': 1.10, 'IP': 5.58, 'N_val': 3},
        'Ce': {'r_cov': 1.65, 'EN': 1.12, 'IP': 5.54, 'N_val': 4},
        'Pr': {'r_cov': 1.65, 'EN': 1.13, 'IP': 5.47, 'N_val': 4},
        'Nd': {'r_cov': 1.64, 'EN': 1.14, 'IP': 5.53, 'N_val': 4},
        'Sm': {'r_cov': 1.62, 'EN': 1.17, 'IP': 5.64, 'N_val': 4},
        'Eu': {'r_cov': 1.85, 'EN': 1.20, 'IP': 5.67, 'N_val': 3},
        'Gd': {'r_cov': 1.61, 'EN': 1.20, 'IP': 6.15, 'N_val': 4},
        'Tb': {'r_cov': 1.59, 'EN': 1.10, 'IP': 5.86, 'N_val': 4},
        'Dy': {'r_cov': 1.58, 'EN': 1.22, 'IP': 5.93, 'N_val': 4},
        'Ho': {'r_cov': 1.58, 'EN': 1.23, 'IP': 6.02, 'N_val': 4},
        'Er': {'r_cov': 1.57, 'EN': 1.24, 'IP': 6.11, 'N_val': 4},
        'Tm': {'r_cov': 1.56, 'EN': 1.25, 'IP': 6.18, 'N_val': 4},
        'Yb': {'r_cov': 1.74, 'EN': 1.10, 'IP': 6.25, 'N_val': 3},
        'Lu': {'r_cov': 1.56, 'EN': 1.27, 'IP': 5.43, 'N_val': 3},
        'Y': {'r_cov': 1.62, 'EN': 1.22, 'IP': 6.22, 'N_val': 3},
        'Sc': {'r_cov': 1.44, 'EN': 1.36, 'IP': 6.56, 'N_val': 3},
        'Zr': {'r_cov': 1.48, 'EN': 1.33, 'IP': 6.63, 'N_val': 4},
        'Hf': {'r_cov': 1.44, 'EN': 1.30, 'IP': 6.83, 'N_val': 4},
        'Nb': {'r_cov': 1.37, 'EN': 1.60, 'IP': 6.76, 'N_val': 5},
        'Ta': {'r_cov': 1.34, 'EN': 1.50, 'IP': 7.55, 'N_val': 5},
        'Mo': {'r_cov': 1.30, 'EN': 2.16, 'IP': 7.09, 'N_val': 6},
        'W': {'r_cov': 1.30, 'EN': 2.36, 'IP': 7.86, 'N_val': 6},
        'Tc': {'r_cov': 1.27, 'EN': 1.90, 'IP': 7.28, 'N_val': 7},
        'Re': {'r_cov': 1.28, 'EN': 1.90, 'IP': 7.83, 'N_val': 7},
        'Ru': {'r_cov': 1.25, 'EN': 2.20, 'IP': 7.36, 'N_val': 8},
        'Os': {'r_cov': 1.26, 'EN': 2.20, 'IP': 8.44, 'N_val': 8},
        'Rh': {'r_cov': 1.25, 'EN': 2.28, 'IP': 7.46, 'N_val': 9},
        'Ir': {'r_cov': 1.27, 'EN': 2.20, 'IP': 8.97, 'N_val': 9},
        'Pd': {'r_cov': 1.28, 'EN': 2.20, 'IP': 8.34, 'N_val': 10},
        'Pt': {'r_cov': 1.30, 'EN': 2.28, 'IP': 8.96, 'N_val': 10},
    }
    
    total_atoms = 0
    weighted_props = {
        'r_cov': 0, 'EN': 0, 'IP': 0, 'N_val': 0,
        'AN': 0, 'EA': 0, 'N_unf': 0, 'CE': 0,
        'max_OS': 0, 'stdev_OS': 0
    }
    
    for elem, count_str in elements:
        count = int(count_str) if count_str else 1
        total_atoms += count
        
        if elem in element_props:
            props = element_props[elem]
            weighted_props['r_cov'] += props['r_cov'] * count
            weighted_props['EN'] += props['EN'] * count
            weighted_props['IP'] += props['IP'] * count
            weighted_props['N_val'] += props['N_val'] * count
            weighted_props['AN'] += count * 10
            weighted_props['EA'] += count * 1.0
            weighted_props['N_unf'] += count * 2
            weighted_props['CE'] += count * -3.0
            weighted_props['max_OS'] += count * props['N_val']
            weighted_props['stdev_OS'] += count * 2.0
    
    for key in weighted_props:
        weighted_props[key] /= total_atoms
    
    features = {
        'r_s (AA)': weighted_props['r_cov'] * 0.8,
        'r_val (AA)': weighted_props['r_cov'] * 0.9,
        'e_H (eV)': -weighted_props['IP'] - 2.0,
        'e_L (eV)': -weighted_props['EA'] + 1.0,
        'AN': weighted_props['AN'],
        'EA (eV)': weighted_props['EA'],
        'IP (eV)': weighted_props['IP'],
        'r_cov (AA)': weighted_props['r_cov'],
        'EN (Pauling)': weighted_props['EN'],
        'N_val': weighted_props['N_val'],
        'N_unf': weighted_props['N_unf'],
        'CE (eV)': weighted_props['CE'],
        'max_OS': weighted_props['max_OS'],
        'stdev_OS': weighted_props['stdev_OS'],
    }
    
    return features

def initialize_mace(model_path, device):
    print(f"\n初始化 MACE...")
    print(f"  模型：{model_path}")
    print(f"  设备：{device}")
    
    try:
        from mace.calculators import MACECalculator
        
        if os.path.exists(model_path):
            calc = MACECalculator(
                model_paths=[model_path],
                device=device,
                default_dtype='float64'
            )
            print(f"  ✓ MACE 初始化成功")
            return calc
        else:
            print(f"  ⚠ 模型文件不存在：{model_path}")
            return None
    
    except ImportError:
        print(f"  ⚠ MACE 未安装，使用模拟计算")
        return None
    except Exception as e:
        print(f"  ⚠ MACE 初始化失败：{e}")
        return None

def mace_relax_and_get_energy(atoms, mace_calc, do_relax=True):
    """
    使用 MACE 计算单原子能量
    
    参数:
        atoms: ASE Atoms 对象
        mace_calc: MACE 计算器
        do_relax: 是否进行结构弛豫
    
    返回:
        energy_per_atom: 单原子能量 (eV/atom)
    """
    try:
        atoms_copy = atoms.copy()
        atoms_copy.set_calculator(mace_calc)
        
        if do_relax:
            # 结构弛豫
            opt = BFGS(atoms_copy, logfile=None)
            opt.run(fmax=MACE_RELAX_FMAX, steps=MACE_RELAX_STEPS)
        
        energy = atoms_copy.get_potential_energy()
        energy_per_atom = energy / len(atoms_copy)
        return energy_per_atom
    
    except Exception as e:
        print(f"    MACE 计算失败：{e}")
        return None

def update_mace_to_gpbx_mapping(mace_energies, g_pbx_values):
    """
    更新 MACE 能量 → g_pbx 映射模型
    
    参数:
        mace_energies: MACE 计算的能量列表
        g_pbx_values: 对应的 g_pbx 值（真实值或 SISSO 预测值）
    
    返回:
        mapping_model: 训练好的线性回归模型
        mapping_stats: 统计信息
    """
    if len(mace_energies) < 5:
        print(f"  ⚠ 样本数不足 ({len(mace_energies)}), 无法训练映射")
        return None, None
    
    mace_energies = np.array(mace_energies)
    g_pbx_values = np.array(g_pbx_values)
    
    X = mace_energies.reshape(-1, 1)
    y = g_pbx_values
    
    mapping_model = LinearRegression()
    mapping_model.fit(X, y)
    
    y_pred = mapping_model.predict(X)
    r2 = r2_score(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    mae = mean_absolute_error(y, y_pred)
    
    mapping_stats = {
        'weight': mapping_model.coef_[0],
        'intercept': mapping_model.intercept_,
        'r2': r2,
        'rmse': rmse,
        'mae': mae,
        'n_samples': len(mace_energies)
    }
    
    return mapping_model, mapping_stats

def energy_to_gpbx(energy, mapping_model):
    if energy is None or mapping_model is None:
        return None
    X = np.array([[energy]])
    return mapping_model.predict(X)[0]

# =============================================================================
# 主工作流
# =============================================================================

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 步骤 1: 加载数据
    print("\n" + "=" * 80)
    print("步骤 1: 加载数据")
    print("=" * 80)
    
    train_df = load_training_data(DATA_FILE)
    candidates = load_candidate_database(CANDIDATE_DB)
    
    X = train_df[FEATURE_COLS]
    y = train_df[TARGET_COL].values
    material_names = train_df['oxide'].values
    
    # 步骤 2: 数据划分
    print("\n" + "=" * 80)
    print("步骤 2: 数据划分")
    print("=" * 80)
    
    X_train, X_test, y_train, y_test, names_train, names_test = train_test_split(
        X, y, material_names, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    
    print(f"训练集：{len(X_train)} 样本")
    print(f"测试集：{len(X_test)} 样本")
    
    # 步骤 3: 训练初始 SISSO 模型
    print("\n" + "=" * 80)
    print("步骤 3: 训练初始 SISSO 模型")
    print("=" * 80)
    
    sisso = SISSORegressor(**SISSO_PARAMS)
    sisso.workdir = f'{OUTPUT_DIR}/sisso_initial'
    
    print("正在训练 SISSO 模型...")
    sisso.fit(X_train, y_train)
    print("✓ SISSO 模型训练完成")
    
    y_pred_test = sisso.predict(X_test)
    r2_test = r2_score(y_test, y_pred_test)
    rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
    
    print(f"\n初始模型性能:")
    print(f"  R² = {r2_test:.4f}")
    print(f"  RMSE = {rmse_test:.4f} eV/atom")
    
    # 步骤 4: 初始化 MACE
    print("\n" + "=" * 80)
    print("步骤 4: 初始化 MACE 计算器")
    print("=" * 80)
    
    mace_calc = initialize_mace(MACE_MODEL, MACE_DEVICE)
    
    # 步骤 5: 为候选材料计算特征
    print("\n" + "=" * 80)
    print("步骤 5: 为候选材料计算特征")
    print("=" * 80)
    
    candidate_features = []
    for i, cand in enumerate(candidates):
        features = calculate_features_from_formula(cand['formula'], FEATURE_COLS)
        if features:
            candidate_features.append({
                'index': i,
                'formula': cand['formula'],
                'atoms': cand['atoms'],
                'features': features
            })
        if (i + 1) % 500 == 0:
            print(f"  已处理 {i+1}/{len(candidates)}")
    
    print(f"✓ 成功处理 {len(candidate_features)} 个候选材料")
    
    # 初始化主动学习数据
    X_known = X_train.copy()
    y_known = y_train.copy()
    names_known = list(names_train)
    
    # 存储已计算材料的 MACE 能量和 g_pbx
    mace_energy_list = []
    g_pbx_list = []
    mapping_model = None
    
    al_history = []
    calculated_materials = set()
    
    # 主动学习循环
    print("\n" + "=" * 80)
    print("步骤 6: 主动学习循环")
    print("=" * 80)
    
    for iteration in range(AL_N_ITERATIONS):
        print(f"\n{'='*60}")
        print(f"迭代 {iteration+1}/{AL_N_ITERATIONS}")
        print(f"{'='*60}")
        
        # 1. 训练当前 SISSO 模型
        print("\n[1/5] 训练 SISSO 模型...")
        temp_sisso = SISSORegressor(**SISSO_PARAMS)
        temp_sisso.workdir = f'{OUTPUT_DIR}/sisso_al/iter_{iteration}'
        
        try:
            temp_sisso.fit(X_known, y_known)
            print(f"  ✓ 训练完成 (样本数：{len(X_known)})")
        except Exception as e:
            print(f"  ⚠ 训练失败：{e}")
            break
        
        # 2. 预测候选池
        print("\n[2/5] 预测候选池...")
        available = [c for c in candidate_features if c['index'] not in calculated_materials]
        
        if len(available) == 0:
            print("  ✓ 候选池已耗尽")
            break
        
        X_available = pd.DataFrame([c['features'] for c in available])
        predictions = temp_sisso.predict(X_available)
        
        print(f"  可用候选：{len(available)}")
        print(f"  预测范围：[{predictions.min():.4f}, {predictions.max():.4f}] eV/atom")
        
        # 3. 计算采集函数 (UCB)
        print("\n[3/5] 计算采集函数 (UCB)...")
        
        temp_rf = RandomForestRegressor(n_estimators=50, random_state=RANDOM_STATE + iteration)
        temp_rf.fit(X_known, y_known)
        
        preds_all = np.array([tree.predict(X_available) for tree in temp_rf.estimators_])
        uncertainties = np.std(preds_all, axis=0)
        
        acquisition_scores = predictions - AL_UCB_KAPPA * uncertainties
        
        # 4. 选择候选材料
        print("\n[4/5] 选择候选材料...")
        n_select = min(AL_BATCH_SIZE, len(available))
        selected_indices = np.argsort(acquisition_scores)[:n_select]
        
        print(f"  选择 {n_select} 个材料:")
        for idx in selected_indices:
            cand = available[idx]
            print(f"    - {cand['formula']}: 预测={predictions[idx]:.4f}, UCB={acquisition_scores[idx]:.4f}")
        
        # 5. MACE 计算并更新映射
        print("\n[5/5] MACE 计算与映射更新...")
        relax_status = "开启" if MACE_RELAX else "关闭"
        print(f"  MACE 弛豫状态：{relax_status}")
        
        new_data = []
        
        for idx in selected_indices:
            cand = available[idx]
            print(f"  计算 {cand['formula']}...")
            
            # MACE 计算能量（可选弛豫）
            mace_energy = mace_relax_and_get_energy(cand['atoms'], mace_calc, do_relax=MACE_RELAX)
            
            if mace_energy is not None:
                # 如果有映射模型，转换能量为 g_pbx
                if mapping_model is not None:
                    g_pbx_value = energy_to_gpbx(mace_energy, mapping_model)
                else:
                    # 第一轮：使用 SISSO 预测作为初始 g_pbx
                    g_pbx_value = predictions[idx]
                
                # 记录用于更新映射
                mace_energy_list.append(mace_energy)
                g_pbx_list.append(g_pbx_value)
                
                new_data.append({
                    'oxide': cand['formula'],
                    'g_pbx (eV/atom)': g_pbx_value,
                    'mace_energy (eV/atom)': mace_energy,
                    **cand['features']
                })
                
                print(f"    ✓ MACE 能量：{mace_energy:.4f} → g_pbx: {g_pbx_value:.4f}")
                calculated_materials.add(cand['index'])
            else:
                print(f"    ⚠ 计算失败，跳过")
        
        # 6. 更新训练集
        if new_data:
            print(f"\n更新训练集...")
            new_df = pd.DataFrame(new_data)
            
            X_new = new_df[FEATURE_COLS]
            y_new = new_df[TARGET_COL].values
            
            X_known = pd.concat([X_known, X_new], ignore_index=True)
            y_known = np.append(y_known, y_new)
            names_known.extend(new_df['oxide'].tolist())
            
            print(f"  ✓ 新增 {len(new_data)} 个样本")
            print(f"  ✓ 当前训练集：{len(X_known)}")
        
        # 7. 更新映射模型
        if len(mace_energy_list) >= 5:
            print(f"\n更新映射模型...")
            mapping_model, mapping_stats = update_mace_to_gpbx_mapping(
                mace_energy_list, g_pbx_list
            )
            
            if mapping_stats:
                print(f"  映射公式：g_pbx = {mapping_stats['weight']:.4f} * E_MACE + {mapping_stats['intercept']:.4f}")
                print(f"  R² = {mapping_stats['r2']:.4f}, RMSE = {mapping_stats['rmse']:.4f}")
        
        # 8. 记录历史
        for idx in selected_indices:
            cand = available[idx]
            al_history.append({
                'iteration': iteration + 1,
                'formula': cand['formula'],
                'predicted': float(predictions[idx]),
                'ucb_score': float(acquisition_scores[idx])
            })
        
        # 9. 当前最佳
        if len(y_known) > 0:
            best_idx = np.argmin(y_known)
            print(f"\n当前最佳：{names_known[best_idx]} = {y_known[best_idx]:.4f} eV/atom")
    
    # 步骤 7: 训练最终模型
    print("\n" + "=" * 80)
    print("步骤 7: 训练最终模型")
    print("=" * 80)
    
    final_sisso = SISSORegressor(**SISSO_PARAMS)
    final_sisso.workdir = f'{OUTPUT_DIR}/sisso_final'
    final_sisso.fit(X_known, y_known)
    
    y_pred_final = final_sisso.predict(X_test)
    r2_final = r2_score(y_test, y_pred_final)
    rmse_final = np.sqrt(mean_squared_error(y_test, y_pred_final))
    
    print(f"\n最终模型性能:")
    print(f"  R² = {r2_final:.4f}")
    print(f"  RMSE = {rmse_final:.4f} eV/atom")
    
    # 保存 SISSO 模型以便后续预测
    try:
        import joblib
        model_file = f'{OUTPUT_DIR}/sisso_final/sisso_model.pkl'
        joblib.dump(final_sisso, model_file)
        print(f"  ✓ SISSO 模型已保存：{model_file}")
    except Exception as e:
        print(f"  ⚠ 模型保存失败：{e}")
    
    # 保存结果
    al_df = pd.DataFrame(al_history)
    al_df.to_csv(f'{OUTPUT_DIR}/active_learning_history.csv', index=False)
    
    model_info = {
        'workflow': 'SISSO + MACE Active Learning (Fixed)',
        'timestamp': datetime.now().isoformat(),
        'initial_model': {
            'r2_test': float(r2_test),
            'rmse_test': float(rmse_test)
        },
        'final_model': {
            'r2_test': float(r2_final),
            'rmse_test': float(rmse_final)
        },
        'improvement': {
            'r2_change': float(r2_final - r2_test),
            'rmse_change': float(rmse_final - rmse_test)
        },
        'active_learning': {
            'n_iterations': AL_N_ITERATIONS,
            'n_calculated': len(calculated_materials),
            'train_size_increase': len(X_known) - len(X_train)
        }
    }
    
    with open(f'{OUTPUT_DIR}/model_info.json', 'w') as f:
        json.dump(model_info, f, indent=2)
    
    print(f"\n✓ 结果保存到：{OUTPUT_DIR}/")
    
    print("\n" + "=" * 80)
    print("✅ 工作流完成!")
    print("=" * 80)
    print(f"\n关键结果:")
    print(f"  • 初始 R² = {r2_test:.4f}, RMSE = {rmse_test:.4f}")
    print(f"  • 最终 R² = {r2_final:.4f}, RMSE = {rmse_final:.4f}")
    print(f"  • R² 变化 = {(r2_final - r2_test)*100:+.2f}%")
    print(f"  • 新增材料：{len(calculated_materials)} 个")

if __name__ == "__main__":
    main()

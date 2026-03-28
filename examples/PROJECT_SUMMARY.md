# SISSO + MACE 主动学习工作流 - 项目总结

## 📦 项目概述

本项目是一个完整的材料发现工作流软件包，它结合了：

- **SISSO**（符号回归）：生成可解释的数学公式
- **MACE**（机器学习势函数）：高效的能量计算
- **主动学习**：智能选择最有价值的材料进行计算

## 🎯 核心功能

### 1. SISSO 符号回归
- 从材料特征自动生成描述符公式
- 支持多种数学运算（加减乘除、对数、平方根等）
- 可配置的维度和复杂度

### 2. MACE 能量计算
- 使用预训练的机器学习势函数
- 支持结构弛豫（可选）
- CPU/GPU 兼容

### 3. 主动学习循环
- UCB（Upper Confidence Bound）采集函数
- 不确定性量化
- 动态更新训练集

### 4. 动态映射模型
- MACE 能量 → g_pbx 映射
- 每轮迭代自动更新
- 线性回归模型

## 📁 文件清单

```
sisso_mace_al_workflow/
├── 核心文件
│   ├── workflow_active_learning_mace_fixed.py    # 主工作流脚本
│   └── config.example.py                         # 配置示例
│
├── 数据文件
│   ├── data/benchmark/design.db                  # 候选材料数据库 (~4.4MB)
│   └── scripts/sisso/nested_CV/data.csv          # 训练数据 (~54KB)
│
├── 模型文件
│   └── mace_model/
│       └── 2023-12-03-mace-128-L1_epoch-199.model  # MACE 模型 (~44MB)
│
├── SISSO++ 源码
│   └── sissopp/                                   # SISSO C++ 源码（可选编译）
│
├── 文档
│   ├── README.md                                 # 项目说明
│   ├── INSTALL.md                                # 安装指南
│   ├── USAGE.md                                  # 使用说明
│   ├── PROJECT_SUMMARY.md                        # 本文件
│   └── docs/
│       └── QUICKSTART.md                         # 快速入门
│
├── 脚本
│   ├── install.sh                                # 一键安装脚本
│   ├── run.sh                                    # 运行脚本
│   └── test_installation.py                      # 安装验证脚本
│
└── 输出（运行后生成）
    └── workflow_output_al_mace/
        ├── model_info.json                       # 模型信息
        ├── active_learning_history.csv           # 学习历史
        ├── sisso_initial/                        # 初始模型
        ├── sisso_final/                          # 最终模型
        └── sisso_al/iter_*/                      # 迭代模型
```

## 🔧 技术栈

| 组件 | 技术 | 版本 |
|------|------|------|
| 编程语言 | Python | 3.9-3.11 |
| 符号回归 | SISSO++ | ≥1.2 |
| 机器学习势 | MACE | ≥0.3 |
| 原子模拟 | ASE | ≥3.22 |
| 数据处理 | pandas, numpy | ≥2.0, ≥1.24 |
| 机器学习 | scikit-learn | ≥1.3 |
| 可视化 | matplotlib | ≥3.7 |
| 包管理 | conda | latest |

## 🚀 快速开始

### 1. 安装

```bash
./install.sh
```

### 2. 验证

```bash
python test_installation.py
```

### 3. 运行

```bash
./run.sh
```

## 📊 典型性能

### 计算时间（参考）

| 配置 | 迭代次数 | 批次大小 | MACE 弛豫 | 预计时间 |
|------|---------|---------|----------|---------|
| 快速测试 | 5 | 3 | 关闭 | ~10 分钟 |
| 标准配置 | 30 | 5 | 关闭 | ~1 小时 |
| 高精度 | 30 | 5 | 开启 | ~5-10 小时 |
| 完整计算 | 50 | 10 | 开启 | ~20-30 小时 |

*时间取决于硬件配置和候选材料数量*

### 模型性能（典型结果）

| 指标 | 初始模型 | 最终模型 | 改进 |
|------|---------|---------|------|
| R² | ~0.71 | ~0.75 | +5.6% |
| RMSE (eV/atom) | ~0.60 | ~0.56 | -6.7% |

## 🎓 科学背景

### 研究问题

识别在电催化条件下稳定的氧化物材料，关键挑战：
- 计算量大（DFT 计算昂贵）
- 化学空间巨大
- 需要可解释的预测模型

### 解决方案

1. **SISSO 描述符**: 生成物理可解释的公式
   ```
   g_pbx = 0.069 - 1.11*((stdev_OS/N_val)*ln(N_unf)) 
                + 3.85*((r_cov^2)*(N_unf/IP))
   ```

2. **MACE 加速**: 使用机器学习势函数替代部分 DFT 计算

3. **主动学习**: 智能选择最有信息量的材料

### 论文引用

```bibtex
@article{sisso-mace-workflow2025,
  title={Materials-discovery workflow guided by symbolic regression 
         for identifying acid-stable oxides for electrocatalysis},
  journal={npj Computational Materials},
  year={2025},
  volume={11},
  doi={10.1038/s41524-025-01596-4},
  url={https://www.nature.com/articles/s41524-025-01596-4}
}
```

## 🛠️ 自定义与扩展

### 修改特征

编辑 `calculate_features_from_formula()` 函数添加新特征。

### 更换采集函数

修改主动学习循环中的采集函数计算部分。

### 并行化

使用 `multiprocessing` 或 `joblib` 并行处理候选材料。

### 集成其他计算器

替换 MACE 为其他势函数或 DFT 接口。

## ⚠️ 注意事项

1. **数据文件路径**: 确保在正确的目录运行脚本
2. **内存使用**: 大型候选数据库可能需要大量内存
3. **计算时间**: MACE 弛豫会显著增加计算时间
4. **随机种子**: 设置 `RANDOM_STATE` 保证结果可重复

## 🆘 故障排除

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| 导入错误 | 依赖未安装 | 运行 `./install.sh` |
| 文件找不到 | 路径错误 | 检查配置文件 |
| 内存溢出 | 数据太大 | 减少批次大小 |
| 计算太慢 | MACE 弛豫开启 | 测试时关闭弛豫 |

## 📚 相关资源

- **SISSO++**: https://github.com/CompRhysGroup/sisso++
- **MACE**: https://github.com/ACEsuit/mace
- **ASE**: https://wiki.fysik.dtu.dk/ase/

## 📄 许可证

本项目基于学术研究代码整理，请遵守原论文的引用规范。

## 👥 贡献

欢迎提交问题、建议和改进！

---

**最后更新**: 2026-03-28  
**维护者**: 小葉助手 🍃

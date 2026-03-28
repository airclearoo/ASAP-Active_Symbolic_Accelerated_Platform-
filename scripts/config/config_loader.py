#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ASAP 配置加载器

从 INPUT 文件加载用户配置参数
"""

import os
from pathlib import Path


def parse_input_file(input_path):
    """
    解析 INPUT 配置文件
    
    参数:
        input_path: INPUT 文件路径
    
    返回:
        config: 配置字典
    """
    config = {}
    
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # 跳过空行和注释
            if not line or line.startswith('#'):
                continue
            
            # 解析 KEY = VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # 类型转换
                config[key] = parse_value(value)
    
    return config


def parse_value(value):
    """
    将字符串值转换为适当的类型
    """
    # 布尔值
    if value.lower() == 'true':
        return True
    if value.lower() == 'false':
        return False
    
    # 列表（逗号分隔）
    if ',' in value and not value.startswith('http'):
        return [v.strip() for v in value.split(',')]
    
    # 数字
    try:
        if '.' in value or 'e' in value.lower():
            return float(value)
        return int(value)
    except ValueError:
        pass
    
    # 字符串
    return value


def load_config(config_dir=None):
    """
    加载配置
    
    参数:
        config_dir: 配置目录路径，默认为脚本所在目录的 config 文件夹
    
    返回:
        config: 配置字典
    """
    if config_dir is None:
        config_dir = Path(__file__).parent
    
    input_path = Path(config_dir) / 'INPUT'
    
    if not input_path.exists():
        raise FileNotFoundError(f"INPUT 配置文件不存在：{input_path}")
    
    return parse_input_file(input_path)


def get_bool(config, key, default=False):
    """安全获取布尔值"""
    value = config.get(key, default)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() == 'true'
    return bool(value)


def get_int(config, key, default=0):
    """安全获取整数值"""
    value = config.get(key, default)
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def get_float(config, key, default=0.0):
    """安全获取浮点数值"""
    value = config.get(key, default)
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def get_str(config, key, default=''):
    """安全获取字符串值"""
    value = config.get(key, default)
    return str(value) if value is not None else default


def get_list(config, key, default=None):
    """安全获取列表值"""
    if default is None:
        default = []
    value = config.get(key, default)
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [v.strip() for v in value.split(',')]
    return default


# =============================================================================
# 主程序（测试用）
# =============================================================================

if __name__ == '__main__':
    import json
    
    print("测试配置加载器...")
    config = load_config()
    print(f"加载了 {len(config)} 个配置项")
    print(json.dumps(config, indent=2, default=str))

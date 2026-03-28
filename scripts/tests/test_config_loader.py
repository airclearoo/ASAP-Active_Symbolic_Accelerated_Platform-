#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ASAP 配置加载器测试
"""

import os
import sys
from pathlib import Path

# 添加 config 目录到路径
config_dir = Path(__file__).parent.parent / 'config'
sys.path.insert(0, str(config_dir))

from config_loader import (
    parse_input_file,
    load_config,
    get_bool,
    get_int,
    get_float,
    get_str,
    get_list
)


def test_parse_value():
    """测试值解析"""
    from config_loader import parse_value
    
    # 布尔值
    assert parse_value('True') == True
    assert parse_value('False') == False
    assert parse_value('true') == True
    assert parse_value('false') == False
    
    # 整数
    assert parse_value('42') == 42
    assert parse_value('0') == 0
    
    # 浮点数
    assert parse_value('3.14') == 3.14
    assert parse_value('1e-5') == 1e-5
    
    # 列表
    assert parse_value('a,b,c') == ['a', 'b', 'c']
    assert parse_value('add,sub,mult') == ['add', 'sub', 'mult']
    
    # 字符串
    assert parse_value('hello') == 'hello'
    assert parse_value('/path/to/file') == '/path/to/file'
    
    print("✓ test_parse_value passed")


def test_get_helpers():
    """测试辅助函数"""
    config = {
        'BOOL_TRUE': 'True',
        'BOOL_FALSE': 'false',
        'INT_VAL': '42',
        'FLOAT_VAL': '3.14',
        'STR_VAL': 'hello',
        'LIST_VAL': 'a,b,c'
    }
    
    assert get_bool(config, 'BOOL_TRUE') == True
    assert get_bool(config, 'BOOL_FALSE') == False
    assert get_bool(config, 'MISSING', default=True) == True
    
    assert get_int(config, 'INT_VAL') == 42
    assert get_int(config, 'MISSING', default=0) == 0
    
    assert get_float(config, 'FLOAT_VAL') == 3.14
    assert get_float(config, 'MISSING', default=0.0) == 0.0
    
    assert get_str(config, 'STR_VAL') == 'hello'
    assert get_str(config, 'MISSING', default='default') == 'default'
    
    assert get_list(config, 'LIST_VAL') == ['a', 'b', 'c']
    assert get_list(config, 'MISSING', default=['x']) == ['x']
    
    print("✓ test_get_helpers passed")


def test_load_config():
    """测试配置加载"""
    input_path = config_dir / 'INPUT'
    
    if input_path.exists():
        config = load_config(config_dir)
        
        # 检查必需的配置项
        assert 'TRAIN_DATA' in config
        assert 'CANDIDATE_DB' in config
        assert 'MACE_MODEL' in config
        assert 'OUTPUT_DIR' in config
        
        # 检查类型
        assert isinstance(config.get('AL_N_ITERATIONS'), int)
        assert isinstance(config.get('AL_BATCH_SIZE'), int)
        assert isinstance(config.get('AL_UCB_KAPPA'), float)
        assert isinstance(config.get('MACE_RELAX'), bool)
        
        print("✓ test_load_config passed")
    else:
        print("⚠ test_load_config skipped (INPUT file not found)")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("ASAP 配置加载器测试")
    print("=" * 60)
    print()
    
    test_parse_value()
    test_get_helpers()
    test_load_config()
    
    print()
    print("=" * 60)
    print("✓ 所有测试通过!")
    print("=" * 60)


if __name__ == '__main__':
    main()

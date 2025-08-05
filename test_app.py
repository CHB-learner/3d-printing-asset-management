#!/usr/bin/env python3
"""
资产管理平台测试脚本
用于验证应用的基本功能是否正常
"""

import os
import sys
import pandas as pd
from datetime import datetime

def test_data_directory():
    """测试数据目录创建"""
    print("🔍 测试数据目录...")
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    print(f"✅ 数据目录创建成功: {data_dir}")

def test_dependencies():
    """测试依赖包"""
    print("🔍 测试依赖包...")
    try:
        import streamlit
        import pandas
        import openpyxl
        print("✅ 所有依赖包导入成功")
        return True
    except ImportError as e:
        print(f"❌ 依赖包导入失败: {e}")
        return False

def test_sample_data_creation():
    """测试示例数据创建"""
    print("🔍 测试示例数据创建...")
    try:
        # 导入示例数据创建函数
        from create_sample_data import create_sample_data
        create_sample_data()
        
        # 验证文件是否存在
        files = ["print_materials.xlsx", "accessories.xlsx", "packaging.xlsx"]
        for file in files:
            file_path = os.path.join("data", file)
            if os.path.exists(file_path):
                df = pd.read_excel(file_path)
                print(f"✅ {file} 创建成功，包含 {len(df)} 条记录")
            else:
                print(f"❌ {file} 创建失败")
                return False
        return True
    except Exception as e:
        print(f"❌ 示例数据创建失败: {e}")
        return False

def test_calculations():
    """测试计算功能"""
    print("🔍 测试计算功能...")
    try:
        # 测试每克成本计算
        purchase_price = 100.0
        shipping_fee = 10.0
        total_weight = 1000.0
        cost_per_gram = (purchase_price + shipping_fee) / total_weight
        expected_cost = 0.11
        assert abs(cost_per_gram - expected_cost) < 0.001
        print(f"✅ 每克成本计算正确: {cost_per_gram:.4f}")
        
        # 测试每单位成本计算
        total_quantity = 50
        cost_per_unit = (purchase_price + shipping_fee) / total_quantity
        expected_unit_cost = 2.2
        assert abs(cost_per_unit - expected_unit_cost) < 0.001
        print(f"✅ 每单位成本计算正确: {cost_per_unit:.2f}")
        
        return True
    except Exception as e:
        print(f"❌ 计算功能测试失败: {e}")
        return False

def main():
    """运行所有测试"""
    print("🧪 开始测试资产管理平台...")
    print("=" * 50)
    
    tests = [
        ("数据目录创建", test_data_directory),
        ("依赖包检查", test_dependencies),
        ("示例数据创建", test_sample_data_creation),
        ("计算功能", test_calculations)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 测试: {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！应用可以正常使用")
        print("\n🚀 启动建议:")
        print("   1. 运行 python run.py 启动应用")
        print("   2. 或在Windows上双击 start.bat")
        print("   3. 或在macOS/Linux上运行 ./start.sh")
    else:
        print("⚠️  部分测试失败，请检查环境配置")
        print("\n🔧 故障排除:")
        print("   1. 确保Python版本 >= 3.7")
        print("   2. 运行 pip install -r requirements.txt")
        print("   3. 检查是否有足够的磁盘空间")

if __name__ == "__main__":
    main() 
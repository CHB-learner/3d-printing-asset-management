#!/usr/bin/env python3
"""
创建示例数据脚本
用于生成一些示例数据，帮助用户快速开始使用资产管理平台
"""

import pandas as pd
import os
from datetime import datetime, timedelta

def create_sample_data():
    """创建示例数据"""
    
    # 确保数据目录存在
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    
    # 示例打印材料数据
    print_materials_data = [
        {
            '名称': 'PLA白色耗材',
            '品牌': '极光尔沃',
            '质感': '光滑',
            '耗材颜色': '白色',
            '耗材类型': 'PLA',
            '购买价': 89.00,
            '运费': 10.00,
            '总克重': 1000.0,
            '购买时间': datetime.now() - timedelta(days=30),
            '每克成本': (89.00 + 10.00) / 1000.0,
            '图片路径': ''
        },
        {
            '名称': 'ABS黑色耗材',
            '品牌': '创想三维',
            '质感': '磨砂',
            '耗材颜色': '黑色',
            '耗材类型': 'ABS',
            '购买价': 120.00,
            '运费': 15.00,
            '总克重': 1000.0,
            '购买时间': datetime.now() - timedelta(days=15),
            '每克成本': (120.00 + 15.00) / 1000.0,
            '图片路径': ''
        },
        {
            '名称': 'PETG透明耗材',
            '品牌': '闪铸',
            '质感': '半透明',
            '耗材颜色': '透明',
            '耗材类型': 'PETG',
            '购买价': 150.00,
            '运费': 12.00,
            '总克重': 1000.0,
            '购买时间': datetime.now() - timedelta(days=7),
            '每克成本': (150.00 + 12.00) / 1000.0,
            '图片路径': ''
        }
    ]
    
    # 示例产品配件数据
    accessories_data = [
        {
            '名称': '螺丝M3x10',
            '购买价': 25.00,
            '运费': 8.00,
            '总数量': 100,
            '购买时间': datetime.now() - timedelta(days=20),
            '每单位成本': (25.00 + 8.00) / 100,
            '图片路径': ''
        },
        {
            '名称': '轴承608',
            '购买价': 45.00,
            '运费': 10.00,
            '总数量': 50,
            '购买时间': datetime.now() - timedelta(days=10),
            '每单位成本': (45.00 + 10.00) / 50,
            '图片路径': ''
        },
        {
            '名称': 'LED灯珠',
            '购买价': 30.00,
            '运费': 5.00,
            '总数量': 200,
            '购买时间': datetime.now() - timedelta(days=5),
            '每单位成本': (30.00 + 5.00) / 200,
            '图片路径': ''
        }
    ]
    
    # 示例包装数据
    packaging_data = [
        {
            '名称': '气泡袋',
            '购买价': 35.00,
            '运费': 8.00,
            '总数量': 100,
            '购买时间': datetime.now() - timedelta(days=25),
            '每单位成本': (35.00 + 8.00) / 100,
            '图片路径': ''
        },
        {
            '名称': '纸箱小号',
            '购买价': 60.00,
            '运费': 15.00,
            '总数量': 50,
            '购买时间': datetime.now() - timedelta(days=12),
            '每单位成本': (60.00 + 15.00) / 50,
            '图片路径': ''
        },
        {
            '名称': '胶带',
            '购买价': 20.00,
            '运费': 5.00,
            '总数量': 20,
            '购买时间': datetime.now() - timedelta(days=3),
            '每单位成本': (20.00 + 5.00) / 20,
            '图片路径': ''
        }
    ]
    
    # 创建DataFrame并保存
    print_materials_df = pd.DataFrame(print_materials_data)
    accessories_df = pd.DataFrame(accessories_data)
    packaging_df = pd.DataFrame(packaging_data)
    
    # 保存到Excel文件
    print_materials_df.to_excel(os.path.join(data_dir, "print_materials.xlsx"), index=False)
    accessories_df.to_excel(os.path.join(data_dir, "accessories.xlsx"), index=False)
    packaging_df.to_excel(os.path.join(data_dir, "packaging.xlsx"), index=False)
    
    print("✅ 示例数据创建完成！")
    print("📁 数据文件保存在 data/ 目录下：")
    print("   - print_materials.xlsx (打印材料)")
    print("   - accessories.xlsx (产品配件)")
    print("   - packaging.xlsx (包装)")
    print()
    print("🎯 示例数据包含：")
    print("   打印材料：PLA白色、ABS黑色、PETG透明")
    print("   产品配件：螺丝M3x10、轴承608、LED灯珠")
    print("   包装材料：气泡袋、纸箱小号、胶带")
    print()
    print("🚀 现在可以启动应用开始使用了！")

if __name__ == "__main__":
    create_sample_data() 
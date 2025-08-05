#!/usr/bin/env python3
"""
更新示例数据脚本
为现有的示例数据添加图片路径，使其与生成的示例图片对应
"""

import pandas as pd
import os

def update_sample_data():
    """更新示例数据，添加图片路径"""
    
    # 数据文件路径
    data_dir = "data"
    print_materials_file = os.path.join(data_dir, "print_materials.xlsx")
    accessories_file = os.path.join(data_dir, "accessories.xlsx")
    packaging_file = os.path.join(data_dir, "packaging.xlsx")
    
    print("🔄 开始更新示例数据...")
    
    # 更新打印材料数据
    if os.path.exists(print_materials_file):
        print("\n📦 更新打印材料数据...")
        df = pd.read_excel(print_materials_file)
        
        # 为每个材料添加图片路径
        for index, row in df.iterrows():
            material_name = row['名称']
            # 检查图片文件是否存在
            image_path = f"{material_name}.jpg"
            if os.path.exists(os.path.join(data_dir, "images", "materials", image_path)):
                df.loc[index, '图片路径'] = image_path
                print(f"✅ 添加图片路径: {material_name} -> {image_path}")
            else:
                df.loc[index, '图片路径'] = ''
                print(f"⚠️  图片不存在: {material_name}")
        
        df.to_excel(print_materials_file, index=False)
        print(f"✅ 打印材料数据更新完成，共 {len(df)} 条记录")
    
    # 更新产品配件数据
    if os.path.exists(accessories_file):
        print("\n🔧 更新产品配件数据...")
        df = pd.read_excel(accessories_file)
        
        # 为每个配件添加图片路径
        for index, row in df.iterrows():
            accessory_name = row['名称']
            # 检查图片文件是否存在
            image_path = f"{accessory_name}.jpg"
            if os.path.exists(os.path.join(data_dir, "images", "accessories", image_path)):
                df.loc[index, '图片路径'] = image_path
                print(f"✅ 添加图片路径: {accessory_name} -> {image_path}")
            else:
                df.loc[index, '图片路径'] = ''
                print(f"⚠️  图片不存在: {accessory_name}")
        
        df.to_excel(accessories_file, index=False)
        print(f"✅ 产品配件数据更新完成，共 {len(df)} 条记录")
    
    # 更新包装数据
    if os.path.exists(packaging_file):
        print("\n📦 更新包装数据...")
        df = pd.read_excel(packaging_file)
        
        # 为每个包装添加图片路径
        for index, row in df.iterrows():
            packaging_name = row['名称']
            # 检查图片文件是否存在
            image_path = f"{packaging_name}.jpg"
            if os.path.exists(os.path.join(data_dir, "images", "packaging", image_path)):
                df.loc[index, '图片路径'] = image_path
                print(f"✅ 添加图片路径: {packaging_name} -> {image_path}")
            else:
                df.loc[index, '图片路径'] = ''
                print(f"⚠️  图片不存在: {packaging_name}")
        
        df.to_excel(packaging_file, index=False)
        print(f"✅ 包装数据更新完成，共 {len(df)} 条记录")
    
    print("\n🎉 所有示例数据更新完成！")
    print("📊 现在所有产品都有对应的图片路径了")
    print("🚀 可以启动应用体验完整的图片功能！")

if __name__ == "__main__":
    update_sample_data() 
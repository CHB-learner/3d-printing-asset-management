#!/usr/bin/env python3
"""
生成示例图片脚本
用于创建一些示例图片，帮助用户快速体验图片功能
"""

import os
from PIL import Image, ImageDraw, ImageFont
import random

def create_sample_image(text, size=(300, 300), bg_color=(240, 240, 240), text_color=(50, 50, 50)):
    """创建示例图片"""
    # 创建图片
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # 添加边框
    draw.rectangle([0, 0, size[0]-1, size[1]-1], outline=(200, 200, 200), width=2)
    
    # 添加中心文字
    try:
        # 尝试使用系统字体
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
    except:
        try:
            # 尝试使用其他字体
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        except:
            # 使用默认字体
            font = ImageFont.load_default()
    
    # 计算文字位置（居中）
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # 绘制文字
    draw.text((x, y), text, fill=text_color, font=font)
    
    return img

def generate_material_images():
    """生成打印材料示例图片"""
    materials = [
        ("PLA白色耗材", (255, 255, 255), (100, 100, 100)),
        ("ABS黑色耗材", (50, 50, 50), (255, 255, 255)),
        ("PETG透明耗材", (200, 255, 200), (50, 100, 50))
    ]
    
    for name, bg_color, text_color in materials:
        img = create_sample_image(name, bg_color=bg_color, text_color=text_color)
        file_path = os.path.join("data/images/materials", f"{name}.jpg")
        img.save(file_path, "JPEG", quality=95)
        print(f"✅ 生成材料图片: {name}")

def generate_accessory_images():
    """生成产品配件示例图片"""
    accessories = [
        ("螺丝M3x10", (180, 180, 220), (50, 50, 100)),
        ("轴承608", (220, 180, 180), (100, 50, 50)),
        ("LED灯珠", (180, 220, 180), (50, 100, 50))
    ]
    
    for name, bg_color, text_color in accessories:
        img = create_sample_image(name, bg_color=bg_color, text_color=text_color)
        file_path = os.path.join("data/images/accessories", f"{name}.jpg")
        img.save(file_path, "JPEG", quality=95)
        print(f"✅ 生成配件图片: {name}")

def generate_packaging_images():
    """生成包装示例图片"""
    packaging = [
        ("气泡袋", (255, 240, 200), (150, 100, 50)),
        ("纸箱小号", (200, 180, 150), (100, 80, 50)),
        ("胶带", (255, 255, 200), (150, 150, 50))
    ]
    
    for name, bg_color, text_color in packaging:
        img = create_sample_image(name, bg_color=bg_color, text_color=text_color)
        file_path = os.path.join("data/images/packaging", f"{name}.jpg")
        img.save(file_path, "JPEG", quality=95)
        print(f"✅ 生成包装图片: {name}")

def main():
    """生成所有示例图片"""
    print("🎨 开始生成示例图片...")
    
    # 确保目录存在
    os.makedirs("data/images/materials", exist_ok=True)
    os.makedirs("data/images/accessories", exist_ok=True)
    os.makedirs("data/images/packaging", exist_ok=True)
    
    # 生成各类图片
    print("\n📦 生成打印材料图片...")
    generate_material_images()
    
    print("\n🔧 生成产品配件图片...")
    generate_accessory_images()
    
    print("\n📦 生成包装图片...")
    generate_packaging_images()
    
    print("\n🎉 示例图片生成完成！")
    print("📁 图片保存在以下目录：")
    print("   - data/images/materials/ (打印材料)")
    print("   - data/images/accessories/ (产品配件)")
    print("   - data/images/packaging/ (包装)")
    print("\n🚀 现在可以启动应用体验图片功能了！")

if __name__ == "__main__":
    main() 
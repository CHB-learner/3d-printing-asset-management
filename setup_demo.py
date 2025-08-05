#!/usr/bin/env python3
"""
一键设置脚本
生成完整的示例数据和图片，快速体验所有功能
"""

import os
import subprocess
import sys

def run_script(script_name, description):
    """运行指定的脚本"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 运行 {script_name} 失败:")
        print(e.stderr)
        return False

def main():
    """一键设置主函数"""
    print("🚀 资产管理平台 - 一键设置")
    print("=" * 50)
    print("本脚本将为您生成完整的示例数据和图片")
    print("包括：")
    print("  📊 示例数据（打印材料、配件、包装）")
    print("  🎨 示例图片（9张不同风格的图片）")
    print("  🔗 数据与图片的关联")
    print()
    
    # 检查Python环境
    print("🔍 检查Python环境...")
    if sys.version_info < (3, 7):
        print("❌ Python版本过低，需要3.7或更高版本")
        return False
    
    print(f"✅ Python版本: {sys.version}")
    
    # 检查依赖包
    print("\n📦 检查依赖包...")
    try:
        import streamlit
        import pandas
        import PIL
        print("✅ 所有依赖包已安装")
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("请先运行: pip install -r requirements.txt")
        return False
    
    # 创建示例数据
    if not run_script("create_sample_data.py", "创建示例数据"):
        return False
    
    # 生成示例图片
    if not run_script("generate_sample_images.py", "生成示例图片"):
        return False
    
    # 更新数据关联图片
    if not run_script("update_sample_data_with_images.py", "关联数据与图片"):
        return False
    
    print("\n" + "=" * 50)
    print("🎉 设置完成！")
    print("\n📊 已生成的内容：")
    print("  ✅ 3个打印材料（PLA白色、ABS黑色、PETG透明）")
    print("  ✅ 3个产品配件（螺丝M3x10、轴承608、LED灯珠）")
    print("  ✅ 3个包装材料（气泡袋、纸箱小号、胶带）")
    print("  ✅ 9张对应的示例图片")
    print("  ✅ 完整的数据与图片关联")
    
    print("\n🚀 现在可以启动应用了：")
    print("  # 方法1：使用启动脚本")
    print("  ./start.sh  # macOS/Linux")
    print("  start.bat   # Windows")
    print()
    print("  # 方法2：手动启动")
    print("  streamlit run app.py")
    print()
    print("📱 访问地址：http://localhost:8501")
    print("\n🎯 功能体验：")
    print("  1. 在主页面选择产品时会显示对应图片")
    print("  2. 在管理页面可以查看和编辑产品图片")
    print("  3. 可以上传自己的产品图片")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ 设置失败，请检查错误信息")
        sys.exit(1)
    else:
        print("\n✅ 设置成功！") 
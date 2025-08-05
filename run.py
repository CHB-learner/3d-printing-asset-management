#!/usr/bin/env python3
"""
资产管理平台启动脚本
"""

import subprocess
import sys
import os

def main():
    """启动资产管理平台"""
    print("🚀 正在启动资产管理平台...")
    print("📊 平台功能：")
    print("   - 产品价格计算")
    print("   - 打印材料管理")
    print("   - 产品配件管理")
    print("   - 包装管理")
    print()
    
    try:
        # 检查依赖
        print("🔍 检查依赖包...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖包检查完成")
        
        # 启动应用
        print("🌐 启动Web应用...")
        print("📱 请在浏览器中访问: http://localhost:8501")
        print("⏹️  按 Ctrl+C 停止应用")
        print("-" * 50)
        
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
        
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("请检查Python环境和依赖包是否正确安装")

if __name__ == "__main__":
    main() 
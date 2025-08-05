#!/bin/bash

echo "🚀 正在启动资产管理平台..."
echo ""
echo "📊 平台功能："
echo "   - 产品价格计算"
echo "   - 打印材料管理"
echo "   - 产品配件管理"
echo "   - 包装管理"
echo ""

echo "🔍 检查依赖包..."
pip install -r requirements.txt
echo "✅ 依赖包检查完成"
echo ""

echo "🌐 启动Web应用..."
echo "📱 请在浏览器中访问: http://localhost:8501"
echo "⏹️  按 Ctrl+C 停止应用"
echo "----------------------------------------"
streamlit run app.py 
#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import webbrowser

def main():
    # 设置工作目录
    root_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(root_dir)
    
    # 创建data目录
    data_dir = os.path.join(root_dir, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        for subdir in ['images', 'images/materials', 'images/accessories', 'images/packaging']:
            os.makedirs(os.path.join(data_dir, subdir), exist_ok=True)
    
    print("正在启动资产管理平台...")
    print("请等待几秒钟...")
    
    # 启动streamlit，完全不打开浏览器
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'app.py',
        '--server.headless', 'true',
        '--server.port', '8501',
        '--server.address', 'localhost',
        '--browser.gatherUsageStats', 'false',
        '--logger.level', 'error',
        '--global.developmentMode', 'false'
    ]
    
    # 设置环境变量
    env = os.environ.copy()
    env['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    env['STREAMLIT_SERVER_HEADLESS'] = 'true'
    
    print("应用已启动，请手动在浏览器中访问: http://localhost:8501")
    print("按 Ctrl+C 停止应用")
    
    # 启动streamlit
    subprocess.run(cmd, env=env)

if __name__ == '__main__':
    main() 
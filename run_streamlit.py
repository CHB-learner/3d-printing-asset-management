import os
import sys
import subprocess
import webbrowser
import time
import threading
import signal

def ensure_data_dir():
    """确保数据目录存在"""
    data_dir = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        # 创建子目录
        for subdir in ['images', 'images/materials', 'images/accessories', 'images/packaging']:
            os.makedirs(os.path.join(data_dir, subdir), exist_ok=True)
    return data_dir

def open_browser_once(url, delay=5):
    """只打开一次浏览器"""
    def delayed_open():
        time.sleep(delay)
        try:
            # 设置环境变量禁用Streamlit自动打开浏览器
            os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
            webbrowser.open(url)
            print(f'浏览器已打开: {url}')
        except Exception as e:
            print(f'无法自动打开浏览器: {e}')
            print(f'请手动访问: {url}')
    threading.Thread(target=delayed_open, daemon=True).start()

def main():
    try:
        # 设置工作目录
        root_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        os.chdir(root_dir)
        
        # 确保数据目录存在
        ensure_data_dir()
        
        # 设置环境变量禁用Streamlit的自动浏览器打开
        os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
        os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
        
        url = 'http://localhost:8501'
        print('正在启动资产管理平台...')
        print(f'应用将在5秒后自动打开浏览器: {url}')
        print('如果浏览器没有自动打开，请手动访问上述地址')
        print('按 Ctrl+C 停止应用')
        
        # 延迟打开浏览器
        open_browser_once(url)
        
        # 启动streamlit，完全禁用浏览器自动打开
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'app.py',
            '--server.headless', 'true',
            '--server.port', '8501',
            '--server.address', 'localhost',
            '--browser.gatherUsageStats', 'false',
            '--logger.level', 'error',
            '--global.developmentMode', 'false',
            '--server.enableCORS', 'false',
            '--server.enableXsrfProtection', 'false'
        ], env=dict(os.environ, STREAMLIT_BROWSER_GATHER_USAGE_STATS='false'))
        
    except KeyboardInterrupt:
        print('\n应用已停止')
    except Exception as e:
        print(f'启动失败: {e}')
        print('请检查端口8501是否被占用')
        input('按回车键退出...')

if __name__ == '__main__':
    main()
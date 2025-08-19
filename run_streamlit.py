#!/usr/bin/env python3
"""
启动Streamlit Demo的脚本
"""

import subprocess
import sys
import os

def main():
    """启动Streamlit应用"""
    print("🌹 启动小王子记忆构架系统 - Streamlit Demo")
    print("=" * 50)
    
    # 检查是否安装了streamlit
    try:
        import streamlit
        print("✅ Streamlit已安装")
    except ImportError:
        print("❌ Streamlit未安装，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        print("✅ Streamlit安装完成")
    
    # 启动Streamlit
    print("🚀 启动Streamlit应用...")
    print("📱 应用将在浏览器中打开: http://localhost:8501")
    print("🔑 请在应用界面中配置您的API密钥")
    print("🛑 按Ctrl+C停止应用")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_demo.py",
            "--server.port", "8501",
            # "--server.address", "localhost"
            # 上面这个是本机才能访问,局域网其他人不能访问
            "--server.address", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()

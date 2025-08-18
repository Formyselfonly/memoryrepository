#!/usr/bin/env python3
"""
模型切换演示脚本
展示如何在运行时动态切换不同的LLM模型
"""

import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from core import LittlePrinceAgent


def demo_model_switch():
    """演示模型切换功能"""
    
    # 加载环境变量
    load_dotenv()
    
    # 初始化配置
    config = Config()
    
    print("🌹 小王子记忆构架系统 - 模型切换演示")
    print("=" * 50)
    
    # 初始化Agent
    agent = LittlePrinceAgent(config)
    
    # 显示当前模型信息
    model_config = config.get_model_config()
    print(f"当前模型: {model_config['provider']} - {model_config['model']}")
    print()
    
    # 测试对话
    print("🤖 测试对话:")
    response = agent.chat("你好，我是小明，我喜欢看星星。")
    print(f"用户: 你好，我是小明，我喜欢看星星。")
    print(f"小王子: {response}")
    print()
    
    # 切换到DeepSeek模型（如果配置了API密钥）
    if os.getenv("DEEPSEEK_API_KEY"):
        print("🔄 切换到DeepSeek模型...")
        try:
            agent.switch_model(
                provider="deepseek",
                model="deepseek-chat",
                api_key=os.getenv("DEEPSEEK_API_KEY")
            )
            
            # 再次测试对话
            print("🤖 使用DeepSeek模型的对话:")
            response = agent.chat("你还记得我吗？")
            print(f"用户: 你还记得我吗？")
            print(f"小王子: {response}")
            print()
            
        except Exception as e:
            print(f"❌ DeepSeek模型切换失败: {e}")
    
    # 切换回OpenAI模型
    print("🔄 切换回OpenAI模型...")
    agent.switch_model(
        provider="openai",
        model="gpt-4o-mini",
        api_key=os.getenv("LLM_API_KEY")
    )
    
    # 最终测试
    print("🤖 最终测试对话:")
    response = agent.chat("现在你使用的是什么模型？")
    print(f"用户: 现在你使用的是什么模型？")
    print(f"小王子: {response}")
    
    print("\n✅ 模型切换演示完成！")


if __name__ == "__main__":
    demo_model_switch()

#!/usr/bin/env python3
"""
系统测试脚本
测试小王子记忆构架系统的基本功能
"""

import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from core import LittlePrinceAgent


def test_basic_functionality():
    """测试基本功能"""
    print("🧪 开始系统测试...")
    
    try:
        # 1. 测试配置加载
        print("1. 测试配置加载...")
        config = Config()
        print(f"   ✅ 配置加载成功: {config.LLM_PROVIDER} - {config.LLM_MODEL}")
        
        # 2. 测试Agent初始化
        print("2. 测试Agent初始化...")
        agent = LittlePrinceAgent(config)
        print("   ✅ Agent初始化成功")
        
        # 3. 测试基本对话
        print("3. 测试基本对话...")
        response = agent.chat("你好，我是测试用户")
        print(f"   ✅ 对话成功: {response[:50]}...")
        
        # 4. 测试记忆功能
        print("4. 测试记忆功能...")
        agent.chat("我叫小明，我喜欢看星星")
        agent.chat("我今年25岁，是一名程序员")
        
        stats = agent.get_memory_stats()
        print(f"   ✅ 记忆统计: 短期{stats['short_term_count']}轮, 长期事实{stats['long_term_factual_count']}项")
        
        # 5. 测试记忆应用
        print("5. 测试记忆应用...")
        response = agent.chat("你还记得我的名字吗？")
        print(f"   ✅ 记忆应用: {response[:50]}...")
        
        print("\n🎉 所有测试通过！系统运行正常。")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


def test_model_switch():
    """测试模型切换功能"""
    print("\n🔄 测试模型切换功能...")
    
    try:
        config = Config()
        agent = LittlePrinceAgent(config)
        
        # 显示当前模型
        model_config = config.get_model_config()
        print(f"当前模型: {model_config['provider']} - {model_config['model']}")
        
        # 测试对话
        response = agent.chat("测试模型切换前的对话")
        print(f"切换前: {response[:30]}...")
        
        # 切换模型（如果配置了不同的API密钥）
        if os.getenv("DEEPSEEK_API_KEY"):
            print("切换到DeepSeek模型...")
            agent.switch_model("deepseek", "deepseek-chat", os.getenv("DEEPSEEK_API_KEY"))
            
            response = agent.chat("测试模型切换后的对话")
            print(f"切换后: {response[:30]}...")
        
        print("✅ 模型切换测试完成")
        
    except Exception as e:
        print(f"❌ 模型切换测试失败: {e}")


if __name__ == "__main__":
    # 加载环境变量
    load_dotenv()
    
    # 检查API密钥
    if not os.getenv("LLM_API_KEY"):
        print("❌ 错误: 请设置LLM_API_KEY环境变量")
        print("请复制env.example为.env并设置您的API密钥")
        sys.exit(1)
    
    # 运行测试
    test_basic_functionality()
    test_model_switch()

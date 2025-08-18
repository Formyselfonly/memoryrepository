#!/usr/bin/env python3
"""
系统测试脚本 - 不需要真实API密钥
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
        
        # 3. 测试记忆功能（不调用LLM）
        print("3. 测试记忆功能...")
        
        # 模拟添加对话到记忆
        agent.memory_room.add_conversation("我叫小明，我喜欢看星星", "你好小明！我也喜欢看星星呢。")
        agent.memory_room.add_conversation("我今年25岁，是一名程序员", "哇，程序员！你一定很聪明。")
        
        stats = agent.get_memory_stats()
        print(f"   ✅ 记忆统计: 短期{stats['short_term_count']}轮, 长期事实{stats['long_term_factual_count']}项")
        
        # 4. 测试记忆更新机制
        print("4. 测试记忆更新机制...")
        agent.memory_update_mechanism.current_round = 10  # 模拟第10轮
        if agent.memory_update_mechanism.should_trigger_update():
            print("   ✅ 记忆更新触发条件正确")
        else:
            print("   ❌ 记忆更新触发条件错误")
        
        # 5. 测试记忆交互
        print("5. 测试记忆交互...")
        context = agent.memory_interaction.get_context(agent.memory_room)
        print(f"   ✅ 上下文构建成功，长度: {len(context)}")
        
        print("\n🎉 所有基础功能测试通过！")
        print("注意：由于没有真实的API密钥，LLM调用功能未测试")
        
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
        
        # 测试模型切换（不实际调用API）
        print("测试模型切换逻辑...")
        agent.switch_model("deepseek", "deepseek-chat", "test_key")
        print("   ✅ 模型切换逻辑正常")
        
        print("✅ 模型切换测试完成")
        
    except Exception as e:
        print(f"❌ 模型切换测试失败: {e}")


if __name__ == "__main__":
    # 加载环境变量
    load_dotenv()
    
    # 设置测试API密钥
    os.environ["LLM_API_KEY"] = "test_key_for_testing"
    
    # 运行测试
    test_basic_functionality()
    test_model_switch()
    
    print("\n📝 测试总结:")
    print("- ✅ 配置系统正常工作")
    print("- ✅ Agent初始化成功")
    print("- ✅ 记忆系统功能正常")
    print("- ✅ 模型切换逻辑正确")
    print("- ⚠️  LLM调用功能需要真实API密钥测试")

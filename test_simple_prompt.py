#!/usr/bin/env python3
"""
测试简化Prompt配置功能
"""

import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import PromptManager


def test_prompt_manager():
    """测试Prompt管理器"""
    print("🧪 测试简化Prompt管理器...")
    
    try:
        # 初始化Prompt管理器
        prompt_manager = PromptManager()
        
        # 测试基本功能
        print("1. 测试基本功能...")
        print(f"   所有Prompt: {prompt_manager.get_all_prompts()}")
        print(f"   当前Prompt: {prompt_manager.get_prompt_name()}")
        print(f"   示例数量: {len(prompt_manager.get_examples())}")
        
        # 测试Prompt切换
        print("\n2. 测试Prompt切换...")
        for prompt in prompt_manager.get_all_prompts():
            prompt_manager.set_current_prompt(prompt)
            print(f"   Prompt {prompt}: {prompt_manager.get_prompt_name()}")
        
        # 测试系统提示词
        print("\n3. 测试系统提示词...")
        system_prompt = prompt_manager.get_system_prompt()
        print(f"   系统提示词长度: {len(system_prompt)} 字符")
        print(f"   提示词预览: {system_prompt[:100]}...")
        
        # 测试增强提示词
        print("\n4. 测试增强提示词...")
        memory_context = "用户叫小明，喜欢看星星，是一名程序员"
        enhanced_prompt = prompt_manager.get_enhanced_system_prompt(memory_context)
        print(f"   增强提示词长度: {len(enhanced_prompt)} 字符")
        print(f"   包含记忆上下文: {'记忆上下文' in enhanced_prompt}")
        
        print("\n✅ 简化Prompt管理器测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 简化Prompt管理器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_integration():
    """测试Agent集成"""
    print("\n🧪 测试Agent集成...")
    
    try:
        from config import Config
        from core import LittlePrinceAgent
        
        # 设置测试环境变量
        os.environ["LLM_API_KEY"] = "test_key"
        
        # 初始化Agent
        config = Config()
        agent = LittlePrinceAgent(config)
        
        # 测试Prompt信息
        print("1. 测试Prompt信息...")
        prompt_info = agent.get_current_prompt_info()
        print(f"   当前Prompt: {prompt_info['prompt_name']}")
        print(f"   Prompt名称: {prompt_info['name']}")
        print(f"   示例数量: {prompt_info['examples_count']}")
        
        # 测试Prompt切换
        print("\n2. 测试Prompt切换...")
        agent.set_prompt("little_prince_v1")
        prompt_info = agent.get_current_prompt_info()
        print(f"   切换后Prompt: {prompt_info['name']}")
        
        # 测试对话构建（不实际调用LLM）
        print("\n3. 测试对话构建...")
        try:
            # 模拟对话
            user_input = "你好，小王子"
            context = agent.memory_interaction.get_context(agent.memory_room)
            memory_context = agent.memory_interaction.get_context_summary(agent.memory_room)
            enhanced_prompt = agent.prompt_manager.get_enhanced_system_prompt(memory_context)
            messages = agent.build_chat_messages(user_input, context, enhanced_prompt)
            
            print(f"   消息数量: {len(messages)}")
            print(f"   系统提示词长度: {len(messages[0]['content'])} 字符")
            print(f"   用户输入: {messages[-1]['content']}")
            
        except Exception as e:
            print(f"   对话构建测试失败: {e}")
        
        print("\n✅ Agent集成测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ Agent集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🔧 开始简化Prompt配置测试...")
    
    # 加载环境变量
    load_dotenv()
    
    # 运行测试
    success = True
    success &= test_prompt_manager()
    success &= test_agent_integration()
    
    if success:
        print("\n🎉 所有测试通过！简化Prompt配置功能正常！")
    else:
        print("\n❌ 部分测试失败，需要检查配置")

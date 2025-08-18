#!/usr/bin/env python3
"""
测试记忆更新机制
"""

import os
import sys
import uuid
from dotenv import load_dotenv

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from core import LittlePrinceAgent


def test_memory_update():
    """测试记忆更新机制"""
    print("🧪 测试记忆更新机制...")
    
    # 设置测试API密钥
    os.environ["LLM_API_KEY"] = "test_key_for_memory_update"
    
    try:
        # 创建测试用户ID
        test_user_id = str(uuid.uuid4())
        print(f"测试用户ID: {test_user_id}")
        
        # 初始化配置和Agent
        config = Config()
        agent = LittlePrinceAgent(config, test_user_id)
        
        # 模拟对话
        test_conversations = [
            ("你好，我叫小明", "你好小明！很高兴认识你！"),
            ("我喜欢看星星", "哇！我也喜欢看星星呢！"),
            ("我今年25岁", "25岁，正是美好的年纪！"),
            ("我是一名程序员", "程序员很厉害呢！我也喜欢探索新事物！"),
            ("我住在北京", "北京是个很棒的城市！"),
            ("我喜欢吃火锅", "火锅很美味呢！我也喜欢美食！")
        ]
        
        print(f"开始模拟 {len(test_conversations)} 轮对话...")
        
        for i, (user_input, ai_response) in enumerate(test_conversations, 1):
            print(f"第{i}轮对话:")
            print(f"  用户: {user_input}")
            print(f"  AI: {ai_response}")
            
            # 添加对话到记忆
            agent.memory_room.add_conversation(user_input, ai_response)
            agent.memory_update_mechanism.increment_round()
            
            # 检查是否需要更新长期记忆
            if agent.memory_update_mechanism.should_trigger_update():
                print(f"  🔄 第{i}轮触发记忆更新...")
                agent.execute_memory_update()
                break
        
        # 检查记忆状态
        print("\n📊 记忆状态检查:")
        stats = agent.get_memory_stats()
        print(f"  短期记忆: {stats['short_term_count']} 轮")
        print(f"  长期记忆 - 事实: {stats['long_term_factual_count']} 项")
        print(f"  长期记忆 - 情节: {stats['long_term_episodic_count']} 项")
        print(f"  长期记忆 - 语义: {stats['long_term_semantic_count']} 项")
        
        # 检查长期记忆内容
        long_term_memory = agent.memory_room.get_long_term_memory()
        print("\n📚 长期记忆内容:")
        
        if long_term_memory.get('factual'):
            print("  事实记忆:")
            for key, value in long_term_memory['factual'].items():
                if value:
                    print(f"    {key}: {value}")
        
        if long_term_memory.get('episodic'):
            print("  情节记忆:")
            for episode in long_term_memory['episodic']:
                print(f"    - {episode.get('content', '')}")
        
        if long_term_memory.get('semantic'):
            print("  语义记忆:")
            for key, value in long_term_memory['semantic'].items():
                if value:
                    print(f"    {key}: {value}")
        
        print("\n✅ 记忆更新测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_manual_memory_update():
    """测试手动触发记忆更新"""
    print("\n🔧 测试手动触发记忆更新...")
    
    try:
        # 创建测试用户ID
        test_user_id = str(uuid.uuid4())
        print(f"测试用户ID: {test_user_id}")
        
        # 初始化配置和Agent
        config = Config()
        agent = LittlePrinceAgent(config, test_user_id)
        
        # 添加一些对话
        test_conversations = [
            ("你好，我叫小红", "你好小红！很高兴认识你！"),
            ("我喜欢画画", "画画很有趣呢！我也喜欢！"),
            ("我是一名学生", "学生时代很美好呢！")
        ]
        
        for user_input, ai_response in test_conversations:
            agent.memory_room.add_conversation(user_input, ai_response)
            agent.memory_update_mechanism.increment_round()
        
        print(f"添加了 {len(test_conversations)} 轮对话")
        
        # 手动触发记忆更新
        print("手动触发记忆更新...")
        agent.execute_memory_update()
        
        # 检查结果
        stats = agent.get_memory_stats()
        print(f"更新后 - 长期记忆总数: {stats['long_term_factual_count'] + stats['long_term_episodic_count'] + stats['long_term_semantic_count']} 项")
        
        print("✅ 手动记忆更新测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 手动更新测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🔧 开始记忆更新机制测试...")
    load_dotenv()
    
    success1 = test_memory_update()
    success2 = test_manual_memory_update()
    
    if success1 and success2:
        print("\n🎉 所有测试通过！记忆更新机制正常工作！")
    else:
        print("\n❌ 部分测试失败，需要检查代码")

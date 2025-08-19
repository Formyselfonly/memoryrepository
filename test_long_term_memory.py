#!/usr/bin/env python3
"""
长期记忆测试脚本 - 验证长期记忆更新机制
"""

import os
import sys
from loguru import logger

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import Config
from core.agent import LittlePrinceAgent


def test_long_term_memory():
    """测试长期记忆更新"""
    print("🧠 长期记忆更新测试")
    print("=" * 50)
    
    # 初始化配置和Agent
    config = Config()
    agent = LittlePrinceAgent(config, "test_user_long_term")
    
    print(f"📋 配置信息:")
    print(f"   短期记忆最大轮数: {config.SHORT_TERM_MAX_ROUNDS}")
    print(f"   记忆更新间隔: {config.MEMORY_UPDATE_INTERVAL}")
    print(f"   当前轮数: {agent.memory_update_mechanism.current_round}")
    
    # 测试对话内容 - 设计为能触发长期记忆更新的内容
    test_conversations = [
        "你好，我叫张小明",
        "我今年28岁，是一名软件工程师",
        "我在北京工作，住在朝阳区",
        "我喜欢编程、读书和旅行",
        "我有一个女朋友叫小红，我们在一起3年了",
        "我最喜欢的颜色是蓝色",
        "我喜欢吃火锅和川菜",
        "我有一只猫叫咪咪，是橘色的",
        "我最近在学习人工智能",
        "我的梦想是环游世界"
    ]
    
    print(f"\n💬 开始{len(test_conversations)}轮对话测试:")
    print("-" * 50)
    
    for i, user_input in enumerate(test_conversations, 1):
        print(f"\n🔄 第{i}轮对话:")
        print(f"   用户: {user_input}")
        
        # 检查是否应该触发记忆更新
        should_update = agent.memory_update_mechanism.should_trigger_update()
        print(f"   ⏰ 是否触发记忆更新: {should_update}")
        
        # 进行对话
        response = agent.chat(user_input)
        print(f"   小王子: {response[:80]}...")
        
        # 获取记忆状态
        stats = agent.memory_room.get_memory_stats()
        print(f"   📊 记忆状态:")
        print(f"      短期记忆: {stats['short_term_count']} 轮")
        print(f"      长期记忆事实: {stats['long_term_factual_count']} 项")
        print(f"      长期记忆情节: {stats['long_term_episodic_count']} 项")
        print(f"      当前轮数: {agent.memory_update_mechanism.current_round}")
        
        # 如果触发了记忆更新，显示详细信息
        if should_update:
            print(f"   🎉 记忆更新已触发！")
            
            # 获取长期记忆内容
            long_term = agent.memory_room.get_long_term_memory()
            print(f"   📝 长期记忆内容:")
            print(f"      事实记忆: {long_term.get('factual', {})}")
            print(f"      情节记忆: {len(long_term.get('episodic', []))} 项")
            print(f"      语义记忆: {long_term.get('semantic', {})}")
    
    # 最终检查
    print(f"\n🎯 测试完成！最终状态:")
    print("-" * 50)
    
    final_stats = agent.memory_room.get_memory_stats()
    print(f"   短期记忆: {final_stats['short_term_count']} 轮")
    print(f"   长期记忆事实: {final_stats['long_term_factual_count']} 项")
    print(f"   长期记忆情节: {final_stats['long_term_episodic_count']} 项")
    print(f"   当前轮数: {agent.memory_update_mechanism.current_round}")
    
    # 获取长期记忆详情
    long_term = agent.memory_room.get_long_term_memory()
    print(f"\n📋 长期记忆详情:")
    print(f"   事实记忆: {long_term.get('factual', {})}")
    print(f"   情节记忆: {long_term.get('episodic', [])}")
    print(f"   语义记忆: {long_term.get('semantic', {})}")
    
    # 获取记忆更新历史
    history = agent.memory_room.get_memory_updates_history()
    print(f"\n📜 记忆更新历史: {len(history)} 条记录")
    for i, record in enumerate(history, 1):
        print(f"   记录{i}: {record.get('timestamp', 'N/A')}")


if __name__ == "__main__":
    test_long_term_memory()

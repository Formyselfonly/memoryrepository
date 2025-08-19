#!/usr/bin/env python3
"""
记忆更新修复测试脚本
"""

import os
import sys
from loguru import logger

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import Config
from core.agent import LittlePrinceAgent


def test_memory_fix():
    """测试记忆更新修复"""
    print("🔧 记忆更新修复测试")
    print("=" * 50)
    
    # 初始化配置和Agent
    config = Config()
    agent = LittlePrinceAgent(config, "test_user_fix")
    
    print(f"📋 配置信息:")
    print(f"   短期记忆最大轮数: {config.SHORT_TERM_MAX_ROUNDS}")
    print(f"   记忆更新间隔: {config.MEMORY_UPDATE_INTERVAL}")
    
    # 测试对话内容
    test_conversations = [
        "你好，我叫李小明",
        "我今年30岁，是一名设计师",
        "我在上海工作，住在浦东新区",
        "我喜欢画画、摄影和旅行",
        "我有一只狗叫旺财，是金毛",
        "我最喜欢的颜色是绿色",
        "我喜欢吃日料和意大利面",
        "我最近在学习3D建模",
        "我的梦想是开一家艺术工作室",
        "我想去日本旅行"
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
        print(f"   小王子: {response[:60]}...")
        
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


if __name__ == "__main__":
    test_memory_fix()

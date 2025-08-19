#!/usr/bin/env python3
"""
记忆配置对比测试脚本
"""

import os
import sys
from loguru import logger

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import Config
from core.agent import LittlePrinceAgent


def test_config(config_name: str, short_term_rounds: int, update_interval: int):
    """测试特定配置"""
    print(f"\n🔧 测试配置: {config_name}")
    print(f"   短期记忆最大轮数: {short_term_rounds}")
    print(f"   记忆更新间隔: {update_interval}")
    print("-" * 50)
    
    # 创建临时配置
    class TempConfig:
        def __init__(self, short_term, update_interval):
            self.SHORT_TERM_MAX_ROUNDS = short_term
            self.MEMORY_UPDATE_INTERVAL = update_interval
            self.LLM_PROVIDER = "openai"
            self.LLM_MODEL = "gpt-4o-mini"
            self.LLM_API_KEY = os.getenv("LLM_API_KEY")
            self.TEMPERATURE = 0.7
    
    config = TempConfig(short_term_rounds, update_interval)
    agent = LittlePrinceAgent(config, f"test_user_{config_name}")
    
    # 测试对话
    test_conversations = [
        "你好，我叫测试用户",
        "我今年25岁",
        "我喜欢编程",
        "我在北京工作",
        "我有一只猫"
    ]
    
    for i, user_input in enumerate(test_conversations, 1):
        print(f"   第{i}轮: {user_input}")
        
        # 检查是否触发更新
        should_update = agent.memory_update_mechanism.should_trigger_update()
        if should_update:
            print(f"   ⏰ 第{i}轮触发记忆更新！")
        
        # 进行对话
        response = agent.chat(user_input)
        
        # 获取状态
        stats = agent.memory_room.get_memory_stats()
        print(f"   短期记忆: {stats['short_term_count']} 轮, 长期记忆: {stats['long_term_factual_count']} 项")
    
    # 最终状态
    final_stats = agent.memory_room.get_memory_stats()
    print(f"\n   📊 最终状态:")
    print(f"      短期记忆: {final_stats['short_term_count']} 轮")
    print(f"      长期记忆事实: {final_stats['long_term_factual_count']} 项")
    print(f"      长期记忆情节: {final_stats['long_term_episodic_count']} 项")
    
    return final_stats


def main():
    """主函数"""
    print("📊 记忆配置对比测试")
    print("=" * 60)
    
    # 测试不同配置
    configs = [
        ("快速测试", 5, 5),
        ("平衡配置", 10, 10),
        ("长对话", 15, 15)
    ]
    
    results = {}
    
    for config_name, short_term, update_interval in configs:
        try:
            result = test_config(config_name, short_term, update_interval)
            results[config_name] = result
        except Exception as e:
            print(f"❌ 配置 {config_name} 测试失败: {e}")
    
    # 总结对比
    print(f"\n🎯 配置对比总结")
    print("=" * 60)
    
    for config_name, result in results.items():
        print(f"\n{config_name}:")
        print(f"   短期记忆: {result['short_term_count']} 轮")
        print(f"   长期记忆事实: {result['long_term_factual_count']} 项")
        print(f"   长期记忆情节: {result['long_term_episodic_count']} 项")


if __name__ == "__main__":
    main()

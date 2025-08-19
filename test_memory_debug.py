#!/usr/bin/env python3
"""
记忆系统调试脚本 - 诊断长期记忆问题
"""

import os
import sys
from loguru import logger

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import Config
from core.agent import LittlePrinceAgent
from core.memory.memory_room import MemoryRoom


def test_memory_system():
    """测试记忆系统"""
    print("🔍 记忆系统调试工具")
    print("=" * 50)
    
    # 1. 检查配置
    print("\n📋 1. 检查配置")
    print("-" * 30)
    try:
        config = Config()
        print(f"✅ 配置加载成功")
        print(f"   SHORT_TERM_MAX_ROUNDS: {config.SHORT_TERM_MAX_ROUNDS}")
        print(f"   MEMORY_UPDATE_INTERVAL: {config.MEMORY_UPDATE_INTERVAL}")
        print(f"   LLM_PROVIDER: {config.LLM_PROVIDER}")
        print(f"   LLM_MODEL: {config.LLM_MODEL}")
        print(f"   API_KEY设置: {'✅' if config.LLM_API_KEY else '❌'}")
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return
    
    # 2. 测试记忆房间
    print("\n🏠 2. 测试记忆房间")
    print("-" * 30)
    try:
        memory_room = MemoryRoom(config, "test_user_123")
        print(f"✅ 记忆房间初始化成功")
        
        # 检查数据库连接
        db_info = memory_room.get_database_info()
        print(f"   数据库路径: {db_info['db_path']}")
        print(f"   用户ID: {db_info['user_id']}")
        print(f"   最大短期记忆轮数: {db_info['max_short_term_rounds']}")
        
        # 检查初始记忆状态
        stats = memory_room.get_memory_stats()
        print(f"   初始记忆统计: {stats}")
        
    except Exception as e:
        print(f"❌ 记忆房间初始化失败: {e}")
        return
    
    # 3. 测试Agent初始化
    print("\n🤖 3. 测试Agent初始化")
    print("-" * 30)
    try:
        agent = LittlePrinceAgent(config, "test_user_123")
        print(f"✅ Agent初始化成功")
        
        # 检查记忆更新机制
        update_mechanism = agent.memory_update_mechanism
        print(f"   当前轮数: {update_mechanism.current_round}")
        print(f"   更新间隔: {update_mechanism.config.MEMORY_UPDATE_INTERVAL}")
        print(f"   是否应该触发更新: {update_mechanism.should_trigger_update()}")
        
    except Exception as e:
        print(f"❌ Agent初始化失败: {e}")
        return
    
    # 4. 模拟对话测试
    print("\n💬 4. 模拟对话测试")
    print("-" * 30)
    
    test_conversations = [
        "你好，我叫小明",
        "我喜欢看星星",
        "我今年25岁",
        "我在北京工作",
        "我喜欢吃苹果"
    ]
    
    for i, user_input in enumerate(test_conversations, 1):
        print(f"\n   第{i}轮对话:")
        print(f"   用户: {user_input}")
        
        try:
            response = agent.chat(user_input)
            print(f"   小王子: {response[:100]}...")
            
            # 检查记忆状态
            stats = agent.memory_room.get_memory_stats()
            print(f"   短期记忆: {stats['short_term_count']} 轮")
            print(f"   长期记忆事实: {stats['long_term_factual_count']} 项")
            print(f"   长期记忆情节: {stats['long_term_episodic_count']} 项")
            print(f"   当前轮数: {agent.memory_update_mechanism.current_round}")
            print(f"   是否触发更新: {agent.memory_update_mechanism.should_trigger_update()}")
            
        except Exception as e:
            print(f"   ❌ 对话失败: {e}")
    
    # 5. 检查最终记忆状态
    print("\n📊 5. 最终记忆状态")
    print("-" * 30)
    
    try:
        # 获取短期记忆
        short_term = agent.memory_room.get_short_term_memory()
        print(f"   短期记忆数量: {len(short_term)}")
        if short_term:
            print(f"   最新短期记忆: {short_term[-1]}")
        
        # 获取长期记忆
        long_term = agent.memory_room.get_long_term_memory()
        print(f"   长期记忆事实: {long_term.get('factual', {})}")
        print(f"   长期记忆情节: {len(long_term.get('episodic', []))} 项")
        print(f"   长期记忆语义: {long_term.get('semantic', {})}")
        
        # 获取记忆更新历史
        history = agent.memory_room.get_memory_updates_history()
        print(f"   记忆更新历史: {len(history)} 条记录")
        
    except Exception as e:
        print(f"   ❌ 获取记忆状态失败: {e}")
    
    print("\n🎯 调试完成！")


def check_env_file():
    """检查环境变量文件"""
    print("\n🔧 检查环境变量文件")
    print("-" * 30)
    
    env_files = ['.env', 'env.example']
    
    for env_file in env_files:
        if os.path.exists(env_file):
            print(f"✅ 找到 {env_file}")
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    # 检查关键配置
                    configs = {
                        'SHORT_TERM_MAX_ROUNDS': None,
                        'MEMORY_UPDATE_INTERVAL': None,
                        'LLM_API_KEY': None
                    }
                    
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if '=' in line:
                                key, value = line.split('=', 1)
                                if key in configs:
                                    configs[key] = value
                    
                    print(f"   {env_file} 配置:")
                    for key, value in configs.items():
                        if key == 'LLM_API_KEY':
                            status = '✅ 已设置' if value and value != 'your_openai_api_key_here' else '❌ 未设置'
                            print(f"     {key}: {status}")
                        else:
                            print(f"     {key}: {value or '未设置'}")
                            
            except Exception as e:
                print(f"   ❌ 读取 {env_file} 失败: {e}")
        else:
            print(f"❌ 未找到 {env_file}")


if __name__ == "__main__":
    check_env_file()
    test_memory_system()

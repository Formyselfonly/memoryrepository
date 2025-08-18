#!/usr/bin/env python3
"""
测试记忆持久化功能
验证记忆数据能够正确保存和加载
"""

import os
import sys
import json
import shutil
from dotenv import load_dotenv

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from core import LittlePrinceAgent


def test_memory_persistence():
    """测试记忆持久化功能"""
    print("🧪 测试记忆持久化功能...")
    
    # 设置测试API密钥
    os.environ["LLM_API_KEY"] = "test_key_for_persistence_test"
    
    try:
        # 1. 清理测试数据
        print("1. 清理测试数据...")
        test_memory_dir = "data/memory"
        if os.path.exists(test_memory_dir):
            shutil.rmtree(test_memory_dir)
        print("   ✅ 测试数据已清理")
        
        # 2. 创建Agent并添加对话
        print("2. 创建Agent并添加对话...")
        config = Config()
        agent = LittlePrinceAgent(config)
        
        # 添加一些测试对话
        test_conversations = [
            ("你好，我叫小明", "你好小明！很高兴认识你！"),
            ("我喜欢看星星", "哇！我也喜欢看星星呢！"),
            ("我今年25岁", "25岁，正是美好的年纪！"),
            ("我是一名程序员", "程序员！你一定很聪明！"),
            ("我喜欢吃苹果", "苹果很健康呢！我也喜欢！")
        ]
        
        for user_input, ai_response in test_conversations:
            agent.memory_room.add_conversation(user_input, ai_response)
        
        print(f"   ✅ 添加了 {len(test_conversations)} 轮对话")
        
        # 3. 检查记忆文件是否创建
        print("3. 检查记忆文件...")
        short_term_file = os.path.join(test_memory_dir, "short_term_memory.json")
        long_term_file = os.path.join(test_memory_dir, "long_term_memory.json")
        
        if os.path.exists(short_term_file):
            print("   ✅ 短期记忆文件已创建")
        else:
            print("   ❌ 短期记忆文件未创建")
            return False
        
        if os.path.exists(long_term_file):
            print("   ✅ 长期记忆文件已创建")
        else:
            print("   ❌ 长期记忆文件未创建")
            return False
        
        # 4. 检查文件内容
        print("4. 检查文件内容...")
        with open(short_term_file, 'r', encoding='utf-8') as f:
            short_term_data = json.load(f)
            conversations = short_term_data.get('conversations', [])
            print(f"   ✅ 短期记忆文件包含 {len(conversations)} 轮对话")
        
        with open(long_term_file, 'r', encoding='utf-8') as f:
            long_term_data = json.load(f)
            memory = long_term_data.get('memory', {})
            print(f"   ✅ 长期记忆文件已创建，包含 {len(memory)} 个记忆类型")
        
        # 5. 测试记忆加载
        print("5. 测试记忆加载...")
        # 创建新的Agent实例，应该能加载之前的记忆
        new_agent = LittlePrinceAgent(config)
        
        # 检查是否加载了之前的记忆
        stats = new_agent.get_memory_stats()
        if stats['short_term_count'] == len(test_conversations):
            print("   ✅ 短期记忆加载成功")
        else:
            print(f"   ❌ 短期记忆加载失败，期望 {len(test_conversations)}，实际 {stats['short_term_count']}")
            return False
        
        # 6. 测试记忆导出
        print("6. 测试记忆导出...")
        export_path = new_agent.memory_room.export_memory()
        if export_path and os.path.exists(export_path):
            print(f"   ✅ 记忆导出成功: {export_path}")
            
            # 检查导出文件内容
            with open(export_path, 'r', encoding='utf-8') as f:
                export_data = json.load(f)
                short_term_count = export_data.get('short_term_memory', {}).get('count', 0)
                if short_term_count == len(test_conversations):
                    print("   ✅ 导出文件内容正确")
                else:
                    print(f"   ❌ 导出文件内容错误，期望 {len(test_conversations)}，实际 {short_term_count}")
                    return False
        else:
            print("   ❌ 记忆导出失败")
            return False
        
        # 7. 测试记忆清空
        print("7. 测试记忆清空...")
        new_agent.memory_room.clear_all_memory()
        
        # 检查文件是否被清空
        with open(short_term_file, 'r', encoding='utf-8') as f:
            short_term_data = json.load(f)
            conversations = short_term_data.get('conversations', [])
            if len(conversations) == 0:
                print("   ✅ 记忆清空成功")
            else:
                print(f"   ❌ 记忆清空失败，仍有 {len(conversations)} 轮对话")
                return False
        
        print("\n🎉 记忆持久化测试全部通过！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_memory_file_structure():
    """测试记忆文件结构"""
    print("\n📁 测试记忆文件结构...")
    
    try:
        # 检查文件结构
        test_memory_dir = "data/memory"
        short_term_file = os.path.join(test_memory_dir, "short_term_memory.json")
        long_term_file = os.path.join(test_memory_dir, "long_term_memory.json")
        
        if os.path.exists(short_term_file):
            with open(short_term_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print("📄 短期记忆文件结构:")
                print(f"   - conversations: {len(data.get('conversations', []))} 轮")
                print(f"   - last_updated: {data.get('last_updated', 'N/A')}")
        
        if os.path.exists(long_term_file):
            with open(long_term_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                memory = data.get('memory', {})
                print("📄 长期记忆文件结构:")
                print(f"   - factual: {len(memory.get('factual', {}))} 项")
                print(f"   - episodic: {len(memory.get('episodic', []))} 项")
                print(f"   - semantic: {len(memory.get('semantic', {}))} 项")
                print(f"   - last_updated: {data.get('last_updated', 'N/A')}")
        
        print("✅ 文件结构检查完成")
        
    except Exception as e:
        print(f"❌ 文件结构检查失败: {e}")


if __name__ == "__main__":
    print("🔧 开始记忆持久化测试...")
    load_dotenv()
    
    success = test_memory_persistence()
    if success:
        test_memory_file_structure()
        print("\n🎉 所有测试通过！记忆持久化功能正常！")
    else:
        print("\n❌ 测试失败，需要检查代码")

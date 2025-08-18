#!/usr/bin/env python3
"""
测试SQLite记忆存储功能
验证记忆数据能够正确保存到SQLite数据库
"""

import os
import sys
import sqlite3
from dotenv import load_dotenv

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from core import LittlePrinceAgent


def test_sqlite_memory_storage():
    """测试SQLite记忆存储功能"""
    print("🧪 测试SQLite记忆存储功能...")
    
    # 设置测试API密钥
    os.environ["LLM_API_KEY"] = "test_key_for_sqlite_test"
    
    try:
        # 1. 清理测试数据库
        print("1. 清理测试数据库...")
        test_db_path = "data/memory.db"
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
        print("   ✅ 测试数据库已清理")
        
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
        
        # 3. 检查数据库文件是否创建
        print("3. 检查数据库文件...")
        if os.path.exists(test_db_path):
            file_size = os.path.getsize(test_db_path)
            print(f"   ✅ 数据库文件已创建 ({file_size} 字节)")
        else:
            print("   ❌ 数据库文件未创建")
            return False
        
        # 4. 检查数据库表结构
        print("4. 检查数据库表结构...")
        with sqlite3.connect(test_db_path) as conn:
            cursor = conn.cursor()
            
            # 检查表是否存在
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = ['short_term_memory', 'long_term_memory', 'memory_updates']
            for table in expected_tables:
                if table in tables:
                    print(f"   ✅ 表 {table} 存在")
                else:
                    print(f"   ❌ 表 {table} 不存在")
                    return False
            
            # 检查短期记忆数据
            cursor.execute("SELECT COUNT(*) FROM short_term_memory")
            short_term_count = cursor.fetchone()[0]
            print(f"   ✅ 短期记忆表包含 {short_term_count} 条记录")
            
            # 检查长期记忆数据
            cursor.execute("SELECT COUNT(*) FROM long_term_memory")
            long_term_count = cursor.fetchone()[0]
            print(f"   ✅ 长期记忆表包含 {long_term_count} 条记录")
            
            # 检查更新记录
            cursor.execute("SELECT COUNT(*) FROM memory_updates")
            updates_count = cursor.fetchone()[0]
            print(f"   ✅ 更新记录表包含 {updates_count} 条记录")
        
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
        else:
            print("   ❌ 记忆导出失败")
            return False
        
        # 7. 测试记忆更新历史
        print("7. 测试记忆更新历史...")
        updates = new_agent.memory_room.get_memory_updates_history(limit=10)
        if updates:
            print(f"   ✅ 获取到 {len(updates)} 条更新记录")
            for update in updates[:3]:  # 显示前3条
                print(f"     - {update['update_type']}: {update['description']}")
        else:
            print("   ❌ 未获取到更新记录")
            return False
        
        # 8. 测试记忆清空
        print("8. 测试记忆清空...")
        new_agent.memory_room.clear_all_memory()
        
        # 检查数据库是否被清空
        with sqlite3.connect(test_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM short_term_memory")
            short_term_count = cursor.fetchone()[0]
            
            if short_term_count == 0:
                print("   ✅ 记忆清空成功")
            else:
                print(f"   ❌ 记忆清空失败，仍有 {short_term_count} 条短期记忆")
                return False
        
        print("\n🎉 SQLite记忆存储测试全部通过！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database_operations():
    """测试数据库操作"""
    print("\n🔧 测试数据库操作...")
    
    try:
        test_db_path = "data/memory.db"
        
        with sqlite3.connect(test_db_path) as conn:
            cursor = conn.cursor()
            
            # 测试查询操作
            print("📊 数据库统计信息:")
            
            # 短期记忆统计
            cursor.execute("SELECT COUNT(*) FROM short_term_memory")
            short_term_count = cursor.fetchone()[0]
            print(f"   • 短期记忆: {short_term_count} 条")
            
            # 长期记忆统计
            cursor.execute("SELECT memory_type, COUNT(*) FROM long_term_memory GROUP BY memory_type")
            long_term_stats = cursor.fetchall()
            for memory_type, count in long_term_stats:
                print(f"   • {memory_type} 记忆: {count} 条")
            
            # 更新记录统计
            cursor.execute("SELECT update_type, COUNT(*) FROM memory_updates GROUP BY update_type")
            update_stats = cursor.fetchall()
            for update_type, count in update_stats:
                print(f"   • {update_type}: {count} 次")
            
            # 显示最近的更新记录
            print("\n📝 最近的更新记录:")
            cursor.execute('''
                SELECT update_type, description, created_at
                FROM memory_updates
                ORDER BY created_at DESC
                LIMIT 5
            ''')
            
            for row in cursor.fetchall():
                update_type, description, created_at = row
                print(f"   • {update_type}: {description}")
                print(f"     时间: {created_at}")
        
        print("✅ 数据库操作测试完成")
        
    except Exception as e:
        print(f"❌ 数据库操作测试失败: {e}")


if __name__ == "__main__":
    print("🔧 开始SQLite记忆存储测试...")
    load_dotenv()
    
    success = test_sqlite_memory_storage()
    if success:
        test_database_operations()
        print("\n🎉 所有测试通过！SQLite记忆存储功能正常！")
    else:
        print("\n❌ 测试失败，需要检查代码")

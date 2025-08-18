#!/usr/bin/env python3
"""
测试用户管理功能
验证用户登录、数据隔离等功能
"""

import os
import sys
import sqlite3
from dotenv import load_dotenv

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from core import LittlePrinceAgent
from core.user_manager import UserManager


def test_user_management():
    """测试用户管理功能"""
    print("🧪 测试用户管理功能...")
    
    # 设置测试API密钥
    os.environ["LLM_API_KEY"] = "test_key_for_user_management"
    
    try:
        # 1. 清理测试数据库
        print("1. 清理测试数据库...")
        test_users_db = "data/users.db"
        test_memory_db = "data/memory.db"
        
        for db_file in [test_users_db, test_memory_db]:
            if os.path.exists(db_file):
                os.remove(db_file)
                print(f"   ✅ 已删除: {db_file}")
        
        # 2. 初始化用户管理器
        print("2. 初始化用户管理器...")
        user_manager = UserManager()
        print("   ✅ 用户管理器初始化完成")
        
        # 3. 测试用户注册和登录
        print("3. 测试用户注册和登录...")
        
        # 测试新用户注册
        login_result1 = user_manager.login_user("小明")
        if login_result1['user_id'] and login_result1['is_new_user']:
            print(f"   ✅ 新用户注册成功: {login_result1['username']} (ID: {login_result1['user_id'][:8]}...)")
            user1_id = login_result1['user_id']
        else:
            print("   ❌ 新用户注册失败")
            return False
        
        # 测试用户再次登录
        login_result2 = user_manager.login_user("小明")
        if login_result2['user_id'] and not login_result2['is_new_user']:
            print(f"   ✅ 用户再次登录成功: {login_result2['username']} (登录次数: {login_result2['login_count']})")
        else:
            print("   ❌ 用户再次登录失败")
            return False
        
        # 测试另一个用户注册
        login_result3 = user_manager.login_user("小红")
        if login_result3['user_id'] and login_result3['is_new_user']:
            print(f"   ✅ 第二个用户注册成功: {login_result3['username']} (ID: {login_result3['user_id'][:8]}...)")
            user2_id = login_result3['user_id']
        else:
            print("   ❌ 第二个用户注册失败")
            return False
        
        # 4. 测试用户数据隔离
        print("4. 测试用户数据隔离...")
        
        # 创建两个Agent实例
        config = Config()
        agent1 = LittlePrinceAgent(config, user1_id)
        agent2 = LittlePrinceAgent(config, user2_id)
        
        # 为两个用户添加不同的对话
        test_conversations1 = [
            ("你好，我叫小明", "你好小明！很高兴认识你！"),
            ("我喜欢看星星", "哇！我也喜欢看星星呢！"),
            ("我今年25岁", "25岁，正是美好的年纪！")
        ]
        
        test_conversations2 = [
            ("你好，我叫小红", "你好小红！很高兴认识你！"),
            ("我喜欢画画", "画画很有趣呢！我也喜欢！"),
            ("我是一名学生", "学生时代很美好呢！")
        ]
        
        # 添加对话到用户1
        for user_input, ai_response in test_conversations1:
            agent1.memory_room.add_conversation(user_input, ai_response)
        print(f"   ✅ 用户1添加了 {len(test_conversations1)} 轮对话")
        
        # 添加对话到用户2
        for user_input, ai_response in test_conversations2:
            agent2.memory_room.add_conversation(user_input, ai_response)
        print(f"   ✅ 用户2添加了 {len(test_conversations2)} 轮对话")
        
        # 检查数据隔离
        stats1 = agent1.get_memory_stats()
        stats2 = agent2.get_memory_stats()
        
        if stats1['short_term_count'] == len(test_conversations1) and stats2['short_term_count'] == len(test_conversations2):
            print("   ✅ 用户数据隔离正常")
        else:
            print(f"   ❌ 用户数据隔离失败，用户1: {stats1['short_term_count']}，用户2: {stats2['short_term_count']}")
            return False
        
        # 5. 测试用户信息获取
        print("5. 测试用户信息获取...")
        
        user1_info = user_manager.get_user_info(user1_id)
        user2_info = user_manager.get_user_info(user2_id)
        
        if user1_info and user2_info:
            print(f"   ✅ 用户1信息: {user1_info['username']} (创建时间: {user1_info['created_at']})")
            print(f"   ✅ 用户2信息: {user2_info['username']} (创建时间: {user2_info['created_at']})")
        else:
            print("   ❌ 获取用户信息失败")
            return False
        
        # 6. 测试用户统计
        print("6. 测试用户统计...")
        
        user_stats = user_manager.get_user_stats()
        print(f"   ✅ 总用户数: {user_stats['total_users']}")
        print(f"   ✅ 今日新增: {user_stats['new_users_today']}")
        print(f"   ✅ 今日活跃: {user_stats['active_users_today']}")
        print(f"   ✅ 在线用户: {user_stats['online_users']}")
        
        if user_stats['total_users'] == 2:
            print("   ✅ 用户统计正确")
        else:
            print("   ❌ 用户统计错误")
            return False
        
        # 7. 测试记忆导出
        print("7. 测试记忆导出...")
        
        export_path1 = agent1.memory_room.export_memory()
        export_path2 = agent2.memory_room.export_memory()
        
        if export_path1 and export_path2 and os.path.exists(export_path1) and os.path.exists(export_path2):
            print(f"   ✅ 用户1记忆导出: {os.path.basename(export_path1)}")
            print(f"   ✅ 用户2记忆导出: {os.path.basename(export_path2)}")
        else:
            print("   ❌ 记忆导出失败")
            return False
        
        # 8. 测试用户会话管理
        print("8. 测试用户会话管理...")
        
        # 结束用户会话
        if user_manager.end_user_session(user1_id):
            print("   ✅ 用户会话结束成功")
        else:
            print("   ❌ 用户会话结束失败")
            return False
        
        # 9. 测试数据库结构
        print("9. 测试数据库结构...")
        
        # 检查用户数据库
        with sqlite3.connect(test_users_db) as conn:
            cursor = conn.cursor()
            
            # 检查用户表
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"   ✅ 用户表包含 {user_count} 条记录")
            
            # 检查会话表
            cursor.execute("SELECT COUNT(*) FROM user_sessions")
            session_count = cursor.fetchone()[0]
            print(f"   ✅ 会话表包含 {session_count} 条记录")
        
        # 检查记忆数据库
        with sqlite3.connect(test_memory_db) as conn:
            cursor = conn.cursor()
            
            # 检查短期记忆表
            cursor.execute("SELECT user_id, COUNT(*) FROM short_term_memory GROUP BY user_id")
            memory_stats = cursor.fetchall()
            print("   ✅ 短期记忆分布:")
            for user_id, count in memory_stats:
                print(f"      - 用户 {user_id[:8]}...: {count} 条")
        
        print("\n🎉 用户管理功能测试全部通过！")
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
        test_users_db = "data/users.db"
        test_memory_db = "data/memory.db"
        
        # 检查用户数据库
        print("📊 用户数据库统计:")
        with sqlite3.connect(test_users_db) as conn:
            cursor = conn.cursor()
            
            # 用户统计
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"   • 总用户数: {user_count}")
            
            # 会话统计
            cursor.execute("SELECT COUNT(*) FROM user_sessions")
            session_count = cursor.fetchone()[0]
            print(f"   • 总会话数: {session_count}")
            
            # 显示用户列表
            print("\n👥 用户列表:")
            cursor.execute('''
                SELECT username, created_at, last_login, login_count
                FROM users
                ORDER BY created_at DESC
            ''')
            
            for row in cursor.fetchall():
                username, created_at, last_login, login_count = row
                print(f"   • {username}: 登录 {login_count} 次，最后登录 {last_login}")
        
        # 检查记忆数据库
        print("\n📊 记忆数据库统计:")
        with sqlite3.connect(test_memory_db) as conn:
            cursor = conn.cursor()
            
            # 短期记忆统计
            cursor.execute("SELECT user_id, COUNT(*) FROM short_term_memory GROUP BY user_id")
            short_term_stats = cursor.fetchall()
            print("   • 短期记忆分布:")
            for user_id, count in short_term_stats:
                print(f"     - 用户 {user_id[:8]}...: {count} 条")
            
            # 长期记忆统计
            cursor.execute("SELECT user_id, memory_type, COUNT(*) FROM long_term_memory GROUP BY user_id, memory_type")
            long_term_stats = cursor.fetchall()
            print("   • 长期记忆分布:")
            for user_id, memory_type, count in long_term_stats:
                print(f"     - 用户 {user_id[:8]}... {memory_type}: {count} 条")
        
        print("✅ 数据库操作测试完成")
        
    except Exception as e:
        print(f"❌ 数据库操作测试失败: {e}")


if __name__ == "__main__":
    print("🔧 开始用户管理功能测试...")
    load_dotenv()
    
    success = test_user_management()
    if success:
        test_database_operations()
        print("\n🎉 所有测试通过！用户管理功能正常！")
    else:
        print("\n❌ 测试失败，需要检查代码")

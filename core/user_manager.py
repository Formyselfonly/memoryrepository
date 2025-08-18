import sqlite3
import os
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from loguru import logger


class UserManager:
    """用户管理类 - 处理用户登录和数据绑定"""
    
    def __init__(self, db_path: str = "data/users.db"):
        self.db_path = db_path
        self.ensure_db_directory()
        self.init_database()
    
    def ensure_db_directory(self):
        """确保数据库目录存在"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
    
    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """初始化用户数据库表结构"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 创建用户表
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id TEXT PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                        last_login TEXT DEFAULT CURRENT_TIMESTAMP,
                        login_count INTEGER DEFAULT 1
                    )
                ''')
                
                # 创建用户会话表
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        session_start TEXT DEFAULT CURRENT_TIMESTAMP,
                        session_end TEXT,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')
                
                # 创建索引
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON user_sessions(user_id)')
                
                conn.commit()
                logger.info("用户数据库表结构初始化完成")
                
        except Exception as e:
            logger.error(f"初始化用户数据库失败: {e}")
            raise
    
    def login_user(self, username: str) -> Dict[str, Any]:
        """用户登录，如果用户不存在则创建新用户"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 检查用户是否已存在
                cursor.execute('SELECT id, username, login_count FROM users WHERE username = ?', (username,))
                existing_user = cursor.fetchone()
                
                if existing_user:
                    # 用户已存在，更新登录信息
                    user_id, existing_username, login_count = existing_user
                    
                    cursor.execute('''
                        UPDATE users 
                        SET last_login = CURRENT_TIMESTAMP, login_count = login_count + 1
                        WHERE id = ?
                    ''', (user_id,))
                    
                    # 记录会话开始
                    cursor.execute('''
                        INSERT INTO user_sessions (user_id, session_start)
                        VALUES (?, CURRENT_TIMESTAMP)
                    ''', (user_id,))
                    
                    conn.commit()
                    
                    logger.info(f"用户登录成功: {username} (ID: {user_id})")
                    
                    return {
                        'user_id': user_id,
                        'username': existing_username,
                        'is_new_user': False,
                        'login_count': login_count + 1,
                        'message': f"欢迎回来，{existing_username}！"
                    }
                else:
                    # 创建新用户
                    user_id = str(uuid.uuid4())
                    
                    cursor.execute('''
                        INSERT INTO users (id, username, created_at, last_login)
                        VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                    ''', (user_id, username))
                    
                    # 记录会话开始
                    cursor.execute('''
                        INSERT INTO user_sessions (user_id, session_start)
                        VALUES (?, CURRENT_TIMESTAMP)
                    ''', (user_id,))
                    
                    conn.commit()
                    
                    logger.info(f"新用户注册成功: {username} (ID: {user_id})")
                    
                    return {
                        'user_id': user_id,
                        'username': username,
                        'is_new_user': True,
                        'login_count': 1,
                        'message': f"欢迎新朋友，{username}！"
                    }
                
        except Exception as e:
            logger.error(f"用户登录失败: {e}")
            return {
                'user_id': None,
                'username': username,
                'is_new_user': False,
                'login_count': 0,
                'message': f"登录失败: {str(e)}"
            }
    
    def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """获取用户信息"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT id, username, created_at, last_login, login_count
                    FROM users WHERE id = ?
                ''', (user_id,))
                
                user_data = cursor.fetchone()
                
                if user_data:
                    return {
                        'user_id': user_data[0],
                        'username': user_data[1],
                        'created_at': user_data[2],
                        'last_login': user_data[3],
                        'login_count': user_data[4]
                    }
                else:
                    return None
                
        except Exception as e:
            logger.error(f"获取用户信息失败: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """根据用户名获取用户信息"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT id, username, created_at, last_login, login_count
                    FROM users WHERE username = ?
                ''', (username,))
                
                user_data = cursor.fetchone()
                
                if user_data:
                    return {
                        'user_id': user_data[0],
                        'username': user_data[1],
                        'created_at': user_data[2],
                        'last_login': user_data[3],
                        'login_count': user_data[4]
                    }
                else:
                    return None
                
        except Exception as e:
            logger.error(f"根据用户名获取用户信息失败: {e}")
            return None
    
    def end_user_session(self, user_id: str) -> bool:
        """结束用户会话"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE user_sessions 
                    SET session_end = CURRENT_TIMESTAMP
                    WHERE user_id = ? AND session_end IS NULL
                ''', (user_id,))
                
                conn.commit()
                logger.info(f"用户会话已结束: {user_id}")
                return True
                
        except Exception as e:
            logger.error(f"结束用户会话失败: {e}")
            return False
    
    def get_all_users(self) -> list:
        """获取所有用户列表"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT id, username, created_at, last_login, login_count
                    FROM users
                    ORDER BY created_at DESC
                ''')
                
                users = []
                for row in cursor.fetchall():
                    users.append({
                        'user_id': row[0],
                        'username': row[1],
                        'created_at': row[2],
                        'last_login': row[3],
                        'login_count': row[4]
                    })
                
                return users
                
        except Exception as e:
            logger.error(f"获取用户列表失败: {e}")
            return []
    
    def delete_user(self, user_id: str) -> bool:
        """删除用户"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 删除用户会话记录
                cursor.execute('DELETE FROM user_sessions WHERE user_id = ?', (user_id,))
                
                # 删除用户
                cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
                
                conn.commit()
                logger.info(f"用户已删除: {user_id}")
                return True
                
        except Exception as e:
            logger.error(f"删除用户失败: {e}")
            return False
    
    def get_user_stats(self) -> Dict[str, Any]:
        """获取用户统计信息"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 总用户数
                cursor.execute('SELECT COUNT(*) FROM users')
                total_users = cursor.fetchone()[0]
                
                # 今日新增用户
                cursor.execute('''
                    SELECT COUNT(*) FROM users 
                    WHERE DATE(created_at) = DATE('now')
                ''')
                new_users_today = cursor.fetchone()[0]
                
                # 今日活跃用户
                cursor.execute('''
                    SELECT COUNT(*) FROM users 
                    WHERE DATE(last_login) = DATE('now')
                ''')
                active_users_today = cursor.fetchone()[0]
                
                # 在线用户数（有未结束会话的用户）
                cursor.execute('''
                    SELECT COUNT(DISTINCT user_id) FROM user_sessions 
                    WHERE session_end IS NULL
                ''')
                online_users = cursor.fetchone()[0]
                
                return {
                    'total_users': total_users,
                    'new_users_today': new_users_today,
                    'active_users_today': active_users_today,
                    'online_users': online_users
                }
                
        except Exception as e:
            logger.error(f"获取用户统计失败: {e}")
            return {
                'total_users': 0,
                'new_users_today': 0,
                'active_users_today': 0,
                'online_users': 0
            }
    
    def get_data_privacy_info(self) -> Dict[str, Any]:
        """获取数据隐私信息"""
        return {
            'data_storage_location': '本地SQLite数据库',
            'data_encryption': '未加密',
            'data_access': '管理员可访问所有用户数据',
            'privacy_risk': '高 - 所有用户数据集中存储',
            'recommendations': [
                '使用云端数据库服务',
                '实现数据加密',
                '添加访问控制',
                '实现数据匿名化'
            ]
        }
    
    def export_user_data_for_privacy(self, user_id: str) -> Dict[str, Any]:
        """导出用户数据用于隐私保护"""
        try:
            user_info = self.get_user_info(user_id)
            if not user_info:
                return {}
            
            # 只导出基本信息，不包含敏感对话内容
            return {
                'user_id': user_info['user_id'],
                'username': user_info['username'],
                'created_at': user_info['created_at'],
                'last_login': user_info['last_login'],
                'login_count': user_info['login_count'],
                'data_export_time': datetime.now().isoformat(),
                'privacy_notice': '此数据仅包含用户基本信息，不包含对话内容'
            }
        except Exception as e:
            logger.error(f"导出用户隐私数据失败: {e}")
            return {}

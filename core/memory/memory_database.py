import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from loguru import logger


class MemoryDatabase:
    """记忆数据库管理类 - 使用SQLite存储记忆数据"""
    
    def __init__(self, db_path: str = "data/memory.db"):
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
        """初始化数据库表结构"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 创建短期记忆表
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS short_term_memory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        user_input TEXT NOT NULL,
                        ai_response TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # 创建长期记忆表
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS long_term_memory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        memory_type TEXT NOT NULL,  -- 'factual', 'episodic', 'semantic'
                        memory_key TEXT,             -- 用于factual和semantic的键
                        memory_value TEXT,           -- 记忆内容
                        memory_data TEXT,            -- JSON格式的完整记忆数据
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # 创建记忆更新记录表
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS memory_updates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        update_type TEXT NOT NULL,   -- 'short_term_add', 'long_term_update', 'memory_consolidation'
                        description TEXT,
                        data_count INTEGER,          -- 涉及的数据条数
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # 创建索引
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_short_term_user_id ON short_term_memory(user_id)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_short_term_timestamp ON short_term_memory(timestamp)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_long_term_user_id ON long_term_memory(user_id)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_long_term_type ON long_term_memory(memory_type)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_long_term_key ON long_term_memory(memory_key)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_memory_updates_user_id ON memory_updates(user_id)')
                
                conn.commit()
                logger.info("数据库表结构初始化完成")
                
        except Exception as e:
            logger.error(f"初始化数据库失败: {e}")
            raise
    
    def add_short_term_memory(self, user_id: str, user_input: str, ai_response: str) -> bool:
        """添加短期记忆"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                timestamp = datetime.now().isoformat()
                
                cursor.execute('''
                    INSERT INTO short_term_memory (user_id, user_input, ai_response, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, user_input, ai_response, timestamp))
                
                # 记录更新
                cursor.execute('''
                    INSERT INTO memory_updates (user_id, update_type, description, data_count)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, 'short_term_add', f'添加对话: {user_input[:50]}...', 1))
                
                conn.commit()
                logger.debug(f"短期记忆已添加: {user_input[:30]}...")
                return True
                
        except Exception as e:
            logger.error(f"添加短期记忆失败: {e}")
            return False
    
    def get_short_term_memory(self, user_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """获取短期记忆"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if limit:
                    cursor.execute('''
                        SELECT user_input, ai_response, timestamp
                        FROM short_term_memory
                        WHERE user_id = ?
                        ORDER BY timestamp DESC
                        LIMIT ?
                    ''', (user_id, limit))
                else:
                    cursor.execute('''
                        SELECT user_input, ai_response, timestamp
                        FROM short_term_memory
                        WHERE user_id = ?
                        ORDER BY timestamp DESC
                    ''', (user_id,))
                
                results = cursor.fetchall()
                memories = []
                
                for row in results:
                    memories.append({
                        'user': row[0],
                        'ai': row[1],
                        'timestamp': row[2]
                    })
                
                # 按时间正序返回（最早的在前）
                memories.reverse()
                return memories
                
        except Exception as e:
            logger.error(f"获取短期记忆失败: {e}")
            return []
    
    def clear_short_term_memory(self, user_id: str) -> bool:
        """清空短期记忆"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 获取删除前的数量
                cursor.execute('SELECT COUNT(*) FROM short_term_memory WHERE user_id = ?', (user_id,))
                count = cursor.fetchone()[0]
                
                cursor.execute('DELETE FROM short_term_memory WHERE user_id = ?', (user_id,))
                
                # 记录更新
                cursor.execute('''
                    INSERT INTO memory_updates (user_id, update_type, description, data_count)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, 'short_term_clear', f'清空短期记忆', count))
                
                conn.commit()
                logger.info(f"短期记忆已清空，删除了 {count} 条记录")
                return True
                
        except Exception as e:
            logger.error(f"清空短期记忆失败: {e}")
            return False
    
    def update_long_term_memory(self, user_id: str, memory_data: Dict[str, Any]) -> bool:
        """更新长期记忆"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 清空现有长期记忆
                cursor.execute('DELETE FROM long_term_memory WHERE user_id = ?', (user_id,))
                
                # 插入新的长期记忆
                for memory_type, data in memory_data.items():
                    if memory_type == 'factual' and isinstance(data, dict):
                        for key, value in data.items():
                            if value:  # 只保存非空值
                                cursor.execute('''
                                    INSERT INTO long_term_memory (user_id, memory_type, memory_key, memory_value, memory_data)
                                    VALUES (?, ?, ?, ?, ?)
                                ''', (user_id, memory_type, key, str(value), json.dumps({key: value})))
                    
                    elif memory_type == 'episodic' and isinstance(data, list):
                        for episode in data:
                            if episode.get('content'):
                                cursor.execute('''
                                    INSERT INTO long_term_memory (user_id, memory_type, memory_key, memory_value, memory_data)
                                    VALUES (?, ?, ?, ?, ?)
                                ''', (user_id, memory_type, None, episode.get('content'), json.dumps(episode)))
                    
                    elif memory_type == 'semantic' and isinstance(data, dict):
                        for key, value in data.items():
                            if value:  # 只保存非空值
                                cursor.execute('''
                                    INSERT INTO long_term_memory (user_id, memory_type, memory_key, memory_value, memory_data)
                                    VALUES (?, ?, ?, ?, ?)
                                ''', (user_id, memory_type, key, str(value), json.dumps({key: value})))
                
                # 记录更新
                cursor.execute('''
                    INSERT INTO memory_updates (user_id, update_type, description, data_count)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, 'long_term_update', '更新长期记忆', len(memory_data)))
                
                conn.commit()
                logger.info("长期记忆已更新")
                return True
                
        except Exception as e:
            logger.error(f"更新长期记忆失败: {e}")
            return False
    
    def get_long_term_memory(self, user_id: str) -> Dict[str, Any]:
        """获取长期记忆"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT memory_type, memory_key, memory_value, memory_data
                    FROM long_term_memory
                    WHERE user_id = ?
                    ORDER BY memory_type, memory_key
                ''', (user_id,))
                
                results = cursor.fetchall()
                
                # 重构记忆数据结构
                memory = {
                    'factual': {},
                    'episodic': [],
                    'semantic': {}
                }
                
                for row in results:
                    memory_type, memory_key, memory_value, memory_data = row
                    
                    if memory_type == 'factual':
                        if memory_key and memory_value:
                            memory['factual'][memory_key] = memory_value
                    
                    elif memory_type == 'episodic':
                        if memory_data:
                            try:
                                episode_data = json.loads(memory_data)
                                memory['episodic'].append(episode_data)
                            except json.JSONDecodeError:
                                # 如果JSON解析失败，使用原始值
                                memory['episodic'].append({'content': memory_value})
                    
                    elif memory_type == 'semantic':
                        if memory_key and memory_value:
                            memory['semantic'][memory_key] = memory_value
                
                return memory
                
        except Exception as e:
            logger.error(f"获取长期记忆失败: {e}")
            return {'factual': {}, 'episodic': [], 'semantic': {}}
    
    def clear_all_memory(self, user_id: str) -> bool:
        """清空所有记忆"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 获取删除前的数量
                cursor.execute('SELECT COUNT(*) FROM short_term_memory WHERE user_id = ?', (user_id,))
                short_term_count = cursor.fetchone()[0]
                
                cursor.execute('SELECT COUNT(*) FROM long_term_memory WHERE user_id = ?', (user_id,))
                long_term_count = cursor.fetchone()[0]
                
                # 清空所有表
                cursor.execute('DELETE FROM short_term_memory WHERE user_id = ?', (user_id,))
                cursor.execute('DELETE FROM long_term_memory WHERE user_id = ?', (user_id,))
                
                # 记录更新
                cursor.execute('''
                    INSERT INTO memory_updates (user_id, update_type, description, data_count)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, 'memory_clear_all', f'清空所有记忆', short_term_count + long_term_count))
                
                conn.commit()
                logger.info(f"所有记忆已清空，删除了 {short_term_count} 条短期记忆和 {long_term_count} 条长期记忆")
                return True
                
        except Exception as e:
            logger.error(f"清空所有记忆失败: {e}")
            return False
    
    def get_memory_stats(self, user_id: str) -> Dict[str, Any]:
        """获取记忆统计信息"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 短期记忆统计
                cursor.execute('SELECT COUNT(*) FROM short_term_memory WHERE user_id = ?', (user_id,))
                short_term_count = cursor.fetchone()[0]
                
                # 长期记忆统计
                cursor.execute('SELECT memory_type, COUNT(*) FROM long_term_memory WHERE user_id = ? GROUP BY memory_type', (user_id,))
                long_term_stats = cursor.fetchall()
                
                stats = {
                    'short_term_count': short_term_count,
                    'long_term_factual_count': 0,
                    'long_term_episodic_count': 0,
                    'long_term_semantic_count': 0
                }
                
                for memory_type, count in long_term_stats:
                    if memory_type == 'factual':
                        stats['long_term_factual_count'] = count
                    elif memory_type == 'episodic':
                        stats['long_term_episodic_count'] = count
                    elif memory_type == 'semantic':
                        stats['long_term_semantic_count'] = count
                
                return stats
                
        except Exception as e:
            logger.error(f"获取记忆统计失败: {e}")
            return {
                'short_term_count': 0,
                'long_term_factual_count': 0,
                'long_term_episodic_count': 0,
                'long_term_semantic_count': 0
            }
    
    def export_memory_data(self, user_id: str, export_path: str = None) -> str:
        """导出记忆数据"""
        if not export_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_dir = os.path.dirname(self.db_path)
            export_path = os.path.join(export_dir, f"memory_export_{user_id}_{timestamp}.json")
        
        try:
            # 获取所有记忆数据
            short_term_memory = self.get_short_term_memory(user_id)
            long_term_memory = self.get_long_term_memory(user_id)
            stats = self.get_memory_stats(user_id)
            
            export_data = {
                'user_id': user_id,
                'short_term_memory': {
                    'conversations': short_term_memory,
                    'count': len(short_term_memory)
                },
                'long_term_memory': {
                    'memory': long_term_memory,
                    'factual_count': stats['long_term_factual_count'],
                    'episodic_count': stats['long_term_episodic_count'],
                    'semantic_count': stats['long_term_semantic_count']
                },
                'export_time': datetime.now().isoformat(),
                'stats': stats,
                'database_info': {
                    'db_path': self.db_path,
                    'export_format': 'json'
                }
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
            
            logger.info(f"记忆数据已导出到: {export_path}")
            return export_path
            
        except Exception as e:
            logger.error(f"导出记忆数据失败: {e}")
            return ""
    
    def get_memory_updates_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """获取记忆更新历史"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT update_type, description, data_count, created_at
                    FROM memory_updates
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (user_id, limit))
                
                results = cursor.fetchall()
                updates = []
                
                for row in results:
                    updates.append({
                        'update_type': row[0],
                        'description': row[1],
                        'data_count': row[2],
                        'created_at': row[3]
                    })
                
                return updates
                
        except Exception as e:
            logger.error(f"获取记忆更新历史失败: {e}")
            return []

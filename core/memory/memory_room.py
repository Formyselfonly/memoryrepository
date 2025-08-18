from datetime import datetime
from typing import List, Dict, Any
from loguru import logger
from .memory_database import MemoryDatabase


class MemoryRoom:
    """记忆房间：统一管理短期和长期记忆"""
    
    def __init__(self, config, user_id: str = None):
        self.max_short_term_rounds = config.SHORT_TERM_MAX_ROUNDS
        self.user_id = user_id
        
        # 初始化SQLite数据库
        self.database = MemoryDatabase()
        
        logger.info(f"记忆房间初始化完成，使用SQLite数据库存储，用户ID: {user_id}")
    
    def set_user_id(self, user_id: str):
        """设置用户ID"""
        self.user_id = user_id
        logger.info(f"记忆房间用户ID已设置: {user_id}")
    
    def add_conversation(self, user_input: str, ai_response: str):
        """添加一轮对话到短期记忆"""
        if not self.user_id:
            logger.error("用户ID未设置，无法添加对话")
            return
        
        # 使用数据库添加短期记忆
        success = self.database.add_short_term_memory(self.user_id, user_input, ai_response)
        
        if success:
            logger.debug("对话已添加到短期记忆")
        else:
            logger.error("添加对话到短期记忆失败")
    
    def _cleanup_old_short_term_memory(self):
        """清理过期的短期记忆，保持轮数限制"""
        if not self.user_id:
            return
            
        try:
            # 获取当前短期记忆数量
            stats = self.database.get_memory_stats(self.user_id)
            current_count = stats['short_term_count']
            
            if current_count > self.max_short_term_rounds:
                # 获取所有短期记忆
                all_memories = self.database.get_short_term_memory(self.user_id)
                
                # 保留最新的N轮
                memories_to_keep = all_memories[-self.max_short_term_rounds:]
                
                # 清空并重新添加保留的记忆
                self.database.clear_short_term_memory(self.user_id)
                
                for memory in memories_to_keep:
                    self.database.add_short_term_memory(self.user_id, memory['user'], memory['ai'])
                
                logger.info(f"清理短期记忆，从 {current_count} 轮减少到 {len(memories_to_keep)} 轮")
                
        except Exception as e:
            logger.error(f"清理短期记忆失败: {e}")
    
    def get_short_term_memory(self) -> List[Dict[str, Any]]:
        """获取短期记忆"""
        if not self.user_id:
            logger.error("用户ID未设置，无法获取短期记忆")
            return []
        
        return self.database.get_short_term_memory(self.user_id, limit=self.max_short_term_rounds)
    
    def get_long_term_memory(self) -> Dict[str, Any]:
        """获取长期记忆"""
        if not self.user_id:
            logger.error("用户ID未设置，无法获取长期记忆")
            return {'factual': {}, 'episodic': [], 'semantic': {}}
        
        return self.database.get_long_term_memory(self.user_id)
    
    def update_long_term_memory(self, new_long_term_data: Dict[str, Any]):
        """更新长期记忆"""
        if not self.user_id:
            logger.error("用户ID未设置，无法更新长期记忆")
            return
        
        success = self.database.update_long_term_memory(self.user_id, new_long_term_data)
        
        if success:
            logger.info("长期记忆已更新")
        else:
            logger.error("更新长期记忆失败")
    
    def clear_short_term_memory(self):
        """清空短期记忆"""
        if not self.user_id:
            logger.error("用户ID未设置，无法清空短期记忆")
            return
        
        success = self.database.clear_short_term_memory(self.user_id)
        
        if success:
            logger.info("短期记忆已清空")
        else:
            logger.error("清空短期记忆失败")
    
    def cleanup_short_term_memory_if_needed(self):
        """如果需要，清理过期的短期记忆"""
        if not self.user_id:
            return
            
        try:
            # 获取当前短期记忆数量
            stats = self.database.get_memory_stats(self.user_id)
            current_count = stats['short_term_count']
            
            if current_count > self.max_short_term_rounds:
                # 获取所有短期记忆
                all_memories = self.database.get_short_term_memory(self.user_id)
                
                # 保留最新的N轮
                memories_to_keep = all_memories[-self.max_short_term_rounds:]
                
                # 清空并重新添加保留的记忆
                self.database.clear_short_term_memory(self.user_id)
                
                for memory in memories_to_keep:
                    self.database.add_short_term_memory(self.user_id, memory['user'], memory['ai'])
                
                logger.info(f"清理短期记忆，从 {current_count} 轮减少到 {len(memories_to_keep)} 轮")
                
        except Exception as e:
            logger.error(f"清理短期记忆失败: {e}")
    
    def clear_all_memory(self):
        """清空所有记忆"""
        if not self.user_id:
            logger.error("用户ID未设置，无法清空所有记忆")
            return
        
        success = self.database.clear_all_memory(self.user_id)
        
        if success:
            logger.info("所有记忆已清空")
        else:
            logger.error("清空所有记忆失败")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆统计信息"""
        if not self.user_id:
            logger.error("用户ID未设置，无法获取记忆统计")
            return {
                'short_term_count': 0,
                'long_term_factual_count': 0,
                'long_term_episodic_count': 0,
                'long_term_semantic_count': 0
            }
        
        return self.database.get_memory_stats(self.user_id)
    
    def export_memory(self, export_path: str = None) -> str:
        """导出记忆数据"""
        if not self.user_id:
            logger.error("用户ID未设置，无法导出记忆数据")
            return ""
        
        return self.database.export_memory_data(self.user_id, export_path)
    
    def get_memory_updates_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取记忆更新历史"""
        if not self.user_id:
            logger.error("用户ID未设置，无法获取记忆更新历史")
            return []
        
        return self.database.get_memory_updates_history(self.user_id, limit)
    
    def get_database_info(self) -> Dict[str, Any]:
        """获取数据库信息"""
        return {
            'db_path': self.database.db_path,
            'user_id': self.user_id,
            'max_short_term_rounds': self.max_short_term_rounds,
            'stats': self.get_memory_stats()
        }

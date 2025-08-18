from typing import List, Dict, Any
from loguru import logger


class MemoryInteraction:
    """记忆交互：处理记忆的检索和应用"""
    
    def __init__(self, config):
        self.config = config
    
    def get_context(self, memory_room) -> List[Dict[str, str]]:
        """获取对话上下文：长期记忆 + 短期记忆"""
        long_term_context = self.format_long_term_context(memory_room.get_long_term_memory())
        short_term_context = self.format_short_term_context(memory_room.get_short_term_memory())
        
        return long_term_context + short_term_context
    
    def format_long_term_context(self, long_term_memory: Dict[str, Any]) -> List[Dict[str, str]]:
        """格式化长期记忆为上下文"""
        if not long_term_memory or not any(long_term_memory.values()):
            return []
        
        context_parts = []
        
        # 事实记忆
        factual = long_term_memory.get('factual', {})
        if factual:
            factual_info = []
            if factual.get('identity'):
                factual_info.append(f"用户身份：{factual['identity']}")
            if factual.get('preferences'):
                factual_info.append(f"喜好：{factual['preferences']}")
            if factual.get('interests'):
                factual_info.append(f"兴趣：{factual['interests']}")
            if factual.get('important_people'):
                factual_info.append(f"重要人物：{factual['important_people']}")
            if factual.get('taboos'):
                factual_info.append(f"禁忌话题：{factual['taboos']}")
            
            if factual_info:
                context_parts.append("事实记忆：\n" + "\n".join(f"- {info}" for info in factual_info))
        
        # 情节记忆
        episodic = long_term_memory.get('episodic', [])
        if episodic:
            recent_episodes = episodic[-3:] if len(episodic) > 3 else episodic
            episode_info = [f"- {episode.get('content', '')}" for episode in recent_episodes]
            context_parts.append("最近经历：\n" + "\n".join(episode_info))
        
        # 语义记忆
        semantic = long_term_memory.get('semantic', {})
        if semantic:
            semantic_info = []
            if semantic.get('values'):
                semantic_info.append(f"价值观：{semantic['values']}")
            if semantic.get('themes'):
                semantic_info.append(f"核心主题：{semantic['themes']}")
            if semantic.get('goals'):
                semantic_info.append(f"目标抱负：{semantic['goals']}")
            
            if semantic_info:
                context_parts.append("语义记忆：\n" + "\n".join(f"- {info}" for info in semantic_info))
        
        if context_parts:
            context_text = "\n\n".join(context_parts)
            return [{
                "role": "system", 
                "content": f"基于我对您的了解：\n\n{context_text}\n\n请以小王子的身份与用户对话，体现对用户的深度理解和关怀。"
            }]
        
        return []
    
    def format_short_term_context(self, short_term_memory: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """格式化短期记忆为上下文"""
        context = []
        for conv in short_term_memory:
            context.append({"role": "user", "content": conv['user']})
            context.append({"role": "assistant", "content": conv['ai']})
        return context
    
    def get_context_summary(self, memory_room) -> str:
        """获取上下文摘要，用于调试"""
        stats = memory_room.get_memory_stats()
        return f"短期记忆: {stats['short_term_count']}轮, 长期记忆: 事实{stats['long_term_factual_count']}项, 情节{stats['long_term_episodic_count']}项, 语义{stats['long_term_semantic_count']}项"

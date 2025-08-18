import json
from typing import List, Dict, Any
from loguru import logger
from config import PromptManager


class MemoryUpdateMechanism:
    """记忆更新机制 - 将短期记忆转换为长期记忆"""
    
    def __init__(self, config, llm=None, memory_room=None):
        self.config = config
        self.current_round = 0
        self.llm = llm
        self.memory_room = memory_room
        
        # 初始化Prompt管理器
        self.prompt_manager = PromptManager()
        self.memory_analysis_template = self.prompt_manager.create_memory_analysis_template()
    
    def set_llm(self, llm):
        """设置LLM接口"""
        self.llm = llm
    
    def set_memory_room(self, memory_room):
        """设置记忆房间"""
        self.memory_room = memory_room
    
    def increment_round(self):
        """增加对话轮数"""
        self.current_round += 1
    
    def should_trigger_update(self) -> bool:
        """判断是否应该触发记忆更新"""
        return self.current_round % self.config.MEMORY_UPDATE_INTERVAL == 0
    
    def update_memory(self, short_term_memory: List[Dict[str, str]], existing_long_term_memory: Dict[str, Any]) -> Dict[str, Any]:
        """更新长期记忆"""
        try:
            # 构建对话内容字符串
            conversations = self._format_conversations(short_term_memory)
            
            # 使用LLM分析对话内容
            prompt_messages = self.memory_analysis_template.format_messages(conversations=conversations)
            analysis_result = self.llm.invoke_direct(prompt_messages)
            new_long_term_memory = self.parse_analysis_result(analysis_result)
            
            # 合并新旧记忆
            merged_memory = self._merge_memories(existing_long_term_memory, new_long_term_memory)
            
            logger.info(f"记忆更新完成，新增事实记忆: {len(new_long_term_memory.get('factual', {}))}项")
            return merged_memory
            
        except Exception as e:
            logger.error(f"记忆更新失败: {e}")
            return existing_long_term_memory
    
    def _format_conversations(self, short_term_memory: List[Dict[str, str]]) -> str:
        """格式化对话内容"""
        formatted = []
        for i, conv in enumerate(short_term_memory, 1):
            formatted.append(f"第{i}轮对话:")
            formatted.append(f"用户: {conv['user']}")
            formatted.append(f"小王子: {conv['assistant']}")
            formatted.append("")
        
        return "\n".join(formatted)
    
    def parse_analysis_result(self, analysis_result: str) -> Dict[str, Any]:
        """解析LLM分析结果"""
        try:
            import json
            # 尝试直接解析JSON
            return json.loads(analysis_result)
        except json.JSONDecodeError:
            try:
                # 尝试提取JSON部分
                import re
                json_match = re.search(r'\{.*\}', analysis_result, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    logger.error("无法从分析结果中提取JSON")
                    return self._get_empty_memory_structure()
            except Exception as e:
                logger.error(f"解析分析结果失败: {e}")
                return self._get_empty_memory_structure()
    
    def _get_empty_memory_structure(self) -> Dict[str, Any]:
        """获取空的记忆结构"""
        return {
            "factual": {
                "identity": "",
                "preferences": "",
                "interests": "",
                "important_people": "",
                "taboos": ""
            },
            "episodic": [],
            "semantic": {
                "values": "",
                "themes": "",
                "goals": ""
            }
        }
    
    def _merge_memories(self, existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
        """合并新旧记忆"""
        merged = existing.copy()
        
        # 合并事实记忆（覆盖）
        if 'factual' in new:
            if 'factual' not in merged:
                merged['factual'] = {}
            for key, value in new['factual'].items():
                if value:  # 只更新非空值
                    merged['factual'][key] = value
        
        # 合并情节记忆（追加）
        if 'episodic' in new and new['episodic']:
            if 'episodic' not in merged:
                merged['episodic'] = []
            merged['episodic'].extend(new['episodic'])
        
        # 合并语义记忆（覆盖）
        if 'semantic' in new:
            if 'semantic' not in merged:
                merged['semantic'] = {}
            for key, value in new['semantic'].items():
                if value:  # 只更新非空值
                    merged['semantic'][key] = value
        
        return merged

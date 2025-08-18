from typing import List, Dict, Any
from loguru import logger

from .llm import LLMInterface
from .memory import MemoryRoom, MemoryInteraction, MemoryUpdateMechanism
from config import PromptManager


class LittlePrinceAgent:
    """小王子AI Agent"""
    
    def __init__(self, config, user_id: str = None):
        self.config = config
        self.user_id = user_id
        
        # 初始化LLM接口
        self.llm = LLMInterface(config)
        
        # 初始化记忆房间（传入用户ID）
        self.memory_room = MemoryRoom(config, user_id)
        
        # 初始化记忆交互模块
        self.memory_interaction = MemoryInteraction(config)
        
        # 初始化记忆更新机制
        self.memory_update_mechanism = MemoryUpdateMechanism(config, self.llm, self.memory_room)
        
        # 初始化Prompt管理器
        self.prompt_manager = PromptManager()
        
        # 创建聊天模板
        self.chat_template = self.prompt_manager.create_chat_template()
        
        # TODO: self.tools = ToolsManager()
        # TODO: self.knowledge = KnowledgeBase()
        
        logger.info("小王子AI Agent初始化完成")
    
    def set_user_id(self, user_id: str):
        """设置用户ID"""
        self.user_id = user_id
        self.memory_room.set_user_id(user_id)
        logger.info(f"Agent用户ID已设置: {user_id}")
    
    def chat(self, user_input: str) -> str:
        """与用户对话"""
        try:
            # 1. 获取当前上下文
            context = self.memory_interaction.get_context(self.memory_room)
            
            # 2. 获取增强的系统提示词（包含记忆上下文）
            memory_context = self.memory_interaction.get_context_summary(self.memory_room)
            enhanced_system_prompt = self.prompt_manager.get_enhanced_system_prompt(memory_context)
            
            # 3. 构建完整提示词
            messages = self.build_chat_messages(user_input, context, enhanced_system_prompt)
            
            # 4. 调用LLM生成回复
            ai_response = self.llm.generate(messages)
            
            # 5. 更新记忆
            self.memory_room.add_conversation(user_input, ai_response)
            self.memory_update_mechanism.increment_round()
            
            # 6. 检查是否需要更新长期记忆（优先于短期记忆清理）
            if self.memory_update_mechanism.should_trigger_update():
                self.execute_memory_update()
            else:
                # 只有在不需要更新长期记忆时才清理短期记忆
                # 这样可以避免在记忆更新前清空短期记忆
                self.memory_room.cleanup_short_term_memory_if_needed()
            
            logger.debug(f"对话完成，当前轮数: {self.memory_update_mechanism.current_round}, 当前Prompt: {self.prompt_manager.get_prompt_name()}")
            return ai_response
            
        except Exception as e:
            logger.error(f"对话处理失败: {e}")
            return "抱歉，我遇到了一些问题，请稍后再试。"
    
    def build_chat_messages(self, user_input: str, context: List[Dict[str, str]], system_prompt: str) -> List[Dict[str, str]]:
        """构建聊天消息"""
        messages = []
        
        # 添加系统提示词
        messages.append({"role": "system", "content": system_prompt})
        
        # 添加记忆上下文
        messages.extend(context)
        
        # 添加用户输入
        messages.append({"role": "user", "content": user_input})
        
        return messages
    
    def execute_memory_update(self):
        """执行记忆更新"""
        try:
            short_term = self.memory_room.get_short_term_memory()
            existing_long_term = self.memory_room.get_long_term_memory()
            
            logger.info(f"开始记忆更新，短期记忆轮数: {len(short_term)}")
            
            # 更新长期记忆
            new_long_term = self.memory_update_mechanism.update_memory(short_term, existing_long_term)
            
            # 检查长期记忆是否成功更新
            # 检查是否有实际的内容变化
            has_changes = False
            logger.info(f"开始检查记忆变化...")
            logger.info(f"现有长期记忆: {existing_long_term}")
            logger.info(f"新的长期记忆: {new_long_term}")
            
            if new_long_term:
                # 检查事实记忆是否有变化
                if 'factual' in new_long_term:
                    logger.info(f"检查事实记忆: {new_long_term['factual']}")
                    for key, value in new_long_term['factual'].items():
                        if value:
                            existing_value = existing_long_term.get('factual', {}).get(key, "")
                            logger.info(f"  比较 {key}: '{value}' vs '{existing_value}'")
                            if key not in existing_long_term.get('factual', {}) or existing_long_term['factual'][key] != value:
                                logger.info(f"    ✅ 检测到变化")
                                has_changes = True
                                break
                            else:
                                logger.info(f"    ❌ 没有变化")
                
                # 检查情节记忆是否有变化
                if 'episodic' in new_long_term and new_long_term['episodic']:
                    logger.info(f"检查情节记忆: {len(new_long_term['episodic'])} 项")
                    if new_long_term['episodic']:
                        logger.info(f"    ✅ 检测到变化")
                        has_changes = True
                
                # 检查语义记忆是否有变化
                if 'semantic' in new_long_term:
                    logger.info(f"检查语义记忆: {new_long_term['semantic']}")
                    for key, value in new_long_term['semantic'].items():
                        if value:
                            existing_value = existing_long_term.get('semantic', {}).get(key, "")
                            logger.info(f"  比较 {key}: '{value}' vs '{existing_value}'")
                            if key not in existing_long_term.get('semantic', {}) or existing_long_term['semantic'][key] != value:
                                logger.info(f"    ✅ 检测到变化")
                                has_changes = True
                                break
                            else:
                                logger.info(f"    ❌ 没有变化")
            
            logger.info(f"最终比较结果: has_changes = {has_changes}")
            
            if has_changes:
                self.memory_room.update_long_term_memory(new_long_term)
                logger.info(f"长期记忆更新成功，检测到变化")
                
                # 只有在长期记忆更新成功后才清空短期记忆
                self.memory_room.clear_short_term_memory()
                logger.info(f"短期记忆已清空")
                
                # 成功更新后重置对话轮计数，确保严格的批次语义（例如1-5总结后，从0重新计数）
                self.memory_update_mechanism.current_round = 0
                logger.info("对话轮计数已重置为0")

                logger.info(f"第{self.memory_update_mechanism.current_round}轮：记忆更新完成")
            else:
                logger.warning(f"长期记忆更新失败或没有变化，保留短期记忆")
            
        except Exception as e:
            logger.error(f"记忆更新失败: {e}")
            # 出错时不清空短期记忆，避免数据丢失
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆统计信息"""
        return self.memory_room.get_memory_stats()
    
    def get_context_summary(self) -> str:
        """获取上下文摘要"""
        return self.memory_interaction.get_context_summary(self.memory_room)
    
    def get_current_prompt_info(self) -> Dict[str, Any]:
        """获取当前Prompt信息"""
        return {
            "prompt_name": self.prompt_manager.current_prompt_name,
            "name": self.prompt_manager.get_prompt_name(),
            "examples_count": len(self.prompt_manager.get_examples())
        }
    
    def switch_model(self, provider: str, model: str, api_key: str = None):
        """动态切换模型"""
        self.llm.switch_model(provider, model, api_key)
        logger.info(f"Agent模型切换成功: {provider} - {model}")
    
    def set_prompt(self, prompt_name: str):
        """设置Prompt"""
        self.prompt_manager.set_current_prompt(prompt_name)
        logger.info(f"Agent Prompt切换成功: {self.prompt_manager.get_prompt_name(prompt_name)}")
    
    def get_available_prompts(self) -> List[str]:
        """获取可用的Prompt列表"""
        return self.prompt_manager.get_available_prompts()

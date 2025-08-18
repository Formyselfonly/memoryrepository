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
        self.memory_interaction = MemoryInteraction(self.memory_room)
        
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
            context = self.memory_interaction.get_context()
            
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
            
            # 6. 检查是否需要更新长期记忆
            if self.memory_update_mechanism.should_trigger_update():
                self.execute_memory_update()
            
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
            
            # 更新长期记忆
            new_long_term = self.memory_update_mechanism.update_memory(short_term, existing_long_term)
            self.memory_room.update_long_term_memory(new_long_term)
            
            # 清空短期记忆
            self.memory_room.clear_short_term_memory()
            
            logger.info(f"第{self.memory_update_mechanism.current_round}轮：记忆更新完成")
            
        except Exception as e:
            logger.error(f"记忆更新失败: {e}")
    
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

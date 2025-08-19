import json
import os
from typing import Dict, Any, Optional
from loguru import logger
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    logger.warning("PyYAML未安装，将使用JSON格式")


class PromptManager:
    """Prompt管理器 - 统一管理Prompt配置和LangChain模板"""
    
    def __init__(self, config_file: str = "config/prompts_config.yaml"):
        self.config_file = config_file
        self.prompts_config = self._load_prompts_config()
        self.current_prompt_name = "little_prince_fan_v1"  # 默认Prompt
    
    def _load_prompts_config(self) -> Dict[str, Any]:
        """加载Prompt配置文件"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), "prompts_config.yaml")
            
            # 优先尝试YAML格式
            if YAML_AVAILABLE and os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                logger.info(f"成功加载YAML Prompt配置，共{len(config)}个Prompt")
                return config
            
            # 如果YAML不可用或文件不存在，尝试JSON格式
            json_path = os.path.join(os.path.dirname(__file__), "prompts_config.json")
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logger.info(f"成功加载JSON Prompt配置，共{len(config)}个Prompt")
                return config
            
            # 如果都不可用，返回默认配置
            logger.warning("未找到Prompt配置文件，使用默认配置")
            return self._get_default_config()
            
        except Exception as e:
            logger.error(f"加载Prompt配置失败: {e}")
            # 返回默认配置
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "little_prince_v1": {
                "name": "little_prince_v1",
                "system_prompt": "你是小王子，来自B-612星球。你有着纯真的心灵和对世界的好奇心。请以小王子的身份与用户对话，体现你的纯真、善良和对友谊的珍视。",
                "examples": []
            }
        }
    
    def get_current_prompt_config(self) -> Dict[str, Any]:
        """获取当前Prompt的配置"""
        return self.prompts_config.get(self.current_prompt_name, self.prompts_config["little_prince_v1"])
    
    def get_system_prompt(self, prompt_name: Optional[str] = None) -> str:
        """获取指定Prompt的系统提示词"""
        prompt_name = prompt_name or self.current_prompt_name
        config = self.prompts_config.get(prompt_name, self.prompts_config["little_prince_v1"])
        return config.get("system_prompt", "")
    
    def get_prompt_name(self, prompt_name: Optional[str] = None) -> str:
        """获取指定Prompt的名称"""
        prompt_name = prompt_name or self.current_prompt_name
        config = self.prompts_config.get(prompt_name, self.prompts_config["little_prince_v1"])
        return config.get("name", "unknown_prompt")
    
    def get_examples(self, prompt_name: Optional[str] = None) -> list:
        """获取指定Prompt的示例对话"""
        prompt_name = prompt_name or self.current_prompt_name
        config = self.prompts_config.get(prompt_name, self.prompts_config["little_prince_v1"])
        return config.get("examples", [])
    
    def set_current_prompt(self, prompt_name: str):
        """设置当前Prompt"""
        if prompt_name in self.prompts_config:
            self.current_prompt_name = prompt_name
            logger.info(f"切换到Prompt: {self.get_prompt_name(prompt_name)}")
        else:
            logger.warning(f"未知的Prompt: {prompt_name}")
    
    def get_all_prompts(self) -> list:
        """获取所有Prompt名称"""
        return list(self.prompts_config.keys())
    
    def get_available_prompts(self) -> list:
        """获取可用的Prompt列表（别名方法）"""
        return self.get_all_prompts()
    
    def get_prompt_info(self, prompt_name: str) -> Dict[str, Any]:
        """获取指定Prompt的完整信息"""
        return self.prompts_config.get(prompt_name, {})
    
    def get_enhanced_system_prompt(self, memory_context: str = "", prompt_name: Optional[str] = None) -> str:
        """获取增强的系统提示词（包含记忆上下文）"""
        base_prompt = self.get_system_prompt(prompt_name)
        
        if memory_context:
            enhanced_prompt = f"{base_prompt}\n\n**记忆上下文**:\n{memory_context}\n\n请基于以上记忆信息，以小王子的身份与用户对话。"
        else:
            enhanced_prompt = base_prompt
        
        return enhanced_prompt
    
    # LangChain模板方法
    def get_memory_analysis_prompt(self) -> str:
        """获取记忆分析提示词"""
        return """请分析以下对话，提取用户的长期记忆信息。请严格按照以下格式返回JSON：
        对话内容：
        {conversations}

        请提取并返回以下格式的JSON：

        {{
            "factual": {{
                "identity": "用户身份信息（姓名、昵称、偏好称呼）",
                "preferences": "喜好与厌恶（食物、天气、颜色、动物等）",
                "interests": "兴趣与习惯（爱好、日常作息、生活方式）",
                "important_people": "重要人物（家人、朋友、宠物）",
                "taboos": "禁忌话题（用户不喜欢或避免谈论的内容）"
            }},
            "episodic": [
                {{
                    "type": "用户经历/情感亮点/共享记忆/特殊时刻/怀旧故事",
                    "content": "具体内容描述",
                    "timestamp": "时间信息"
                }}
            ],
            "semantic": {{
                "values": "价值观（对幸福、爱情、成长的看法）",
                "themes": "核心主题（重复的情感模式、人生信念）",
                "goals": "长期目标与抱负（想成为的人、追求的生活）"
            }}
        }}

        注意：
        1. 只提取确实在对话中提到的信息
        2. 如果某个类别没有相关信息，返回空字符串或空数组
        3. 确保返回的是有效的JSON格式
        4. 不要添加任何额外的解释文字，只返回JSON"""

    def create_chat_template(self) -> ChatPromptTemplate:
        """创建聊天模板"""
        return ChatPromptTemplate.from_messages([
            ("system", self.get_system_prompt()),
            MessagesPlaceholder(variable_name="context"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])

    def create_memory_analysis_template(self) -> ChatPromptTemplate:
        """创建记忆分析模板"""
        return ChatPromptTemplate.from_messages([
            ("system", self.get_memory_analysis_prompt())
        ])

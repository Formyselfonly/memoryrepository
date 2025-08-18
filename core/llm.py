from typing import List, Dict, Any, Optional
from loguru import logger
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek


class LLMInterface:
    """LLM接口封装 - 使用LangChain实现"""
    
    def __init__(self, config):
        self.config = config
        self.model = config.LLM_MODEL
        self.temperature = config.TEMPERATURE
        self.provider = config.LLM_PROVIDER.lower()
        
        # 根据提供商初始化不同的LLM
        self.llm = self._initialize_llm()
        
        logger.info(f"LLM初始化完成: {self.provider} - {self.model}")
    
    def _initialize_llm(self):
        """根据配置初始化LLM"""
        if self.provider == "openai":
            return ChatOpenAI(
                model=self.model,
                temperature=self.temperature,
                openai_api_key=self.config.LLM_API_KEY
            )
        elif self.provider == "deepseek":
            return ChatDeepSeek(
                model=self.model,
                temperature=self.temperature,
                deepseek_api_key=self.config.LLM_API_KEY
            )
        else:
            raise ValueError(f"不支持的LLM提供商: {self.provider}")
    
    def generate(self, messages: List[Dict[str, str]]) -> str:
        """生成回复 - 使用LangChain消息格式"""
        try:
            # 转换消息格式
            langchain_messages = self._convert_messages(messages)
            
            # 调用LLM
            response = self.llm.invoke(langchain_messages)
            return response.content
            
        except Exception as e:
            logger.error(f"LLM调用失败: {e}")
            return "抱歉，我现在无法回应，请稍后再试。"
    
    def generate_from_prompt(self, prompt: str) -> str:
        """从提示词生成回复"""
        try:
            # 创建提示模板
            prompt_template = ChatPromptTemplate.from_messages([
                ("user", prompt)
            ])
            
            # 生成回复
            response = self.llm.invoke(prompt_template.format_messages())
            return response.content
            
        except Exception as e:
            logger.error(f"提示词生成失败: {e}")
            return "抱歉，我现在无法回应，请稍后再试。"
    
    def _convert_messages(self, messages: List[Dict[str, str]]) -> List[BaseMessage]:
        """转换消息格式为LangChain格式"""
        langchain_messages = []
        
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                langchain_messages.append(SystemMessage(content=content))
            elif role == "user":
                langchain_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                langchain_messages.append(AIMessage(content=content))
            else:
                logger.warning(f"未知的消息角色: {role}")
                langchain_messages.append(HumanMessage(content=content))
        
        return langchain_messages
    
    def create_prompt_template(self, template: str) -> ChatPromptTemplate:
        """创建提示模板"""
        return ChatPromptTemplate.from_messages([
            ("system", template),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
    
    def switch_model(self, provider: str, model: str, api_key: Optional[str] = None):
        """动态切换模型"""
        try:
            self.provider = provider.lower()
            self.model = model
            if api_key:
                self.config.LLM_API_KEY = api_key
            
            # 重新初始化LLM
            self.llm = self._initialize_llm()
            logger.info(f"模型切换成功: {self.provider} - {self.model}")
            
        except Exception as e:
            logger.error(f"模型切换失败: {e}")
            raise

    def invoke_direct(self, messages) -> str:
        """直接调用LLM，供记忆更新机制使用"""
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"直接LLM调用失败: {e}")
            return ""

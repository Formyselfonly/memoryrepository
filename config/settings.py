import os
from typing import Optional
from pydantic_settings import BaseSettings
from loguru import logger


class Config(BaseSettings):
    """系统配置类"""
    
    # LLM配置
    LLM_PROVIDER: str = "deepseek"  # openai, deepseek
    LLM_MODEL: str = "deepseek-chat"  # 根据提供商选择模型
    LLM_API_KEY: Optional[str] = None
    DEEPSEEK_API_KEY: Optional[str] = None  # DeepSeek API密钥
    
    # 记忆配置
    SHORT_TERM_MAX_ROUNDS: int = 10
    MEMORY_UPDATE_INTERVAL: int = 10
    # 系统配置
    LOG_LEVEL: str = "INFO"
    TEMPERATURE: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # 忽略额外的字段
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.LLM_API_KEY:
            raise ValueError("LLM_API_KEY is required. Please set it in your .env file.")
    
    def get_model_config(self) -> dict:
        """获取模型配置信息"""
        return {
            "provider": self.LLM_PROVIDER,
            "model": self.LLM_MODEL,
            "temperature": self.TEMPERATURE
        }
    
    def validate_model_config(self):
        """验证模型配置"""
        valid_providers = ["openai", "deepseek"]
        if self.LLM_PROVIDER.lower() not in valid_providers:
            raise ValueError(f"不支持的LLM提供商: {self.LLM_PROVIDER}. 支持的提供商: {valid_providers}")
        
        # 根据提供商验证模型名称
        if self.LLM_PROVIDER.lower() == "openai":
            valid_models = ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
            if self.LLM_MODEL not in valid_models:
                logger.warning(f"OpenAI模型 {self.LLM_MODEL} 可能不是标准模型名")
        
        elif self.LLM_PROVIDER.lower() == "deepseek":
            valid_models = ["deepseek-chat", "deepseek-coder", "deepseek-llm-7b-chat"]
            if self.LLM_MODEL not in valid_models:
                logger.warning(f"DeepSeek模型 {self.LLM_MODEL} 可能不是标准模型名")

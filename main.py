#!/usr/bin/env python3
"""
小王子记忆构架系统 - 主入口文件
"""

import os
from dotenv import load_dotenv
from loguru import logger

from config import Config
from utils.logger import setup_logger
from core import LittlePrinceAgent


def main():
    """主函数"""
    # 加载环境变量
    load_dotenv()
    
    # 设置日志
    setup_logger("INFO")
    
    try:
        # 初始化配置
        config = Config()
        logger.info("配置加载成功")
        
        # 初始化AI Agent
        agent = LittlePrinceAgent(config)
        logger.info("小王子AI Agent初始化成功")
        
        # 简单的命令行交互界面
        print("🌹 欢迎来到小王子的世界！")
        print("我是小王子，来自B-612星球。让我们开始对话吧！")
        print("输入 'quit' 或 'exit' 退出对话")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("你: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("小王子: 再见！希望我们很快能再次相遇。记住，真正重要的东西用眼睛是看不见的。")
                    break
                
                if not user_input:
                    continue
                
                # 获取AI回复
                response = agent.chat(user_input)
                print(f"小王子: {response}")
                
                # 显示记忆统计（调试用）
                if agent.memory_update_mechanism.current_round % 5 == 0:
                    stats = agent.get_memory_stats()
                    print(f"\n[记忆状态] 短期: {stats['short_term_count']}轮, 长期: 事实{stats['long_term_factual_count']}项, 情节{stats['long_term_episodic_count']}项")
                
                print()
                
            except KeyboardInterrupt:
                print("\n小王子: 再见！")
                break
            except Exception as e:
                logger.error(f"对话处理错误: {e}")
                print("小王子: 抱歉，我遇到了一些问题。")
    
    except Exception as e:
        logger.error(f"系统初始化失败: {e}")
        print(f"系统错误: {e}")
        print("请检查配置文件和环境变量设置。")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
简单测试脚本 - 验证bug修复
"""

import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试导入是否正常"""
    print("🧪 测试导入...")
    
    try:
        from config import Config
        print("   ✅ Config导入成功")
        
        from core import LittlePrinceAgent
        print("   ✅ LittlePrinceAgent导入成功")
        
        print("✅ 所有导入测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 导入测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config():
    """测试配置加载"""
    print("\n🧪 测试配置加载...")
    
    try:
        from config import Config
        
        # 设置测试环境变量
        os.environ["LLM_API_KEY"] = "test_key"
        
        config = Config()
        print(f"   ✅ 配置加载成功: {config.LLM_PROVIDER} - {config.LLM_MODEL}")
        
        model_config = config.get_model_config()
        print(f"   ✅ 模型配置: {model_config}")
        
        print("✅ 配置测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_init():
    """测试Agent初始化"""
    print("\n🧪 测试Agent初始化...")
    
    try:
        from config import Config
        from core import LittlePrinceAgent
        
        # 设置测试环境变量
        os.environ["LLM_API_KEY"] = "test_key"
        
        config = Config()
        agent = LittlePrinceAgent(config)
        print("   ✅ Agent初始化成功")
        
        # 测试记忆统计
        stats = agent.get_memory_stats()
        print(f"   ✅ 记忆统计: {stats}")
        
        print("✅ Agent初始化测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ Agent初始化测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔧 开始bug修复验证...")
    
    # 加载环境变量
    load_dotenv()
    
    # 运行测试
    success = True
    success &= test_imports()
    success &= test_config()
    success &= test_agent_init()
    
    if success:
        print("\n🎉 所有测试通过！Bug修复成功！")
        print("现在可以运行完整的测试: python test_system.py")
    else:
        print("\n❌ 部分测试失败，需要进一步修复")

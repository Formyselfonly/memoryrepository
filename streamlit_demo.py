#!/usr/bin/env python3
"""
小王子记忆构架系统 - Streamlit Demo
"""

import streamlit as st
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from core import LittlePrinceAgent
from core.user_manager import UserManager


def initialize_session_state():
    """初始化会话状态"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'agent' not in st.session_state:
        st.session_state.agent = None
    if 'user_manager' not in st.session_state:
        st.session_state.user_manager = UserManager()
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'prompt_authenticated' not in st.session_state:
        st.session_state.prompt_authenticated = False


def load_env_config():
    """加载环境配置"""
    # 加载.env文件
    load_dotenv()
    
    # 检查是否有可用的API密钥
    openai_key = os.getenv("LLM_API_KEY")
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    provider = os.getenv("LLM_PROVIDER", "openai")
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    
    # 获取Prompt查看密码
    prompt_password = os.getenv("PROMPT_VIEW_PASSWORD", "test")
    
    return {
        'openai_key': openai_key,
        'deepseek_key': deepseek_key,
        'provider': provider,
        'model': model,
        'has_config': bool(openai_key or deepseek_key),
        'prompt_password': prompt_password
    }


def setup_api_config():
    """设置API配置"""
    st.sidebar.header("🔑 API配置")
    
    # 加载环境配置
    env_config = load_env_config()
    
    # 显示当前环境配置状态
    if env_config['has_config']:
        st.sidebar.success("✅ 检测到本地.env配置")
        st.sidebar.info(f"当前配置: {env_config['provider']} - {env_config['model']}")
        
        # 自动初始化按钮
        if st.sidebar.button("🚀 使用本地配置初始化", type="primary"):
            try:
                # 使用环境变量初始化
                config = Config()
                # 检查是否有当前用户，如果有则使用其user_id
                if st.session_state.current_user:
                    st.session_state.agent = LittlePrinceAgent(config, st.session_state.current_user['user_id'])
                else:
                    st.sidebar.error("❌ 请先登录用户！")
                    return False
                st.session_state.chat_history = []
                
                st.sidebar.success("✅ 系统初始化成功！")
                st.rerun()
                
            except Exception as e:
                st.sidebar.error(f"❌ 初始化失败: {str(e)}")
                return False
    
    st.sidebar.markdown("---")
    st.sidebar.write("**或手动配置:**")
    
    # 选择LLM提供商
    provider = st.sidebar.selectbox(
        "选择LLM提供商",
        ["openai", "deepseek"],
        index=0 if env_config['provider'] == 'openai' else 1
    )
    
    # 根据提供商选择模型
    if provider == "openai":
        model = st.sidebar.selectbox(
            "选择OpenAI模型",
            ["gpt-4o-mini", "gpt-4o", "gpt-5", "gpt-5-mini"],
            index=0
        )
        api_key = st.sidebar.text_input(
            "OpenAI API密钥",
            value=env_config['openai_key'] or "",
            type="password",
            help="请输入您的OpenAI API密钥"
        )
        deepseek_key = None
    else:
        model = st.sidebar.selectbox(
            "选择DeepSeek模型",
            ["deepseek-chat", "deepseek-reasoner"],
            index=0
        )
        api_key = st.sidebar.text_input(
            "DeepSeek API密钥",
            value=env_config['deepseek_key'] or "",
            type="password",
            help="请输入您的DeepSeek API密钥"
        )
        deepseek_key = api_key
    
    # 手动初始化按钮
    if st.sidebar.button("🔧 手动初始化系统"):
        if not api_key:
            st.sidebar.error("请输入API密钥")
            return False
        
        try:
            # 设置环境变量
            os.environ["LLM_PROVIDER"] = provider
            os.environ["LLM_MODEL"] = model
            os.environ["LLM_API_KEY"] = api_key
            if deepseek_key:
                os.environ["DEEPSEEK_API_KEY"] = deepseek_key
            
            # 初始化配置和Agent
            config = Config()
            # 检查是否有当前用户，如果有则使用其user_id
            if st.session_state.current_user:
                st.session_state.agent = LittlePrinceAgent(config, st.session_state.current_user['user_id'])
            else:
                st.sidebar.error("❌ 请先登录用户！")
                return False
            st.session_state.chat_history = []
            
            st.sidebar.success("✅ 系统初始化成功！")
            st.rerun()
            
        except Exception as e:
            st.sidebar.error(f"❌ 初始化失败: {str(e)}")
            return False
    
    return provider, model, api_key, deepseek_key, env_config['prompt_password']


def display_memory_stats():
    """显示记忆统计信息"""
    if st.session_state.agent:
        stats = st.session_state.agent.get_memory_stats()
        st.session_state.memory_stats = stats
    
    # 创建记忆状态显示区域
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="对话轮数",
            value=st.session_state.memory_stats.get('short_term_count', 0),
            delta=None
        )
    
    with col2:
        st.metric(
            label="短期记忆",
            value=st.session_state.memory_stats.get('short_term_count', 0),
            delta=None
        )
    
    with col3:
        long_term_total = (
            st.session_state.memory_stats.get('long_term_factual_count', 0) +
            st.session_state.memory_stats.get('long_term_episodic_count', 0) +
            st.session_state.memory_stats.get('long_term_semantic_count', 0)
        )
        st.metric(
            label="长期记忆",
            value=long_term_total,
            delta=None
        )
    
    with col4:
        st.metric(
            label="记忆更新轮数",
            value=st.session_state.agent.memory_update_mechanism.current_round if st.session_state.agent else 0,
            delta=None
        )
    
    with col5:
        if st.session_state.agent:
            prompt_info = st.session_state.agent.get_current_prompt_info()
            st.metric(
                label="当前Prompt",
                value=prompt_info.get('name', '未知'),
                delta=None
            )
        else:
            st.metric(
                label="当前Prompt",
                value="未初始化",
                delta=None
            )


def display_chat_history():
    """显示聊天历史"""
    st.subheader("💬 聊天记录")
    
    # 创建聊天容器
    chat_container = st.container()
    
    with chat_container:
        for i, message in enumerate(st.session_state.chat_history):
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(message["content"])


def chat_interface():
    """聊天界面"""
    st.subheader("🌹 与小王子对话")
    
    # 聊天输入
    if prompt := st.chat_input("输入您的消息..."):
        if st.session_state.agent:
            # 添加用户消息到历史
            st.session_state.chat_history.append({
                "role": "user",
                "content": prompt,
                "timestamp": datetime.now()
            })
            
            # 获取AI回复
            with st.spinner("小王子正在思考..."):
                try:
                    response = st.session_state.agent.chat(prompt)
                    
                    # 添加AI回复到历史
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response,
                        "timestamp": datetime.now()
                    })
                    
                    # 更新记忆统计
                    stats = st.session_state.agent.get_memory_stats()
                    st.session_state.memory_stats = stats
                    
                except Exception as e:
                    error_msg = f"抱歉，我遇到了一些问题：{str(e)}"
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": error_msg,
                        "timestamp": datetime.now()
                    })
            
            # 重新运行页面以显示新消息
            st.rerun()


def display_memory_details():
    """显示详细记忆信息"""
    if st.session_state.agent:
        with st.expander("📚 详细记忆信息"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**短期记忆详情:**")
                short_term = st.session_state.agent.memory_room.get_short_term_memory()
                if short_term:
                    for i, conv in enumerate(short_term, 1):
                        st.write(f"第{i}轮:")
                        st.write(f"  用户: {conv['user'][:50]}...")
                        st.write(f"  AI: {conv['ai'][:50]}...")
                else:
                    st.write("暂无短期记忆")
            
            with col2:
                st.write("**长期记忆详情:**")
                long_term = st.session_state.agent.memory_room.get_long_term_memory()
                
                if long_term.get('factual'):
                    st.write("**事实记忆:**")
                    for key, value in long_term['factual'].items():
                        if value:
                            st.write(f"  {key}: {value}")
                
                if long_term.get('episodic'):
                    st.write("**情节记忆:**")
                    for episode in long_term['episodic'][-3:]:  # 显示最近3个
                        st.write(f"  - {episode.get('content', '')[:50]}...")
                
                if long_term.get('semantic'):
                    st.write("**语义记忆:**")
                    for key, value in long_term['semantic'].items():
                        if value:
                            st.write(f"  {key}: {value}")


def display_sidebar_prompt_details(prompt_password):
    """在侧边栏显示Prompt详情（需要密码）"""
    st.sidebar.markdown("---")
    st.sidebar.header("🎭 Prompt详情")
    
    # 密码验证
    if 'prompt_authenticated' not in st.session_state:
        st.session_state.prompt_authenticated = False
    
    if not st.session_state.prompt_authenticated:
        password_input = st.sidebar.text_input(
            "请输入密码查看Prompt详情",
            type="password",
            key="prompt_password_input"
        )
        
        if st.sidebar.button("🔓 验证密码"):
            if password_input == prompt_password:
                st.session_state.prompt_authenticated = True
                st.sidebar.success("✅ 密码验证成功！")
                st.rerun()
            else:
                st.sidebar.error("❌ 密码错误！")
        return
    
    # 密码验证成功，显示Prompt详情
    if not st.session_state.agent:
        st.sidebar.warning("请先初始化系统")
        return
    
    # 获取当前Prompt信息
    prompt_info = st.session_state.agent.get_current_prompt_info()
    current_prompt_name = prompt_info['prompt_name']
    
    # 获取完整的Prompt配置
    prompt_config = st.session_state.agent.prompt_manager.get_prompt_info(current_prompt_name)
    
    # 显示基本信息
    st.sidebar.markdown("**📊 Prompt信息**")
    system_prompt = prompt_config.get('system_prompt', '')
    examples = prompt_config.get('examples', [])
    
    st.sidebar.write(f"**名称**: {prompt_config.get('name', 'N/A')}")
    st.sidebar.write(f"**长度**: {len(system_prompt)} 字符")
    st.sidebar.write(f"**示例**: {len(examples)} 个")
    
    # 显示系统提示词内容
    st.sidebar.markdown("**📝 系统提示词内容**")
    if system_prompt:
        st.sidebar.text_area(
            "系统提示词",
            value=system_prompt,
            height=300,
            disabled=True,
            key="sidebar_system_prompt"
        )
    else:
        st.sidebar.warning("未设置系统提示词")
    
    # 退出按钮
    if st.sidebar.button("🔒 退出查看"):
        st.session_state.prompt_authenticated = False
        st.rerun()


def display_user_login():
    """显示用户登录界面"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("👤 用户登录")
    
    if st.session_state.current_user is None:
        # 用户未登录，显示登录界面
        username = st.sidebar.text_input("请输入您的用户名", placeholder="例如：小明")
        
        if st.sidebar.button("登录/注册", type="primary"):
            if username.strip():
                # 执行用户登录
                login_result = st.session_state.user_manager.login_user(username.strip())
                
                if login_result['user_id']:
                    st.session_state.current_user = login_result
                    
                    # 创建或更新Agent
                    config = Config()
                    st.session_state.agent = LittlePrinceAgent(config, login_result['user_id'])
                    
                    st.sidebar.success(login_result['message'])
                    st.rerun()
                else:
                    st.sidebar.error(login_result['message'])
            else:
                st.sidebar.error("请输入用户名！")
    else:
        # 用户已登录，显示用户信息
        user = st.session_state.current_user
        
        st.sidebar.success(f"✅ 已登录: {user['username']}")
        st.sidebar.write(f"**用户ID:** {user['user_id'][:8]}...")
        st.sidebar.write(f"**登录次数:** {user['login_count']}")
        
        if st.sidebar.button("退出登录"):
            # 结束用户会话
            st.session_state.user_manager.end_user_session(user['user_id'])
            
            # 清空会话状态
            st.session_state.current_user = None
            st.session_state.agent = None
            st.session_state.messages = []
            st.session_state.prompt_authenticated = False
            
            st.sidebar.success("已退出登录")
            st.rerun()


def display_user_stats():
    """显示用户统计信息"""
    if st.session_state.current_user:
        st.sidebar.markdown("---")
        st.sidebar.subheader("📊 用户统计")
        
        user_stats = st.session_state.user_manager.get_user_stats()
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("总用户数", user_stats['total_users'])
            st.metric("今日新增", user_stats['new_users_today'])
        
        with col2:
            st.metric("今日活跃", user_stats['active_users_today'])
            st.metric("在线用户", user_stats['online_users'])
    
    # 显示数据隐私信息
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔒 数据隐私")
    
    privacy_info = st.session_state.user_manager.get_data_privacy_info()
    
    # 隐私风险警告
    st.sidebar.warning("⚠️ 隐私风险提醒")
    st.sidebar.write(f"**存储位置**: {privacy_info['data_storage_location']}")
    st.sidebar.write(f"**加密状态**: {privacy_info['data_encryption']}")
    st.sidebar.write(f"**访问权限**: {privacy_info['data_access']}")
    
    # 展开显示详细建议
    with st.sidebar.expander("📋 隐私保护建议", expanded=False):
        for i, recommendation in enumerate(privacy_info['recommendations'], 1):
            st.write(f"{i}. {recommendation}")
        
        st.markdown("---")
        st.markdown("**当前部署方式**:")
        server_address = st.get_option("server.address")
        if server_address and "localhost" in server_address:
            st.write("🔴 本地部署 - 高隐私风险")
            st.write("所有用户数据存储在您的电脑上")
        else:
            st.write("🟡 云端部署 - 中等隐私风险")
            st.write("数据存储在云端服务器上")


def main():
    """主函数"""
    st.set_page_config(
        page_title="小王子记忆构架系统",
        page_icon="🌹",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 初始化会话状态
    initialize_session_state()
    
    # 获取环境配置
    env_config = load_env_config()
    llm_provider = env_config['provider']
    llm_model = env_config['model']
    llm_api_key = env_config['openai_key']
    deepseek_api_key = env_config['deepseek_key']
    prompt_password = env_config['prompt_password']
    
    # 页面标题
    st.title("🌹 小王子记忆构架系统")
    st.markdown("---")
    
    # 侧边栏配置
    with st.sidebar:
        st.header("⚙️ 系统配置")
        
        # 用户登录
        display_user_login()
        
        # 用户统计
        display_user_stats()
        
        # 只有在用户登录后才显示其他配置
        if st.session_state.current_user:
            # API配置
            st.markdown("---")
            st.subheader("🔑 API配置")
            
            # 显示当前配置状态
            if env_config['has_config']:
                st.success("✅ 检测到API配置")
                st.info(f"当前配置: {llm_provider} - {llm_model}")
            else:
                st.warning("⚠️ 未检测到API配置")
                st.info("请在.env文件中配置API密钥")
            
            # LLM提供商选择
            selected_provider = st.selectbox(
                "选择LLM提供商",
                ["openai", "deepseek"],
                index=0 if llm_provider == "openai" else 1
            )
            
            # 根据提供商显示不同的配置
            if selected_provider == "openai":
                openai_models = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
                selected_model = st.selectbox("OpenAI模型", openai_models, index=openai_models.index(llm_model) if llm_model in openai_models else 0)
                api_key = st.text_input("OpenAI API Key", value=llm_api_key or "", type="password")
                
                if st.button("更新OpenAI配置"):
                    os.environ["LLM_PROVIDER"] = "openai"
                    os.environ["LLM_MODEL"] = selected_model
                    os.environ["LLM_API_KEY"] = api_key
                    st.success("OpenAI配置已更新！")
                    
            else:  # deepseek
                deepseek_models = ["deepseek-chat", "deepseek-coder", "deepseek-llm-7b-chat"]
                selected_model = st.selectbox("DeepSeek模型", deepseek_models, index=deepseek_models.index(llm_model) if llm_model in deepseek_models else 0)
                api_key = st.text_input("DeepSeek API Key", value=deepseek_api_key or "", type="password")
                
                if st.button("更新DeepSeek配置"):
                    os.environ["LLM_PROVIDER"] = "deepseek"
                    os.environ["LLM_MODEL"] = selected_model
                    os.environ["DEEPSEEK_API_KEY"] = api_key
                    st.success("DeepSeek配置已更新！")
            
            # Prompt控制
            st.markdown("---")
            st.subheader("🎭 Prompt控制")
            
            if st.session_state.agent:
                current_prompt = st.session_state.agent.get_current_prompt_info()
                st.write(f"**当前Prompt:** {current_prompt['name']}")
                
                available_prompts = st.session_state.agent.get_available_prompts()
                selected_prompt = st.selectbox("选择Prompt", available_prompts, index=0)
                
                if st.button("切换Prompt"):
                    if st.session_state.agent.set_prompt(selected_prompt):
                        st.success(f"已切换到: {selected_prompt}")
                        st.rerun()
                    else:
                        st.error("Prompt切换失败")
            
            # Prompt详情显示
            display_sidebar_prompt_details(prompt_password)
            
            # 记忆管理
            st.markdown("---")
            st.subheader("💾 记忆管理")
            
            if st.session_state.agent:
                # 导出记忆数据
                if st.button("📤 导出记忆数据"):
                    export_path = st.session_state.agent.memory_room.export_memory()
                    if export_path:
                        with open(export_path, 'r', encoding='utf-8') as f:
                            st.download_button(
                                label="📥 下载记忆数据",
                                data=f.read(),
                                file_name=os.path.basename(export_path),
                                mime="application/json"
                            )
                        st.success(f"记忆数据已导出: {export_path}")
                    else:
                        st.error("导出失败")
                
                # 清空所有记忆
                st.markdown("**🗑️ 清空记忆:**")
                clear_confirm = st.checkbox("确认清空所有记忆")
                if st.button("清空所有记忆", disabled=not clear_confirm):
                    st.session_state.agent.memory_room.clear_all_memory()
                    st.session_state.messages = []
                    st.success("所有记忆已清空")
                    st.rerun()
                
                # 显示数据库信息
                db_info = st.session_state.agent.memory_room.get_database_info()
                
                st.markdown("**🗄️ SQLite数据库信息:**")
                st.write(f"• 数据库路径: `{db_info['db_path']}`")
                st.write(f"• 用户ID: `{db_info['user_id']}`")
                st.write(f"• 短期记忆上限: {db_info['max_short_term_rounds']} 轮")
                
                # 检查数据库文件是否存在
                if os.path.exists(db_info['db_path']):
                    file_size = os.path.getsize(db_info['db_path'])
                    st.write(f"✅ 数据库文件存在 ({file_size} 字节)")
                else:
                    st.write("❌ 数据库文件不存在")
                
                # 显示记忆更新历史
                with st.expander("📊 记忆更新历史", expanded=False):
                    updates = st.session_state.agent.memory_room.get_memory_updates_history(limit=5)
                    if updates:
                        for update in updates:
                            st.write(f"• **{update['update_type']}**: {update['description']} ({update['data_count']} 条数据)")
                            st.write(f"  _时间: {update['created_at']}_")
                            st.divider()
                    else:
                        st.write("暂无更新历史")
    
    # 主界面
    if st.session_state.current_user is None:
        # 用户未登录，显示欢迎界面
        st.markdown("## 👋 欢迎使用小王子记忆架构系统")
        st.markdown("""
        ### 🚀 系统特色
        - **智能记忆管理**: 短期记忆 + 长期记忆的智能转换
        - **个性化体验**: 每个用户都有独立的记忆空间
        - **多模型支持**: 支持OpenAI和DeepSeek等多种LLM
        - **实时对话**: 流畅的聊天体验
        
        ### 📝 使用说明
        1. 在左侧边栏输入您的用户名
        2. 点击"登录/注册"按钮
        3. 配置您的API密钥
        4. 开始与小王子对话吧！
        
        ### 🔧 技术架构
        - **记忆系统**: SQLite数据库存储，支持多用户隔离
        - **LLM集成**: LangChain框架，支持多模型切换
        - **用户管理**: 无密码登录，自动分配唯一ID
        - **界面**: Streamlit构建，响应式设计
        """)
        
        # 显示系统统计
        user_stats = st.session_state.user_manager.get_user_stats()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("总用户数", user_stats['total_users'])
        with col2:
            st.metric("今日新增", user_stats['new_users_today'])
        with col3:
            st.metric("今日活跃", user_stats['active_users_today'])
        with col4:
            st.metric("在线用户", user_stats['online_users'])
    
    else:
        # 用户已登录，显示聊天界面
        user = st.session_state.current_user
        
        # 显示用户信息
        st.markdown(f"### 👤 当前用户: {user['username']}")
        
        # 显示记忆统计
        if st.session_state.agent:
            stats = st.session_state.agent.get_memory_stats()
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("短期记忆", stats['short_term_count'])
            with col2:
                st.metric("事实记忆", stats['long_term_factual_count'])
            with col3:
                st.metric("情节记忆", stats['long_term_episodic_count'])
            with col4:
                st.metric("语义记忆", stats['long_term_semantic_count'])
        
        # 聊天界面
        st.markdown("---")
        st.subheader("💬 与小王子对话")
        
        # 显示聊天历史
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # 聊天输入
        if prompt := st.chat_input("输入您的消息..."):
            # 添加用户消息
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # 生成AI回复
            with st.chat_message("assistant"):
                with st.spinner("小王子正在思考..."):
                    if st.session_state.agent:
                        response = st.session_state.agent.chat(prompt)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    else:
                        st.error("Agent未初始化，请检查配置")
        
        # 显示系统信息
        st.markdown("---")
        st.subheader("📊 系统信息")
        
        if st.session_state.agent:
            # 显示当前Prompt信息
            prompt_info = st.session_state.agent.get_current_prompt_info()
            st.write(f"**当前Prompt:** {prompt_info['name']}")
            
            # 显示记忆详情
            with st.expander("📚 记忆详情", expanded=False):
                short_term_memory = st.session_state.agent.memory_room.get_short_term_memory()
                long_term_memory = st.session_state.agent.memory_room.get_long_term_memory()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**短期记忆 (最近对话):**")
                    if short_term_memory:
                        for i, memory in enumerate(short_term_memory[-5:], 1):
                            st.write(f"{i}. **用户:** {memory['user'][:50]}...")
                            st.write(f"   **AI:** {memory['ai'][:50]}...")
                            st.write("---")
                    else:
                        st.write("暂无短期记忆")
                
                with col2:
                    st.markdown("**长期记忆:**")
                    if long_term_memory['factual']:
                        st.write("**事实记忆:**")
                        for key, value in long_term_memory['factual'].items():
                            st.write(f"• {key}: {value}")
                    
                    if long_term_memory['episodic']:
                        st.write("**情节记忆:**")
                        for episode in long_term_memory['episodic'][:3]:
                            st.write(f"• {episode.get('content', '')[:50]}...")
                    
                    if long_term_memory['semantic']:
                        st.write("**语义记忆:**")
                        for key, value in long_term_memory['semantic'].items():
                            st.write(f"• {key}: {value}")


if __name__ == "__main__":
    main()

# Streamlit Demo 使用说明

## 🚀 快速启动

1. **启动应用**
   ```bash
   python run_streamlit.py
   ```

2. **在浏览器中打开**
   - 应用会自动在浏览器中打开：http://localhost:8501
   - 如果没有自动打开，请手动访问该地址

## 🔑 API配置

### 方式一：自动加载本地配置（推荐）

如果您已经有 `.env` 文件配置：

1. **自动检测**
   - 系统会自动检测并加载 `.env` 文件中的配置
   - 左侧边栏会显示 "✅ 检测到本地.env配置"

2. **一键初始化**
   - 点击 "🚀 使用本地配置初始化" 按钮
   - 系统会自动使用您的本地配置启动

### 方式二：手动配置

如果没有 `.env` 文件或需要修改配置：

1. **选择LLM提供商**
   - 在左侧边栏选择 "openai" 或 "deepseek"

2. **选择模型**
   - **OpenAI模型**：
     - `gpt-4o-mini` (推荐，快速且经济)
     - `gpt-4o` (最新大模型)
     - `gpt-5` (最新大模型)
     - `gpt-5-mini` (轻量级)

   - **DeepSeek模型**：
     - `deepseek-chat` (通用对话)
     - `deepseek-reasoner` (推理专用)

3. **输入API密钥**
   - 在密码输入框中输入您的API密钥
   - OpenAI: 从 https://platform.openai.com/account/api-keys 获取
   - DeepSeek: 从 https://platform.deepseek.com/ 获取

4. **手动初始化**
   - 点击 "🔧 手动初始化系统" 按钮

### .env文件配置示例

```env
# LLM配置
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
LLM_API_KEY=your_openai_api_key_here

# 如果使用DeepSeek
# LLM_PROVIDER=deepseek
# LLM_MODEL=deepseek-chat
# DEEPSEEK_API_KEY=your_deepseek_api_key_here

# 记忆配置
SHORT_TERM_MAX_ROUNDS=10
MEMORY_UPDATE_INTERVAL=10

# 系统配置
LOG_LEVEL=INFO
TEMPERATURE=0.7
```

## 💬 开始对话

1. **查看记忆状态**
   - 顶部显示对话轮数、短期记忆、长期记忆、记忆更新轮数

2. **开始聊天**
   - 在底部聊天框中输入消息
   - 点击发送或按回车键

3. **观察记忆变化**
   - 短期记忆会实时更新
   - 每10轮对话后会自动更新长期记忆

## ⚙️ 系统控制

### 侧边栏功能

- **🗑️ 清空聊天历史**：清除所有对话记录
- **🔄 重置记忆**：清空所有记忆，重新开始
- **📊 系统信息**：显示当前配置信息

### 详细记忆信息

- 点击 "📚 详细记忆信息" 展开查看：
  - **短期记忆详情**：最近N轮对话
  - **长期记忆详情**：事实记忆、情节记忆、语义记忆

## 🔧 故障排除

### 常见问题

1. **初始化失败**
   - 检查API密钥是否正确
   - 确认网络连接正常
   - 查看错误信息并相应处理

2. **对话无响应**
   - 检查API密钥余额
   - 确认模型选择正确
   - 查看控制台错误信息

3. **记忆不更新**
   - 确认对话轮数达到更新阈值（默认10轮）
   - 检查记忆更新机制是否正常工作

4. **端口被占用**
   - 如果8501端口被占用，可以手动指定其他端口：
   ```bash
   streamlit run streamlit_demo.py --server.port 8502
   ```

### 获取API密钥

- **OpenAI**: https://platform.openai.com/account/api-keys
- **DeepSeek**: https://platform.deepseek.com/

## 📝 使用建议

1. **首次对话**
   - 尝试简单的问候："你好"
   - 介绍自己："我叫小明，我喜欢编程"

2. **测试记忆功能**
   - 告诉AI一些个人信息
   - 在后续对话中询问："你还记得我吗？"

3. **观察记忆更新**
   - 进行10轮对话后观察长期记忆的变化
   - 查看详细记忆信息了解记忆结构

## 🎯 功能特点

- **自动配置检测**：自动加载本地.env文件配置
- **实时记忆显示**：对话轮数、短期记忆、长期记忆统计
- **智能记忆管理**：自动将短期记忆总结为长期记忆
- **多模型支持**：支持OpenAI和DeepSeek多种模型
- **记忆可视化**：详细展示记忆结构和内容
- **交互式控制**：实时重置和清空功能

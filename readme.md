# 🌹 小王子记忆架构系统 (Little Prince Memory Architecture System)

![小王子记忆架构系统](resources/picture/MemoryRepositoryforLittlePrice.svg)

## 📖 项目简介

小王子记忆架构系统是一个基于AI Agent的智能对话系统，实现了创新的记忆管理机制。系统通过短期记忆和长期记忆的智能转换，为用户提供个性化的对话体验，同时支持多用户数据隔离和隐私保护。

## 🚀 核心特性

### 🧠 智能记忆架构
- **短期记忆**: 存储最近的对话历史，支持固定轮数限制
- **长期记忆**: 结构化存储，包含事实记忆、情节记忆、语义记忆
- **记忆更新机制**: 自动将短期记忆总结为长期记忆
- **记忆交互**: 智能检索和格式化记忆上下文

### 👥 多用户支持
- **用户管理系统**: 无密码登录，自动分配唯一UUID
- **数据隔离**: 每个用户拥有独立的记忆空间
- **会话管理**: 支持用户会话跟踪和统计
- **隐私保护**: 明确的数据存储位置和访问权限说明

### 🔧 技术架构
- **LLM集成**: 支持OpenAI和DeepSeek等多种模型
- **LangChain框架**: 灵活的模型切换和提示词管理
- **SQLite数据库**: 持久化存储，支持多用户数据隔离
- **Streamlit界面**: 现代化的Web用户界面

## 🏗️ 系统架构

### 核心组件

```
LittlePrinceAgent
├── LLMInterface (LLM接口)
├── MemoryRoom (记忆房间)
│   ├── MemoryDatabase (SQLite数据库)
│   └── MemoryInteraction (记忆交互)
├── MemoryUpdateMechanism (记忆更新机制)
├── PromptManager (提示词管理)
└── UserManager (用户管理)
```

### 记忆系统设计

#### 短期记忆 (Short-term Memory)
- **存储内容**: 原始对话历史
- **轮数限制**: 可配置的最大轮数（默认20轮）
- **更新频率**: 实时更新
- **存储方式**: SQLite数据库

#### 长期记忆 (Long-term Memory)
- **事实记忆 (Factual Memory)**
  - 用户身份信息（姓名、昵称、偏好称呼）
  - 喜好与厌恶（食物、天气、颜色、动物等）
  - 兴趣与习惯（爱好、日常作息、生活方式）
  - 重要人物（家人、朋友、宠物）
  - 禁忌话题（用户不喜欢或避免谈论的内容）

- **情节记忆 (Episodic Memory)**
  - 用户经历（考试、旅行、个人里程碑）
  - 情感亮点（对话中的情感时刻）
  - 共享记忆（与AI的承诺、计划、有趣事件）
  - 特殊时刻（用户分享的惊喜和快乐）
  - 怀旧故事（过去、童年回忆）

- **语义记忆 (Semantic Memory)**
  - 价值观（对幸福、爱情、成长的看法）
  - 核心主题（重复的情感模式、人生信念）
  - 长期目标与抱负（想成为的人、追求的生活）

## 🛠️ 安装和配置

### 环境要求
- Python 3.8+
- SQLite 3
- 网络连接（用于LLM API调用）

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd memoryrepository
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，添加您的API密钥
```

4. **启动应用**
```bash
streamlit run streamlit_demo.py --server.port 8506
```

### 环境变量配置

```bash
# LLM配置
LLM_PROVIDER=openai  # 可选: openai, deepseek
LLM_MODEL=gpt-4o-mini  # OpenAI模型: gpt-4o-mini, gpt-4o, gpt-3.5-turbo, gpt-4, gpt-4-turbo | DeepSeek模型: deepseek-chat, deepseek-coder, deepseek-llm-7b-chat
LLM_API_KEY=your_openai_api_key_here

# DeepSeek配置（如果使用DeepSeek）
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# 记忆系统配置
MEMORY_UPDATE_INTERVAL=10  # 记忆更新间隔（轮数）
SHORT_TERM_MAX_ROUNDS=20   # 短期记忆最大轮数

# Prompt查看密码
PROMPT_VIEW_PASSWORD=admin123  # 查看Prompt详情所需的密码
```

## 🎯 使用指南

### 快速开始

1. **访问系统**: 打开浏览器访问 `http://localhost:8506`

2. **用户登录**: 在侧边栏输入用户名，点击"登录/注册"

3. **配置API**: 在侧边栏配置您的LLM API密钥

4. **开始对话**: 在聊天框中输入消息，开始与小王子对话

### 功能说明

#### 🔑 API配置
- 支持OpenAI和DeepSeek多种LLM提供商
- 动态模型切换
- 本地.env文件配置支持

#### 🎭 Prompt管理
- 查看当前Prompt信息
- 切换不同的Prompt配置
- 密码保护的Prompt详情查看

#### 💾 记忆管理
- 实时显示记忆统计
- 导出记忆数据
- 清空记忆功能
- 查看记忆更新历史

#### 👤 用户管理
- 无密码登录系统
- 用户数据隔离
- 用户统计信息
- 会话管理

#### 🔒 隐私保护
- 数据存储位置说明
- 隐私风险提醒
- 数据访问权限说明
- 隐私保护建议

## 📊 系统功能

### 已实现功能 ✅

#### 核心功能
- [x] AI Agent基础架构
- [x] 短期记忆管理
- [x] 长期记忆管理
- [x] 记忆更新机制
- [x] 记忆交互模块

#### 用户界面
- [x] Streamlit Web界面
- [x] 实时聊天功能
- [x] 记忆统计显示
- [x] 系统配置界面
- [x] 响应式设计

#### 用户管理
- [x] 多用户支持
- [x] 数据隔离
- [x] 用户登录系统
- [x] 会话管理
- [x] 用户统计

#### 数据存储
- [x] SQLite数据库
- [x] 数据持久化
- [x] 多用户数据隔离
- [x] 数据导出功能
- [x] 记忆更新历史

#### LLM集成
- [x] OpenAI API支持
- [x] DeepSeek API支持
- [x] 动态模型切换
- [x] LangChain框架集成
- [x] 多模型支持

#### 隐私保护
- [x] 数据存储位置说明
- [x] 隐私风险提醒
- [x] 访问权限说明
- [x] 隐私保护建议

### 待实现功能 🚧

#### 高级功能
- [ ] 工具集成 (MCP, Function Call)
- [ ] 知识库集成 (RAG, Vector Database)
- [ ] 多阶段Prompt系统
- [ ] 记忆可视化
- [ ] 性能优化

#### 部署功能
- [ ] 云端数据库支持
- [ ] 数据加密
- [ ] 访问控制
- [ ] 数据匿名化
- [ ] 生产环境部署

## 🔧 技术栈

### 后端技术
- **Python 3.8+**: 主要开发语言
- **LangChain**: LLM集成框架
- **SQLite**: 数据存储
- **Pydantic**: 数据验证
- **Loguru**: 日志管理

### 前端技术
- **Streamlit**: Web界面框架
- **HTML/CSS**: 界面样式
- **JavaScript**: 交互功能

### 外部服务
- **OpenAI API**: GPT模型服务
- **DeepSeek API**: DeepSeek模型服务

## 📁 项目结构

```
memoryrepository/
├── core/                          # 核心模块
│   ├── __init__.py
│   ├── agent.py                   # AI Agent主类
│   ├── llm.py                     # LLM接口
│   ├── user_manager.py            # 用户管理
│   └── memory/                    # 记忆系统
│       ├── __init__.py
│       ├── memory_room.py         # 记忆房间
│       ├── memory_database.py     # 数据库操作
│       ├── memory_interaction.py  # 记忆交互
│       └── memory_update_mechanism.py  # 记忆更新机制
├── config/                        # 配置模块
│   ├── __init__.py
│   ├── settings.py                # 系统配置
│   ├── prompt_manager.py          # 提示词管理
│   └── prompts_config.yaml        # 提示词配置
├── utils/                         # 工具模块
│   └── logger.py                  # 日志工具
├── examples/                      # 示例代码
├── tests/                         # 测试代码
├── logs/                          # 日志文件
├── data/                          # 数据文件
│   ├── users.db                   # 用户数据库
│   └── memory.db                  # 记忆数据库
├── resources/                     # 资源文件
│   └── picture/                   # 图片资源
├── streamlit_demo.py              # Streamlit主应用
├── run_streamlit.py               # 启动脚本
├── requirements.txt               # 依赖包
├── .env.example                   # 环境变量示例
├── readme.md                      # 项目文档
├── DEPLOYMENT_GUIDE.md            # 部署指南
└── STREAMLIT_USAGE.md             # 使用说明
```

## 🔒 隐私和安全

### 数据存储
- **本地部署**: 数据存储在本地SQLite数据库
- **云端部署**: 支持云端数据库服务
- **数据隔离**: 每个用户数据完全独立

### 隐私保护
- **数据加密**: 支持敏感数据加密
- **访问控制**: 基于角色的权限管理
- **数据匿名化**: 支持用户数据匿名化处理
- **隐私声明**: 明确的数据使用说明

### 安全建议
1. 使用强密码保护Prompt查看功能
2. 定期备份用户数据
3. 在生产环境中使用云端数据库
4. 实施数据加密和访问控制

## 🚀 部署指南

### 本地部署
```bash
# 开发测试环境
streamlit run streamlit_demo.py --server.port 8506
```

### 云端部署
```bash
# Streamlit Cloud部署
# 1. 上传到GitHub
# 2. 在Streamlit Cloud连接仓库
# 3. 配置环境变量
# 4. 部署应用
```

### 生产环境部署
- 使用云端数据库服务（MongoDB Atlas, PostgreSQL）
- 实施数据加密和访问控制
- 配置负载均衡和监控
- 定期备份和恢复测试

详细部署说明请参考 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 📈 性能指标

### 系统性能
- **响应时间**: < 3秒（取决于LLM API）
- **并发用户**: 支持多用户同时使用
- **数据存储**: SQLite数据库，支持GB级数据
- **内存使用**: 优化的内存管理

### 用户体验
- **界面响应**: 实时更新
- **数据持久化**: 自动保存
- **错误处理**: 友好的错误提示
- **多语言支持**: 中文界面

## 🤝 贡献指南

### 开发环境设置
1. Fork项目
2. 创建功能分支
3. 提交代码
4. 创建Pull Request

### 代码规范
- 遵循PEP 8代码风格
- 添加适当的注释和文档
- 编写单元测试
- 更新相关文档

### 测试
```bash
# 运行测试
python -m pytest tests/

# 运行特定测试
python test_user_management.py
python test_sqlite_memory_storage.py
```

## 📝 更新日志

### v1.0.0 (2024-08-18)
#### 🎉 重大更新
- ✅ 实现完整的AI Agent架构
- ✅ 添加用户管理系统
- ✅ 集成SQLite数据库
- ✅ 实现记忆更新机制
- ✅ 添加隐私保护功能

#### 🔧 技术改进
- 重构LLM集成，使用LangChain框架
- 优化记忆系统架构
- 改进用户界面设计
- 增强错误处理机制

#### 🛡️ 安全增强
- 添加数据隐私保护
- 实现用户数据隔离
- 增加访问控制机制
- 提供隐私风险提醒

#### 📊 功能完善
- 支持多用户并发使用
- 添加记忆统计和可视化
- 实现Prompt管理系统
- 提供数据导出功能

## 📞 技术支持

### 常见问题
1. **API密钥配置**: 确保在.env文件中正确配置API密钥
2. **数据库问题**: 检查data目录权限和SQLite文件
3. **端口冲突**: 使用不同端口启动应用
4. **内存不足**: 调整短期记忆轮数限制

### 获取帮助
- 查看 [STREAMLIT_USAGE.md](STREAMLIT_USAGE.md) 使用说明
- 参考 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) 部署指南
- 提交Issue报告问题
- 参与项目讨论

## 📄 许可证

禁止修改和商用,仅供查看

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户！

---

**🌹 小王子记忆架构系统** - 让AI拥有真正的记忆，让对话更有温度。

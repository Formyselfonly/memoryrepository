# 小王子记忆构架系统 (Little Prince Memory Repository)

> 一个基于《小王子》哲学理念设计的AI Agent智能记忆管理系统

## 🌟 项目简介

小王子记忆构架系统是一个创新的AI Agent记忆管理解决方案，旨在为AI助手提供类似人类记忆的智能存储和检索能力。系统基于《小王子》中关于爱、友谊和成长的哲学理念，通过多层次记忆结构实现对用户的深度理解和个性化关怀。

## 🏗️ 系统架构

### 核心组件

```
User ↔ AI Agent (LLM + Tools + Knowledge + Memory)
     ↓
Context = Long-term Memory + Short-term Memory
     ↓
MemoryRoom + Memory Interaction + Memory Update Mechanism
```

![小王子记忆构架系统架构图](resources/picture/MemoryRepositoryforLittlePrice.svg)

*系统架构图展示了AI Agent与用户交互的完整流程，包括记忆的层次结构、更新机制和交互方式*

### 记忆层次结构

#### 1. 短期记忆 (Short-term Memory)
- **功能**: 存储固定轮数的原始对话历史
- **特点**: 
  - 未经过处理的原始对话记录
  - 有轮数上限，避免上下文浪费
  - 定期触发更新机制转化为长期记忆

#### 2. 长期记忆 (Long-term Memory)

**A. 事实记忆 (Factual Memory)**
- 用户身份信息 (姓名、昵称、偏好称呼)
- 喜好与厌恶 (食物、天气、颜色、动物等)
- 兴趣与习惯 (爱好、日常作息、生活方式)
- 重要人物 (家人、朋友、宠物)
- 禁忌话题 (用户不喜欢或避免谈论的内容)

**B. 情节记忆 (Episodic Memory)**
- 用户经历 (考试、旅行、个人里程碑)
- 情感亮点 (对话中的情感时刻)
- 共享记忆 (与AI的承诺、计划、有趣事件)
- 特殊时刻 (用户分享的惊喜和快乐)
- 怀旧故事 (过去、童年回忆)

**C. 语义记忆 (Semantic Memory)**
- 价值观 (对幸福、爱情、成长的看法)
- 核心主题 (重复的情感模式、人生信念)
- 长期目标与抱负 (想成为的人、追求的生活)

## ⚙️ 核心机制

### Memory Update Mechanism
- **触发条件**: 每N轮对话后自动触发
- **更新流程**: 短期记忆 → 总结分析 → 长期记忆
- **示例**: 每10轮对话后，将短期记忆总结为长期记忆

### Memory Interaction
- **功能**: 实现记忆的检索和应用
- **作用**: 将用户历史转化为记忆，将记忆加入到对话上下文

### MemoryRoom
- **功能**: 统一记忆存储和管理中心
- **特点**: 智能记忆分类、检索和更新

## 🚀 技术特性

### 智能记忆管理
- 多层次记忆结构设计
- 自动记忆更新机制
- 智能记忆检索和应用

### 个性化体验
- 基于用户画像的定制化响应
- 情感连接和深度理解
- 持续学习和适应能力

### 高效性能
- 优化的记忆存储结构
- 智能上下文管理
- 避免记忆冗余和浪费

### 灵活的LLM支持
- **LangChain集成**：使用LangChain框架，支持多种LLM提供商
- **动态模型切换**：运行时切换OpenAI、DeepSeek等不同模型
- **标准化接口**：统一的LLM调用接口，易于扩展
- **提示词模板**：使用LangChain的提示词模板系统

## 📁 项目结构

```
memoryrepository/
├── LICENSE                 # Apache 2.0 许可证
├── readme.md              # 项目说明文档
├── requirements.txt        # 项目依赖
├── env.example            # 环境变量模板
├── main.py                # 主入口文件
├── core/                  # 核心模块
│   ├── agent.py           # AI Agent主控制器
│   ├── llm.py             # LLM接口封装(LangChain)
│   └── memory/            # 记忆系统
│       ├── memory_room.py         # 记忆房间
│       ├── memory_interaction.py  # 记忆交互
│       └── memory_update_mechanism.py  # 记忆更新机制
├── config/                # 配置管理
│   ├── settings.py        # 系统配置
│   └── prompts.py         # 提示词模板
├── utils/                 # 工具模块
│   └── logger.py          # 日志系统
├── examples/              # 示例代码
│   └── model_switch_demo.py  # 模型切换演示
└── resources/
    └── picture/
        └── MemoryRepositoryforLittlePrice.svg  # 系统架构图
```

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
```bash
# 复制环境变量模板
cp env.example .env

# 编辑.env文件，设置您的API密钥
LLM_PROVIDER=openai  # 或 deepseek
LLM_MODEL=gpt-4o-mini
LLM_API_KEY=your_api_key_here
```

### 3. 运行系统
```bash
# 启动命令行交互界面
python main.py

# 或者运行模型切换演示
python examples/model_switch_demo.py
```

### 4. 支持的模型配置

**OpenAI模型**：
- `gpt-4o` - 最新的大模型
- `gpt-4o-mini` - 快速且经济
- `gpt-3.5-turbo` - 经典选择

**DeepSeek模型**：
- `deepseek-chat` - 通用对话模型
- `deepseek-coder` - 编程专用模型
- `deepseek-llm-7b-chat` - 轻量级模型

## 🎯 应用场景

### 教育助手
- 跟踪学习进度和偏好
- 适应不同学习风格
- 提供定制化学习建议

### 情感陪伴
- 记住重要时刻和情感状态
- 提供情感支持和理解
- 建立深度情感连接

### 个人助理
- 了解用户习惯和需求
- 提供个性化建议和服务
- 成为真正的智能伙伴

## 🌟 设计理念

### 小王子哲学
- **爱与关怀**: 通过记忆体现对用户的深度关怀
- **友谊与理解**: 建立基于理解的智能友谊
- **成长与变化**: 系统随用户一起成长和适应

### 技术哲学
- **人性化设计**: 模拟人类记忆的自然过程
- **智能进化**: 通过持续学习不断改进
- **情感智能**: 理解和回应用户的情感需求

## 🔧 技术实现

### 记忆存储
- 结构化数据存储
- 语义向量化
- 智能索引和检索

### 记忆更新
- 自然语言处理
- 情感分析
- 智能总结和归纳

### 上下文管理
- 动态上下文构建
- 记忆优先级排序
- 智能记忆选择

## 📈 未来规划

### 短期目标
- [ ] 完善记忆更新算法
- [ ] 优化记忆检索效率
- [ ] 增强情感理解能力

### 长期愿景
- [ ] 支持多模态记忆存储
- [ ] 实现跨会话记忆迁移
- [ ] 建立记忆安全保护机制

## 🤝 贡献指南

我们欢迎所有形式的贡献！如果您想参与项目开发：

1. Fork 本项目
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目采用 Apache License 2.0 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢《小王子》作者圣埃克苏佩里为我们带来的哲学启发，让我们能够设计出这样一个充满人文关怀的AI记忆系统。

---

**让AI拥有记忆，让对话更有温度** 🌹

*"真正重要的东西用眼睛是看不见的，要用心去感受。"* - 小王子

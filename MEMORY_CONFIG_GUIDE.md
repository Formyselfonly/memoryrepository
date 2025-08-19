# 记忆系统配置调整指南

## 📊 可调整的参数

### 1. `SHORT_TERM_MAX_ROUNDS` - 短期记忆最大轮数
**作用**：控制短期记忆最多保存多少轮对话

**推荐配置**：
- **5轮**：快速测试，频繁更新
- **10轮**：平衡选择（推荐）
- **15-20轮**：长对话，复杂上下文

### 2. `MEMORY_UPDATE_INTERVAL` - 记忆更新间隔
**作用**：每多少轮对话触发一次长期记忆更新

**推荐配置**：
- **5轮**：频繁更新，实时记忆
- **10轮**：平衡选择（推荐）
- **15-20轮**：批量更新，节省API

## 🔧 如何调整

### 方法1：修改 `.env` 文件
```bash
# 快速测试配置
SHORT_TERM_MAX_ROUNDS=5
MEMORY_UPDATE_INTERVAL=5

# 平衡配置（推荐）
SHORT_TERM_MAX_ROUNDS=10
MEMORY_UPDATE_INTERVAL=10

# 长对话配置
SHORT_TERM_MAX_ROUNDS=15
MEMORY_UPDATE_INTERVAL=15
```

### 方法2：修改 `config/settings.py`
```python
class Config(BaseSettings):
    # 记忆配置
    SHORT_TERM_MAX_ROUNDS: int = 5  # 改为你想要的轮数
    MEMORY_UPDATE_INTERVAL: int = 5  # 改为你想要的间隔
```

## 📈 不同配置的效果

### 快速测试配置 (5/5)
- ✅ 快速看到记忆更新效果
- ✅ 适合开发和调试
- ❌ API调用较频繁
- ❌ 可能丢失上下文

### 平衡配置 (10/10) - 推荐
- ✅ 良好的上下文保持
- ✅ 合理的更新频率
- ✅ 适合大多数使用场景

### 长对话配置 (15/15)
- ✅ 保持更长的对话上下文
- ✅ 减少API调用
- ❌ 记忆更新较慢
- ❌ 可能错过重要信息

## 🎯 使用建议

1. **开发测试时**：使用 5/5 配置
2. **日常使用**：使用 10/10 配置
3. **长对话场景**：使用 15/15 配置
4. **根据API预算**：调整 `MEMORY_UPDATE_INTERVAL`

## ⚠️ 注意事项

1. **`SHORT_TERM_MAX_ROUNDS` 应该 >= `MEMORY_UPDATE_INTERVAL`**
2. 调整后需要重启应用才能生效
3. 较小的值会增加API调用频率
4. 较大的值可能影响记忆的及时性

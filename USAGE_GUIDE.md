# GenAI Code Usage Monitor - 使用指南

## 🚀 快速启动

### 方法 1: 使用启动脚本（推荐）

```bash
cd /Users/bytedance/genai-code-usage-monitor
./start_monitor.sh
```

### 方法 2: 手动启动

```bash
cd /Users/bytedance/genai-code-usage-monitor
source venv/bin/activate
PYTHONPATH=$(pwd)/src python -m genai_code_usage_monitor
```

### 方法 3: 使用别名（设置后）

```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
alias genai-code-usage-monitor='cd /Users/bytedance/genai-code-usage-monitor && ./start_monitor.sh'

# 使用
genai-code-usage-monitor
```

---

## 📊 监控界面说明

启动后，你会看到：

```
╭──────────────────────────────────────╮
│ GenAI Code Usage Monitor                  │  ← 头部标题
│ Plan: custom | Time: 2025-01-27...  │
╰──────────────────────────────────────╯

╭────── Usage Statistics ──────╮
│ Daily Usage:                 │
│ Tokens: 0 / unlimited       │  ← Token 使用量
│ Cost: $0.00 / $50.00        │  ← 成本统计
│ API Calls: 0                │  ← API 调用次数
╰──────────────────────────────╯

       Model Usage
┏━━━━━━━┳━━━━━━━━┳━━━━━━┓
┃ Model ┃ Tokens ┃ Cost ┃  ← 模型使用统计
┡━━━━━━━╇━━━━━━━━╇━━━━━━┩
└───────┴────────┴──────┘
```

界面会自动刷新，实时显示使用情况！

---

## 🎛️ 常用命令选项

### 基础使用

```bash
# 默认配置（custom 计划）
./start_monitor.sh

# 使用 Pay-as-you-go 计划
./start_monitor.sh --plan payg

# 设置自定义 Token 限额
./start_monitor.sh --plan custom --custom-limit-tokens 100000

# 设置成本限额
./start_monitor.sh --plan custom --custom-limit-cost 25.0
```

### 显示选项

```bash
# 使用深色主题
./start_monitor.sh --theme dark

# 每日视图
./start_monitor.sh --view daily

# 月度视图
./start_monitor.sh --view monthly

# 更快的刷新率（3秒）
./start_monitor.sh --refresh-rate 3
```

### 时区和时间

```bash
# 使用上海时区
./start_monitor.sh --timezone Asia/Shanghai

# 使用 24 小时格式
./start_monitor.sh --time-format 24h

# 设置每日重置时间为早上 9 点
./start_monitor.sh --reset-hour 9
```

### 日志和调试

```bash
# 启用调试模式
./start_monitor.sh --debug

# 记录日志到文件
./start_monitor.sh --log-file monitor.log

# 设置日志级别
./start_monitor.sh --log-level DEBUG
```

---

## 💡 实用场景

### 场景 1: 开发时实时监控

```bash
# 在一个终端窗口启动监控
./start_monitor.sh --refresh-rate 5

# 在另一个终端窗口进行开发
# 监控器会实时显示 API 使用情况
```

### 场景 2: 预算控制

```bash
# 设置每日预算限制
./start_monitor.sh --plan custom \
  --custom-limit-cost 10.0 \
  --refresh-rate 3

# 当接近限额时，会显示警告
```

### 场景 3: 团队使用报告

```bash
# 生成每日使用报告
./start_monitor.sh --view daily \
  --log-file daily-report-$(date +%Y%m%d).log
```

### 场景 4: 国际团队

```bash
# 适配不同时区
./start_monitor.sh --timezone America/New_York \
  --time-format 12h \
  --reset-hour 9
```

---

## 📈 监控 API 调用

### 编程方式记录使用

```python
from genai_code_usage_monitor.data.api_client import UsageTracker
from pathlib import Path

# 初始化追踪器
tracker = UsageTracker(Path.home() / ".genai-code-usage-monitor")

# 记录 API 调用
call = tracker.log_api_call(
    model="gpt-4",
    prompt_tokens=1000,
    completion_tokens=500
)

print(f"Cost: ${call.cost:.4f}")
```

### 在应用中集成

```python
import openai
from genai_code_usage_monitor.data.api_client import UsageTracker
from pathlib import Path

tracker = UsageTracker(Path.home() / ".genai-code-usage-monitor")

# 调用 OpenAI API
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)

# 记录使用
usage = response['usage']
tracker.log_api_call(
    model="gpt-4",
    prompt_tokens=usage['prompt_tokens'],
    completion_tokens=usage['completion_tokens']
)
```

---

## ⚙️ 配置文件

配置存储在 `~/.genai-code-usage-monitor/`:

- `last_used.json` - 保存的偏好设置
- `usage_log.jsonl` - 使用历史记录
- `cache/` - 缓存数据

### 清除配置

```bash
./start_monitor.sh --clear
```

---

## 🛑 停止监控

按 `Ctrl+C` 优雅退出监控器

---

## 📊 查看历史数据

```bash
# 查看今天的使用
cat ~/.genai-code-usage-monitor/usage_log.jsonl | tail -10

# 使用 jq 解析（如果已安装）
cat ~/.genai-code-usage-monitor/usage_log.jsonl | jq '.cost' | \
  awk '{sum+=$1} END {print "Total cost: $"sum}'
```

---

## 💡 提示和技巧

### 1. 后台运行

```bash
# 在后台启动监控
nohup ./start_monitor.sh > monitor.out 2>&1 &

# 查看输出
tail -f monitor.out
```

### 2. tmux 集成

```bash
# 在 tmux 会话中运行
tmux new-session -d -s genai-code-usage-monitor './start_monitor.sh'

# 查看会话
tmux attach -t genai-code-usage-monitor
```

### 3. 自定义警报

```bash
# 当成本超过阈值时通知
./start_monitor.sh --log-file /tmp/monitor.log &
tail -f /tmp/monitor.log | grep -i "warning\|critical" | \
  while read line; do
    osascript -e "display notification \"$line\" with title \"GenAI Code Usage Monitor\""
  done
```

---

## 🔧 故障排除

### 问题: 命令未找到

```bash
# 确保在正确的目录
cd /Users/bytedance/genai-code-usage-monitor

# 检查脚本权限
ls -l start_monitor.sh
# 应该显示 -rwxr-xr-x

# 如果没有执行权限
chmod +x start_monitor.sh
```

### 问题: 导入错误

```bash
# 激活虚拟环境
source venv/bin/activate

# 确认依赖已安装
pip list | grep -E "pydantic|rich|numpy"
```

### 问题: 配置问题

```bash
# 清除配置并重新开始
./start_monitor.sh --clear
./start_monitor.sh
```

---

## 📚 更多信息

- **完整文档**: [README.md](README.md)
- **快速入门**: [QUICKSTART.md](QUICKSTART.md)
- **API 文档**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- **测试报告**: [INSTALLATION_TEST_REPORT.md](INSTALLATION_TEST_REPORT.md)

---

## 🆘 获取帮助

```bash
./start_monitor.sh --help
```

显示所有可用选项和说明。

---

**享受使用 GenAI Code Usage Monitor！** 🎉

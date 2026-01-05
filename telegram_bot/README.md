# Telegram Traffic Flow Bot

一个用于查询 Wgetcloud 流量使用情况的 Telegram 机器人。

## 功能特性

- 查询 Wgetcloud 流量使用情况
- 显示今日流量消耗
- 消息回显功能

## 环境要求

- Python 3.7+
- pip (Python 包管理器)

## 安装步骤

1. 克隆或下载本项目到本地

2. 安装依赖包：
```bash
pip install python-telegram-bot
```

3. 创建配置文件 `config.json`：
```json
{
  "TG_TOKEN": "your_telegram_bot_token",
  "WG_TOKEN": "your_wgetcloud_api_token",
  "WG_COOKIE": "your_wgetcloud_cookie"
}
```

## 配置说明

### 获取 Telegram Bot Token

1. 在 Telegram 中搜索 [@BotFather](https://t.me/botfather)
2. 发送 `/newbot` 命令创建新机器人
3. 按照提示设置机器人名称和用户名
4. 获取 API Token 并填入 `config.json` 的 `TOKEN` 字段

### 获取 Wgetcloud API Token

从你的 Wgetcloud 账户获取 API Token，并填入 `config.json` 的 `WG_TOKEN` 字段。

## 使用方法

### 启动机器人

使用默认配置文件（config.json）：
```bash
python -m telegram_bot.main
```

使用自定义配置文件：
```bash
python -m telegram_bot.main /path/to/your/config.json
```

### 机器人命令

| 命令 | 说明 |
|------|------|
| `/start` | 启动机器人，显示欢迎信息 |
| `/flow` | 查询当前流量使用情况 |
| 其他文本 | 机器人会回显你发送的消息 |

## 使用示例

1. 在 Telegram 中找到你的机器人
2. 发送 `/start` 查看欢迎信息
3. 发送 `/flow` 获取流量使用情况
4. 发送任意文本，机器人会回复 "You say: [你的消息]"

## 项目结构

```
.
├── main.py          # 主程序文件
├── config.json      # 配置文件（需自行创建）
└── README.md        # 项目说明文档
```

## 日志说明

程序运行时会在控制台输出日志信息，包括：
- 配置文件加载状态
- 消息处理记录
- 错误信息

日志格式：`时间 | 级别 | 文件:行号 | 消息内容`

## 注意事项

- 请妥善保管 `config.json` 文件，不要将其上传到公开仓库
- 建议将 `config.json` 添加到 `.gitignore` 文件中
- 确保服务器网络可以访问 Telegram API 和 Wgetcloud API

## 故障排除

### 配置文件找不到
确保 `config.json` 与 `main.py` 在同一目录下，或通过命令行参数指定正确的路径。

### 机器人无响应
检查 Telegram Bot Token 是否正确，以及网络连接是否正常。

### 流量查询失败
检查 Wgetcloud API Token 是否正确，以及 API 地址是否可访问。

## 许可证

请根据项目实际情况添加相应的开源许可证。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。
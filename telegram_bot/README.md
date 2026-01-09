# Telegram Traffic Flow Bot

一个用于查询 Wgetcloud 流量使用情况的 Telegram 机器人。

## 功能特性

- 多用户支持：每个用户使用自己的 Wgetcloud Cookie
- 查询 Wgetcloud 流量使用情况
- 显示今日流量消耗
- Cookie 管理：设置、更新、删除个人 Cookie
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
  "TG_TOKEN": "your_telegram_bot_token"
}
```

**注意**：从此版本开始，不再需要在配置文件中提供 `WG_COOKIE`。每个用户需要通过 Bot 命令自行设置自己的 Cookie。

## 配置说明

### 获取 Telegram Bot Token

1. 在 Telegram 中搜索 [@BotFather](https://t.me/botfather)
2. 发送 `/newbot` 命令创建新机器人
3. 按照提示设置机器人名称和用户名
4. 获取 API Token 并填入 `config.json` 的 `TG_TOKEN` 字段

### 获取 Wgetcloud Cookie

每个用户需要从自己的 Wgetcloud 账户获取 Cookie：

1. 登录 [Wgetcloud](https://wgetcloud.org) 网站
2. 打开浏览器开发者工具（按 F12 键）
3. 切换到 "Network"（网络）标签页
4. 刷新页面或进行任意操作
5. 在请求列表中选择任意请求，查看 Request Headers（请求头）
6. 复制 `Cookie` 字段的完整内容
7. 在 Telegram Bot 中使用 `/setcookie <复制的Cookie>` 命令设置

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
| `/start` | 启动机器人，显示欢迎信息和设置状态 |
| `/setcookie <cookie>` | 设置或更新你的 Wgetcloud Cookie |
| `/flow` | 查询当前流量使用情况 |
| `/removecookie` | 删除你的 Wgetcloud Cookie |
| 其他文本 | 机器人会回显你发送的消息 |

## 使用示例

### 首次使用

1. 在 Telegram 中找到你的机器人
2. 发送 `/start` 查看欢迎信息
3. 按照提示获取你的 Wgetcloud Cookie
4. 发送 `/setcookie <你的Cookie>` 设置 Cookie
5. 发送 `/flow` 获取流量使用情况

### 后续使用

- 发送 `/flow` 随时查询流量
- 如果 Cookie 过期，使用 `/setcookie <新Cookie>` 更新
- 如需删除数据，使用 `/removecookie`

## 项目结构

```
.
├── main.py              # 主程序文件
├── config.json          # 配置文件（需自行创建，仅包含 TG_TOKEN）
├── user_cookies.json    # 用户 Cookie 存储文件（自动生成，已加入 .gitignore）
└── README.md            # 项目说明文档
```

## 日志说明

程序运行时会在控制台输出日志信息，包括：
- 配置文件加载状态
- 消息处理记录
- 错误信息

日志格式：`时间 | 级别 | 文件:行号 | 消息内容`

## 注意事项

- 请妥善保管 `config.json` 文件，不要将其上传到公开仓库
- `user_cookies.json` 已自动加入 `.gitignore`，包含所有用户的 Cookie 数据
- 每个用户的 Cookie 仅存储在服务器本地，请确保服务器安全
- Cookie 可能会过期，过期后需要重新设置
- 确保服务器网络可以访问 Telegram API 和 Wgetcloud API
- 每个 Telegram 用户只能查询自己设置的 Cookie 对应的流量数据

## 故障排除

### 配置文件找不到
确保 `config.json` 与 `main.py` 在同一目录下，或通过命令行参数指定正确的路径。

### 机器人无响应
检查 Telegram Bot Token 是否正确，以及网络连接是否正常。

### 流量查询失败
- 检查你的 Wgetcloud Cookie 是否正确
- Cookie 可能已过期，尝试重新获取并使用 `/setcookie` 更新
- 确认 Wgetcloud API 地址是否可访问

### 首次使用提示设置 Cookie
这是正常的！每个用户首次使用都需要设置自己的 Cookie。按照 `/start` 命令的提示获取并设置即可。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

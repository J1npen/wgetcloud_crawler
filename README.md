# 🚀 wgetcloud\_crawler

一个围绕 **Wgetcloud 流量使用情况查询** 构建的自动化项目集合，包含：

- 🌐 **HTTP API 服务**（供程序 / VPS / 手机调用）
- 🤖 **Telegram Bot**（通过聊天指令查询流量）

适用于：\
**自用流量监控、自动化提醒、脚本集成、Telegram 查询等场景**

> ⚠️ 说明：\
> Wgetcloud 为境外流量服务提供商，本项目仅用于 **用户本人账户的自动化查询**，不涉及任何破解或越权行为。

---

## 📄 您需要准备的所有东西
1. Wgetcloud Cookie
2. API Token -- 您自行设置的 API Token，类似用于您 API 的一个密码
3. Telegram Bot API Token -- 自行向 Telegram 申请的 Token，详见 telegram_bot/README.md

## ✨ 项目组成

```
wgetcloud_crawler/
├── api_get_traffic/      # Flask API：提供 HTTP 接口查询流量
│   └── README.md
│
├── telegram_bot/         # Telegram Bot：聊天指令查询流量
│   └── README.md
│
├── venv/                 # Python 虚拟环境（建议忽略提交）
└── README.md             # 项目总说明（本文件）
```

---

## 📦 子项目说明

### 🌐 api\_get\_traffic（HTTP API 服务）

一个轻量级 Flask API，用于：

- 自动爬取 Wgetcloud 面板
- 解析 **今日流量使用情况**
- 通过 HTTP 接口返回 JSON 数据

**适合场景：**

- VPS 部署
- 手机 / 脚本 / 其他服务调用
- 为 Telegram Bot 提供数据来源

📄 详细说明请查看：\
👉 [`api_get_traffic/README.md`](./api_get_traffic/README.md)

---

### 🤖 telegram\_bot（Telegram 流量查询机器人）

一个 Telegram Bot，用于：

- 通过 `/flow` 指令查询今日流量
- 通过 `/start` 启动交互
- 对普通文本进行回显（测试用）

**特点：**

- 基于 `python-telegram-bot`
- 使用 `config.json` 管理 Token
- 可部署在服务器后台长期运行

📄 详细说明请查看：\
👉 [`telegram_bot/README.md`](./telegram_bot/README.md)

---

## 🧠 整体工作流程

```
[Telegram 用户]
        │
        ▼
[Telegram Bot]
        │
        ▼
[HTTP API 服务]
        │
        ▼
[Wgetcloud 用户面板]
```

- Telegram Bot 接收用户命令
- Bot 请求本地 / 远程 API
- API 爬取并解析流量数据
- 返回结果并展示给用户

---

## 🛠️ 技术栈

- Python 3.x
- Flask
- python-telegram-bot
- requests / cloudscraper
- Linux / VPS（推荐）

---

## 🔐 安全与配置说明

- **Cookie / Token 均由用户自行获取**
- 不提供任何账号获取、破解方式
- 建议：
  - `config.json` 加入 `.gitignore`
  - 环境变量仅用于服务端
  - 不要将敏感信息提交到 GitHub

---

## ⚠️ 使用须知

- 本项目仅限 **个人账户使用**
- 页面结构变化可能导致爬虫失效
- 不保证长期可用性
- 请勿用于任何非法用途

---

## 📄 License

本项目为个人学习与自用项目，\
如需开源发布，建议选择：

- MIT License
- 或 Apache License 2.0

---

## 🙌 致谢

- Wgetcloud（流量服务提供商）
- Telegram Bot API
- Flask & Python 社区

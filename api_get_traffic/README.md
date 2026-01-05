# 🚀 wgetcloud-traffic-api

一个用于**获取 wgetcloud 今日流量使用情况**的轻量级 API 服务。\
适用于自建监控、自动化提醒、流量统计等场景。

> **说明**：wgetcloud 是一个境外流量服务提供商，本项目仅用于**用户本人账户的自动化查询**。

---

## ✨ 功能特性

- 🌐 基于 Flask 提供 HTTP API
- 🔐 使用 Token 进行接口访问鉴权
- 🧭 自动爬取 wgetcloud 用户面板流量数据
- 📊 智能识别单位（M / G）
- 🧩 适合部署在 VPS，供手机/脚本调用

---

## 🧱 项目结构

```
.
├── api_get_traffic.py      # Flask API 主程序
├── get_today_traffic.py   # 负责爬取并解析流量数据
└── README.md
```

---

## 🛠️ 安装依赖

```bash
pip install flask cloudscraper fake-useragent
```

---

## 🔐 环境变量配置

在服务器中设置以下环境变量：

```bash
export WG_COOKIE="你的 wgetcloud 登录 Cookie"
export WG_TOKEN="你的 API Token 的 MD5 值"
```

> ⚠️ **注意**：`WG_TOKEN` 不是明文，而是 **Token 的 MD5 值**

例如：

```bash
echo -n XXX | md5sum
```

将得到的 MD5 结果作为 `WG_TOKEN`

---

## ▶️ 启动服务

```bash
python api_get_traffic.py
```

默认运行在：

```
http://127.0.0.1:5000/
```

---

## 📡 API 使用方式

### 请求示例

```bash
curl -H "X-API-TOKEN: XXX" http://127.0.0.1:5000/
```

### 返回示例

```json
{
  "msg": "今日已使用 360.0M"
}
```

或

```json
{
  "msg": "今日已使用 2.41G"
}
```

---

## 🧠 工作原理简述

1. Flask 接收请求
2. 校验 `X-API-TOKEN` 的 MD5 值
3. 使用 Cookie 登录 wgetcloud
4. 爬取用户流量日志接口
5. 解析当日流量并格式化返回

---

## ⚠️ 使用须知

- 本项目**只适用于用户本人账户**
- 不提供 Cookie 获取方式
- 请勿用于任何非法用途
- wgetcloud 页面结构变化可能导致接口失效
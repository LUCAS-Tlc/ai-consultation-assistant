# 技术规格说明 — AI 客户咨询跟进助手

## 技术栈

| 层级 | 技术 | 版本要求 |
|------|------|----------|
| 语言 | Python | 3.9+ |
| Web 框架 | Flask | 3.0+ |
| 数据库 | SQLite | 内置于 Python |
| AI SDK | anthropic | 0.40+ |
| 前端 | HTML5 + CSS3 + 原生 JS | — |
| 环境变量 | python-dotenv | 1.0+ |

## 系统架构

```
浏览器 (Chrome/Safari)
    │
    ▼
Flask Web Server (localhost:5000)
    │
    ├── database.py ──── SQLite (customers.db)
    │
    └── ai_service.py ── Claude API
```

## 数据库设计

单表 `customers`：

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PK, AUTOINCREMENT | 主键 |
| name | TEXT | NOT NULL | 客户姓名 |
| email | TEXT | NOT NULL | 客户邮箱 |
| company | TEXT | — | 公司名称 |
| need | TEXT | — | 客户需求描述 |
| budget | TEXT | — | 预算 |
| timeline | TEXT | — | 时间线 |
| notes | TEXT | — | 其他备注 |
| intent_level | TEXT | — | AI 判定的意向等级 (High/Medium/Low) |
| ai_analysis | TEXT | — | AI 需求分析文本 |
| email_draft | TEXT | — | AI 生成的邮件草稿 |
| follow_up_date | TEXT | — | AI 建议的跟进日期 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 提交时间 |

## API 路由

| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/` | 客户咨询表单页 |
| POST | `/submit` | 提交表单，触发 AI 分析 |
| GET | `/result/<id>` | 查看 AI 分析结果 |
| GET | `/dashboard` | Dashboard 仪表盘 |
| GET | `/customer/<id>` | 客户详情 |
| GET | `/export` | 导出 CSV |
| POST | `/generate-demo` | 生成 Demo 数据 |

## Claude API 调用设计

使用单次 API 调用，结构化 prompt 同时输出：
1. 意向等级判断
2. 需求分析
3. 邮件草稿
4. Follow-up 日期

返回格式为 JSON，便于解析。启用 prompt caching 以降低费用。

## 安全约定
- API Key 通过环境变量 `ANTHROPIC_API_KEY` 读取
- `.env` 文件不提交到版本管理
- HTML 模板中做输出转义，防止 XSS

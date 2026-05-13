# AI 客户咨询跟进助手

一款运行在 Mac 本地的 AI 客户咨询跟进助手。客户通过 Web 表单提交咨询，系统调用 DeepSeek API 自动分析需求、判断意向等级（High / Medium / Low）、生成回复邮件草稿，并创建跟进日期。

---

## 环境准备

1. **Python 3.9+**（Mac 自带）
2. **DeepSeek API Key** — 在 [platform.deepseek.com](https://platform.deepseek.com) 注册并创建 API Key
3. 在终端中运行以下命令：

```bash
# 进入项目目录
cd ~/Downloads/ai客户咨询助手

# 创建虚拟环境（仅第一次）
python3 -m venv venv

# 安装依赖（仅第一次）
./venv/bin/pip install -r requirements.txt

# 设置 API Key
export DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxx"

# 启动服务
./venv/bin/python app.py
```

4. 打开浏览器访问 **http://localhost:8080**

---

## 功能一览

| 功能 | 说明 |
|------|------|
| 客户咨询表单 | 填写 Name/Email/Company/Need/Budget/Timeline/Notes |
| AI 自动分析 | 分析需求痛点、判定意向等级、生成回复邮件 |
| 结果展示 | 查看 AI 分析结果和邮件草稿（支持一键复制） |
| Dashboard | 统计仪表盘 + 客户列表 + 意向等级筛选 |
| 客户详情 | 查看单个客户的完整信息和 AI 结果 |
| 导出 CSV | 一键导出所有客户数据 |
| Demo 数据 | 一键生成 8 条模拟客户数据用于体验 |

---

## 使用流程

1. 启动服务后，首页即为**客户咨询表单**
2. 填写客户信息 → 点击「提交并让 AI 分析」
3. AI 分析完成后自动跳转结果页，可查看：
   - 意向等级（High = 红色 / Medium = 橙色 / Low = 灰色）
   - 需求分析摘要
   - 英文回复邮件草稿（可一键复制）
   - 建议的跟进日期
4. 点击「Dashboard」查看所有客户统计和列表
5. 在 Dashboard 中可以：
   - 按意向等级筛选
   - 导出 CSV 文件
   - 一键生成 Demo 数据

---

## 常见问题

**Q: 提示 "DEEPSEEK_API_KEY not set" 怎么办？**
A: 每次打开新终端都需要重新 `export DEEPSEEK_API_KEY="你的key"`。也可以创建 `.env` 文件免去每次设置：
```
echo 'DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx' > .env
```

**Q: 没有 API Key 能用吗？**
A: 可以体验基本功能。表单提交会正常保存客户信息，但 AI 分析会跳过。也可以用「生成 Demo 数据」按钮来生成带意向等级的模拟数据。

**Q: API 调用费用高吗？**
A: 很低。此项目使用 DeepSeek Chat 模型，按量计费，价格远低于同类模型。

**Q: 数据存在哪里？**
A: 所有数据存在项目目录下的 `customers.db`（SQLite 文件）。删除该文件即可清空所有数据。

**Q: 如何停止服务？**
A: 在终端按 `Ctrl + C`。

---

## 项目结构

```
ai客户咨询助手/
├── app.py              # Flask 主应用
├── database.py         # SQLite 数据库操作
├── ai_service.py       # Claude API 调用
├── templates/          # 页面模板
│   ├── form.html       # 客户表单
│   ├── result.html     # AI 分析结果
│   ├── dashboard.html  # 管理仪表盘
│   └── customer.html   # 客户详情
├── static/
│   └── style.css       # 样式
├── docs/               # 项目规范文档
├── dev-logs/           # 开发日志
└── requirements.txt    # Python 依赖
```

---

## 后续学习方向

如果你想自己动手改进这个项目，可以从以下方向入手：

1. **换模型**：在 `ai_service.py` 中把 `deepseek-chat` 改成 `deepseek-reasoner` 获得更强的推理能力
2. **改 Prompt**：修改 `ai_service.py` 中的 `SYSTEM_PROMPT`，调整分析逻辑或邮件风格
3. **改 UI 颜色**：修改 `static/style.css` 顶部的颜色变量
4. **加字段**：在表单、数据库和 AI Prompt 中同步添加新字段
5. **加搜索**：在 Dashboard 添加客户名称/公司搜索功能
6. **加删除**：在客户详情页增加删除按钮，调用 `database.py` 中的 `delete_customer`
7. **邮件发送**：接入 SMTP 服务，实现一键发送邮件草稿

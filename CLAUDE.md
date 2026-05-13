# AI 客户咨询跟进助手 — 项目指引

## 项目简介
这是一款运行在 Mac 本地的 AI 客户咨询跟进助手。客户通过 Web 表单提交咨询信息，系统调用 DeepSeek API 自动分析需求、判断意向等级、生成回复邮件草稿，并创建跟进日期。适合 B 端业务场景的客户管理。

## 关键文件路径

### 应用代码
- 主应用入口：[app.py](app.py)
- 数据库模块：[database.py](database.py)
- AI 服务模块：[ai_service.py](ai_service.py)

### 前端模板
- 客户咨询表单：[templates/form.html](templates/form.html)
- 提交结果页：[templates/result.html](templates/result.html)
- 管理后台：[templates/dashboard.html](templates/dashboard.html)
- 客户详情页：[templates/customer.html](templates/customer.html)

### 规范文档
- 产品需求：[docs/requirements.md](docs/requirements.md)
- 技术规格：[docs/tech-specs.md](docs/tech-specs.md)
- 设计规范：[docs/design-specs.md](docs/design-specs.md)
- 执行计划：[docs/execution-plan.md](docs/execution-plan.md)

### 其他
- 开发日志：[dev-logs/](dev-logs/)
- 全局样式：[static/style.css](static/style.css)

## 开发约定

1. **分阶段推进**：按执行计划的 6 个阶段逐阶段开发，每阶段独立验证后再推进
2. **开发日志**：每次开发会话结束后，在 `dev-logs/` 下更新当日日志（`YYYY-MM-DD.md`）
3. **API Key**：通过环境变量 `DEEPSEEK_API_KEY` 读取，绝不写入代码
4. **代码风格**：保持简单，每个文件职责单一；不引入不必要的抽象
5. **测试**：每个阶段完成后手动验证关键路径

## 启动方式

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 设置 API Key
export DEEPSEEK_API_KEY="your-api-key-here"

# 3. 启动服务
python app.py

# 4. 浏览器访问
open http://localhost:8080
```

## 技术栈
- Python 3.x + Flask
- SQLite（本地数据库）
- DeepSeek API（AI 分析）
- 原生 HTML/CSS/JS（前端）

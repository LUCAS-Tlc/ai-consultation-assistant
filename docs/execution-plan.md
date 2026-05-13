# 分阶段执行计划 — AI 客户咨询跟进助手

## 总览

共 6 个阶段，逐阶段推进。每阶段完成后验证，通过后再进入下一阶段。

---

## 阶段 1：项目骨架 + 文档体系 ✅

### 任务清单
- [x] 创建项目目录结构（templates/, static/, docs/, dev-logs/）
- [x] 编写 `requirements.txt`
- [x] 创建 `CLAUDE.md`（项目指引）
- [x] 编写 `docs/requirements.md`（产品需求）
- [x] 编写 `docs/tech-specs.md`（技术规格）
- [x] 编写 `docs/design-specs.md`（设计规范）
- [x] 编写 `docs/execution-plan.md`（本文件）
- [x] 创建 `dev-logs/2026-05-13.md` 初始化日志

### 验证
- [x] 目录结构完整一致
- [x] 所有文档内容齐备

---

## 阶段 2：基础 Flask 应用 + 数据库 ✅

### 任务清单
- [x] 实现 `app.py`：基础 Flask 骨架
- [x] 实现 `database.py`：建表 + insert/query/update/delete 操作
- [x] 配置 `.env` 读取逻辑

### 验证
- [x] `./venv/bin/python app.py` 启动成功
- [x] 浏览器访问 `http://localhost:5000` 看到表单页
- [x] 数据库文件 `customers.db` 自动生成

---

## 阶段 3：AI 服务模块 ✅

### 任务清单
- [x] 实现 `ai_service.py`：封装 Claude API 调用 (Haiku 4.5)
- [x] 实现意向等级判定（High/Medium/Low）
- [x] 实现需求分析总结
- [x] 实现英文邮件草稿生成
- [x] 实现 follow-up 日期建议
- [x] 返回结构化 JSON 结果
- [x] 启用 prompt caching

### 验证
- [x] 模块正确加载
- [x] API Key 缺少时正确抛错
- [x] System prompt 设计合理

---

## 阶段 4：客户表单 + 提交结果页 ✅

### 任务清单
- [x] 实现 `templates/form.html`：客户表单（7 个字段 + 验证）
- [x] 实现 `templates/result.html`：AI 分析结果展示 + 一键复制
- [x] 实现 `POST /submit` 路由：保存数据 + 调用 AI（优雅降级）
- [x] 实现 `GET /result/<id>` 路由

### 验证
- [x] 表单必填校验有效（Name/Email 为空返回 400）
- [x] 提交后正确保存到数据库
- [x] 无 API Key 时优雅降级（数据保存，AI 跳过）
- [x] 结果页正确展示客户信息和 AI 结果

---

## 阶段 5：Dashboard + 客户详情 + CSV 导出 + Demo 数据 ✅

### 任务清单
- [x] 实现 `templates/dashboard.html`：
  - 统计卡片（总数、High、Medium、Low）
  - 客户列表表格
  - 按意向等级筛选
  - 导出 CSV 按钮
  - 生成 Demo 数据按钮
- [x] 实现 `templates/customer.html`：客户详情 + AI 结果 + 邮件复制
- [x] 实现 `GET /dashboard` 路由（含筛选参数）
- [x] 实现 `GET /customer/<id>` 路由
- [x] 实现 `GET /export` CSV 导出
- [x] 实现 `POST /generate-demo` Demo 数据生成（8 条）

### 验证
- [x] Dashboard 数据展示正确
- [x] 统计数字和实际数据一致
- [x] 筛选功能正常（All/High/Medium/Low）
- [x] CSV 文件成功下载
- [x] Demo 数据生成后有新客户出现
- [x] 客户详情页信息完整
- [x] 404 页面处理正确

---

## 阶段 6：UI 美化 + README ✅

### 任务清单
- [x] 编写 `static/style.css`：统一淡蓝色主题（#F0F7FF 背景、#1976D2 主色）
- [x] 所有页面应用统一样式（表单、表格、卡片、标签）
- [x] 响应式适配（移动端单栏 + 桌面端双栏）
- [x] 编写 `README.md`：使用说明 + 常见问题 + 项目结构 + 学习方向

### 验证
- [x] 全流程走通：填表 → 提交 → 结果 → Dashboard → 详情 → 导出
- [x] UI 风格一致，配色协调（淡蓝色主题）
- [x] 所有路由 E2E 测试通过

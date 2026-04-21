# CICD_webhook 实施计划

## 背景

基于 CICD_webhook 调研，需要打通"沙箱写代码 → GitHub → 云电脑自动编译 → 通知结果"的完整流程。

## 阶段目标

1. ✅ GitHub Actions CI 配置
2. ✅ 云电脑 Webhook 服务（端口 8888）
3. ✅ 飞书 + 邮件通知
4. ✅ 多语言编译支持（C++/Python/TypeScript）

## 里程碑

- [ ] Task 1: 创建 GitHub Actions 主流程 (ci.yml)
- [ ] Task 2: 创建飞书通知 Action (notify.yml)
- [ ] Task 3: 修改云电脑 Webhook 服务
- [ ] Task 4: 配置 GitHub Webhook
- [ ] Task 5: 配置飞书机器人
- [ ] Task 6: 端到端测试

---

## 子任务清单

### [x] Task 1: 创建 GitHub Actions 主流程 (已完成，待配置)

**目标**: 创建 `.github/workflows/ci.yml`，实现多语言编译

**实施方案**:
1. ✅ 创建 `.github/workflows/` 目录
2. ✅ 创建 `ci.yml`：
   - 触发条件：push/PR 到 main
   - 多语言支持：C++ (cmake) / Python (pytest) / TypeScript (pnpm)
   - 步骤：checkout → 安装依赖 → 编译 → 测试 → lint
3. ⚠️ Token 缺少 workflow scope，需手动配置

**验收标准**:
- [x] `ci.yml` 文件已创建
- [ ] GitHub Actions 页面能看到 workflow  ⚠️ 需要重新配置
- [ ] push 代码后自动触发构建

**文件改动**:
- `.github/workflows/ci.yml` (已创建，内容如下)

```yaml
# 4 个 Jobs: lint, build, test, notify
# 多平台: Ubuntu + macOS
# 并行构建 + 自动通知
```

**⚠️ Token 问题**: 当前 Token 缺少 `workflow` scope，需要重新生成或手动创建

---

### [ ] Task 2: 创建飞书通知 Action

**目标**: 创建飞书通知 workflow，构建失败时发送消息

**实施方案**:
1. 创建 `.github/workflows/notify.yml`
2. 监听 `workflow_run` 事件
3. 当 CI 失败时，调用飞书 Webhook 发送通知

**验收标准**:
- [ ] `notify.yml` 文件已创建
- [ ] GitHub Secrets 中配置飞书 Webhook URL
- [ ] 模拟构建失败能收到飞书通知

**文件改动**:
- `.github/workflows/notify.yml` (新增)

---

### [ ] Task 3: 修改云电脑 Webhook 服务

**目标**: 更新 `cloud_build.py`，支持端口 8888 和飞书通知

**实施方案**:
1. 修改监听端口为 8888
2. 添加 GitHub Secret 验证
3. 添加飞书通知函数
4. 添加日志记录

**验收标准**:
- [ ] `cloud_build.py` 支持 `--port 8888`
- [ ] 支持 `--secret` 参数验证
- [ ] 支持 `--feishu-webhook` 飞书通知

**文件改动**:
- `scripts/cloud_build.py` (修改)

---

### [ ] Task 4: 配置 GitHub Webhook

**目标**: 在 GitHub 仓库设置 Webhook，指向云电脑

**实施方案**:
1. GitHub → Settings → Webhooks → Add webhook
2. Payload URL: `http://115.190.107.107:8888/webhook`
3. Content type: `application/json`
4. Secret: 设置与 `cloud_build.py --secret` 相同的密码
5. Events: Just the push event
6. Add webhook

**验收标准**:
- [ ] Webhook 配置成功
- [ ] 点击 "Test" 能收到请求
- [ ] 云电脑能打印接收日志

---

### [ ] Task 5: 配置飞书机器人

**目标**: 获取飞书群机器人 Webhook URL

**实施方案**:
1. 在飞书群中添加自定义机器人
2. 复制 Webhook URL
3. 配置到 GitHub Secrets

**验收标准**:
- [ ] 获取到飞书 Webhook URL
- [ ] Webhook URL 已配置到 GitHub Secrets (FEISHU_WEBHOOK)

---

### [ ] Task 6: 端到端测试

**目标**: 验证完整流程

**实施方案**:
1. 在沙箱修改代码并 push
2. GitHub Actions 自动编译
3. 云电脑 Webhook 收到通知
4. 收到飞书通知
5. 验证整个链路

**验收标准**:
- [ ] 代码 push 后 GitHub Actions 运行
- [ ] 云电脑 Webhook 收到通知
- [ ] 飞书收到构建结果通知
- [ ] 完整日志可查

---

## 执行记录

| 日期 | 完成任务 | 状态 |
|------|----------|------|
| - | - | - |

---

## 模板命令

### 创建新调研
```bash
make new-research TOPIC=<主题>
```

### 创建新计划
```bash
make new-plan TOPIC=<主题>
```

### 查看计划进度
```bash
make show-plan TOPIC=CICD_webhook
```

### 标记任务完成
```bash
make done TASK=N TOPIC=CICD_webhook
```

---

*最后更新: 2024-04-21*

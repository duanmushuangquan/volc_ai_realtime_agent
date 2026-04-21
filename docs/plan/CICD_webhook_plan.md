# CICD_webhook 实施计划

## 背景

基于 CICD_webhook 调研，需要打通"沙箱写代码 → GitHub → 云电脑自动编译"的完整流程。

**架构**：纯 GitHub Webhook 方案（无 SSH 依赖）

```
沙箱 (push) → GitHub → Webhook → 云电脑 (拉取 + 编译)
```

## 阶段目标

1. ✅ GitHub Actions CI 配置
2. ✅ 云电脑 Webhook 服务（端口 8888）
3. ✅ 云电脑 GitHub Webhook 接收
4. ✅ 多语言编译支持（C++/Python）

## 里程碑

- [x] Task 1: 创建 GitHub Actions 主流程 (ci.yml)
- [x] Task 2: 简化通知（GitHub Actions 内置）
- [x] Task 3: 修改云电脑 Webhook 服务
- [ ] Task 4: 配置 GitHub Webhook（网页操作）
- [ ] Task 5: 云电脑首次设置（手动）
- [ ] Task 6: 端到端测试

---

## 子任务清单

### [x] Task 1: 创建 GitHub Actions 主流程 ✅

**目标**: 创建 `.github/workflows/ci.yml`，实现多语言编译

**实施方案**:
1. ✅ 创建 `.github/workflows/` 目录
2. ✅ 创建 `ci.yml`：
   - 触发条件：push/PR 到 main
   - 多语言支持：C++ (cmake) / Python (pytest)
   - 步骤：checkout → 安装依赖 → 编译 → 测试 → lint
3. ✅ Token 问题已解决
4. ✅ 添加 hello world 示例验证 CI 流程

**验收标准**:
- [x] `ci.yml` 文件已创建
- [x] GitHub Actions 页面能看到 workflow
- [x] push 代码后自动触发构建
- [x] 所有 Job 通过 (lint/build/test)

**文件改动**:
- `.github/workflows/ci.yml` (已创建)
- `src/cpp/` (C++ hello world)
- `src/python/` (Python hello world)
- `tests/` (pytest 测试)
- `CMakeLists.txt` (C++ 编译配置)


---

### [x] Task 2: 简化通知（移除飞书）✅

**目标**: 简化流程，使用 GitHub Actions 内置通知

**实施方案**:
1. ✅ 移除飞书通知需求
2. ✅ 使用 GitHub 内置通知（邮件）

**验收标准**:
- [x] 不需要额外配置飞书
- [x] GitHub Actions 通知正常工作


---

### [x] Task 3: 修改云电脑 Webhook 服务 ✅

**目标**: 更新 `cloud_build.py`，支持端口 8888 和 GitHub Secret 验证

**实施方案**:
1. ✅ 修改监听端口为 **8888**
2. ✅ 添加 GitHub Secret 验证
3. ✅ 添加日志记录到文件
4. ✅ 添加健康检查端点 (GET /webhook/git)
5. ✅ 更新 `sync_to_cloud.py` 适配新端口

**验收标准**:
- [x] `cloud_build.py` 支持 `--port 8888`
- [x] 支持 `--secret` 参数验证
- [x] 支持健康检查 (GET /webhook/git)
- [x] 添加日志记录

**文件改动**:
- `scripts/cloud_build.py` (已更新)
- `scripts/sync_to_cloud.py` (已更新)
- `Makefile` (已更新，端口改为 8888)

---

### [ ] Task 4: 配置 GitHub Webhook（网页操作）

**目标**: 在 GitHub 仓库设置 Webhook，指向云电脑

**责任方**: 你（网页操作）

**实施方案**:
1. 访问 GitHub 仓库 Settings → Webhooks → Add webhook
2. 配置：
   - Payload URL: `http://115.190.107.107:8888/webhook/git`
   - Content type: `application/json`
   - Secret: 可选（与 `--secret` 参数一致）
   - Events: Just the push event
3. 点击 "Add webhook"

**验收标准**:
- [ ] Webhook 配置成功
- [ ] 点击 "Recent Deliveries" 可以看到发送记录
- [ ] 点击 "Test" 能收到请求（显示 200）

---

### [ ] Task 5: 云电脑首次设置（手动）

**责任方**: 你（云电脑操作）

**前提**: Task 4 完成

**实施方案**:
1. 在云电脑上克隆仓库（如未克隆）：
   ```bash
   cd /home/coze/projects
   git clone https://github.com/duanmushuangquan/volc_ai_realtime_agent.git
   ```
2. 启动 Webhook 服务：
   ```bash
   cd volc_ai_realtime_agent
   python3 scripts/cloud_build.py --webhook --port 8888
   ```

**验收标准**:
- [ ] Webhook 服务运行中
- [ ] 健康检查成功：`curl http://115.190.107.107:8888/webhook/git`

---

### [ ] Task 6: 端到端测试

**目标**: 验证完整流程

**前提**: Task 4 + Task 5 完成

**实施方案**:
1. 我推送一个测试 commit
2. GitHub Webhook 发送到云电脑
3. 云电脑收到后自动 `git pull && cmake build`
4. 你验证云电脑编译结果

**验收标准**:
- [ ] 代码 push 后 Webhook 收到通知
- [ ] 云电脑自动拉取最新代码
- [ ] 云电脑成功编译

---

## 执行记录

| 日期 | 完成任务 | 状态 |
|------|----------|------|
| 2024-12-19 | Task 1: GitHub Actions CI | ✅ |
| 2024-12-19 | Task 2: 简化通知 | ✅ |
| 2024-12-19 | Task 3: 云电脑 Webhook 服务 | ✅ |

---

## 快速命令

```bash
# 推送到 GitHub
make sync-github

# 查看云电脑 Webhook 状态
make cloud-status

# 在云电脑上启动 Webhook 服务
make cloud-webhook
```

**注意**: 由于云电脑不支持 SSH（端口 22 未开放），代码同步完全依赖 GitHub Webhook。

---

## 云电脑首次设置

```bash
# 1. 在云电脑上克隆仓库（如未克隆）
cd /home/coze/projects
git clone https://github.com/duanmushuangquan/volc_ai_realtime_agent.git
cd volc_ai_realtime_agent

# 2. 启动 Webhook 服务
python3 scripts/cloud_build.py --webhook --port 8888

# 3. 服务运行后，可以在浏览器访问健康检查
# http://115.190.107.107:8888/webhook/git
```

---

## GitHub Webhook 配置步骤

### 步骤 1: 打开仓库设置

访问: https://github.com/duanmushuangquan/volc_ai_realtime_agent/settings

### 步骤 2: 添加 Webhook

1. 点击左侧 **Webhooks** → **Add webhook**
2. 填写配置：
   - **Payload URL**: `http://115.190.107.107:8888/webhook/git`
   - **Content type**: `application/json`
   - **Secret**: （可选，留空或设置一个密码）
   - **Events**: 选择 **Just the push event**

### 步骤 3: 保存

点击 **Add webhook**

### 步骤 4: 测试

1. 点击刚创建的 Webhook
2. 点击 **Recent deliveries**
3. 点击 **Test** → 选择 **push**
4. 查看是否返回 **200 OK**

---

## 故障排查

| 问题 | 解决方法 |
|------|----------|
| Webhook 连接失败 | 检查云电脑端口 8888 是否开放 |
| 云电脑未响应 | 检查 `cloud_build.py` 是否运行中 |
| 编译失败 | 在云电脑上查看 `cloud_build.log` |

---

## 工作流（完成 Task 4+5 后）

```
你: "推送代码"
    ↓
GitHub: 触发 Actions CI
    ↓
GitHub: 发送 Webhook 到云电脑
    ↓
云电脑: 自动 git pull + 编译
    ↓
完成!
```

---

*最后更新: 2024-12-19*

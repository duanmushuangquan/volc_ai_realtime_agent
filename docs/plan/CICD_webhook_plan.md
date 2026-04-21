# CICD_webhook 实施计划

## 背景

基于 CICD_webhook 调研，需要打通"沙箱写代码 → GitHub → 云电脑自动编译"的完整流程。

## 阶段目标

1. ✅ GitHub Actions CI 配置
2. ✅ 云电脑 Webhook 服务（端口 8888）
3. ⏳ 云电脑与沙箱同步流程
4. ✅ 多语言编译支持（C++/Python）

## 里程碑

- [x] Task 1: 创建 GitHub Actions 主流程 (ci.yml)
- [x] Task 2: 简化通知（GitHub Actions 内置）
- [x] Task 3: 修改云电脑 Webhook 服务 ✅ **进行中**
- [ ] Task 4: 配置 GitHub Webhook（网页操作）
- [ ] Task 5: SSH 公钥配置
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
3. ✅ Token 问题已解决，重新生成了有 workflow 权限的 token
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
2. ✅ 简化 `notify.yml`（可选保留）
3. ✅ 使用 GitHub 内置通知（邮件/SMS）

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

### [ ] Task 4: 配置 GitHub Webhook

**目标**: 在 GitHub 仓库设置 Webhook，指向云电脑

**实施方案**:
1. GitHub → Settings → Webhooks → Add webhook
2. Payload URL: `http://115.190.107.107:8888/webhook/git`
3. Content type: `application/json`
4. Secret: 设置与 `cloud_build.py --secret` 相同的密码（可选）
5. Events: Just the push event
6. Add webhook

**验收标准**:
- [ ] Webhook 配置成功
- [ ] 点击 "Test" 能收到请求
- [ ] 云电脑能打印接收日志

---

### [ ] Task 5: SSH 公钥配置

**目标**: 配置 SSH 公钥，实现沙箱到云电脑的安全连接

**实施方案**:
1. 在沙箱生成 SSH 密钥对
2. 将公钥添加到云电脑 `~/.ssh/authorized_keys`
3. 测试 SSH 连接

**验收标准**:
- [ ] 沙箱可以 SSH 连接云电脑
- [ ] `make cloud-ssh` 可以连接
- [ ] `make sync-all` 可以推送并触发

---

### [ ] Task 6: 端到端测试

**目标**: 验证完整流程

**实施方案**:
1. 在沙箱修改代码并 `make sync-all`
2. GitHub Actions 自动编译
3. 云电脑 Webhook 收到通知
4. 云电脑拉取并编译
5. 验证整个链路

**验收标准**:
- [ ] 代码 push 后 GitHub Actions 运行
- [ ] 云电脑 Webhook 收到通知
- [ ] 云电脑成功编译
- [ ] 完整日志可查

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
# 同步到云电脑（推送 + 触发编译）
make sync-all

# 查看云电脑状态
make cloud-status

# SSH 连接到云电脑
make cloud-ssh

# 在云电脑上启动 Webhook 服务
make cloud-webhook
```

---

## 云电脑首次设置

```bash
# 1. SSH 连接到云电脑
ssh coze@115.190.107.107

# 2. 创建工作目录
mkdir -p /home/coze/projects
cd /home/coze/projects

# 3. 克隆仓库
git clone https://github.com/duanmushuangquan/volc_ai_realtime_agent.git
cd volc_ai_realtime_agent

# 4. 启动 Webhook 服务
python3 scripts/cloud_build.py --webhook --port 8888
```

---

## 故障排查

| 问题 | 解决方法 |
|------|----------|
| SSH 连接失败 | 检查公钥是否添加到云电脑 |
| Webhook 连接失败 | 检查云电脑端口 8888 是否开放 |
| 编译失败 | SSH 到云电脑查看日志 |

---

*最后更新: 2024-12-19*

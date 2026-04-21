# CICD_webhook_plan 实施计划

## 背景
基于 CICD_webhook 调研，需要打通"沙箱写代码 → GitHub → 云电脑自动编译"的流程。提升开发效率，减少手动操作。

## 阶段目标
1. 配置 GitHub Actions 实现自动编译
2. 配置云电脑 Webhook 实现双向同步
3. 实现编译结果通知

## 里程碑
- [ ] GitHub Actions CI 配置完成
- [ ] 云电脑 Webhook 服务配置完成
- [ ] 推送代码后自动编译验证
- [ ] 通知机制配置（待定）

---

## 待确认项（调研问题回答）

> 请回答 research 文档中的问题，确认后更新此处

| 问题 | 选项 | 说明 |
|------|------|------|
| 实现范围 | A/B | 待确认 |
| 通知方式 | A/B/C/D | 待确认 |
| Webhook 端口 | 8000/其他 | 待确认 |
| 编译任务 | A/B | 待确认 |

---

## 子任务清单

### [ ] Task 1: 配置 GitHub Personal Access Token
**目标**: 获取 GitHub 权限，用于 Webhook 触发

**实施方案**:
1. 在 GitHub Settings → Developer settings → Personal access tokens
2. 创建新 Token (classic)
3. 勾选 `repo` (完全控制仓库)
4. 保存 Token

**验收标准**:
- [ ] 获取到 Token
- [ ] Token 已配置到沙箱环境

**文件改动**:
- 无

---

### [ ] Task 2: 创建 GitHub Actions Workflow
**目标**: 实现代码 push 后自动编译

**实施方案**:
1. 创建 `.github/workflows/build.yml`
2. 配置触发条件 (push/pull_request)
3. 配置编译步骤：
   - checkout 代码
   - 安装依赖 (cmake, gcc)
   - 编译项目
   - 运行测试

**验收标准**:
- [ ] `.github/workflows/build.yml` 已创建
- [ ] push 代码后 GitHub Actions 自动运行
- [ ] 编译状态可在 GitHub 仓库看到

**文件改动**:
- `.github/workflows/build.yml` (新增)

---

### [ ] Task 3: 配置云电脑 Webhook 服务
**目标**: 云电脑能接收 GitHub Webhook 通知

**实施方案**:
1. 在云电脑上克隆项目（如未克隆）
2. 配置防火墙开放端口
3. 启动 Webhook 服务：
   ```bash
   python3 scripts/cloud_build.py --webhook --port 8000
   ```
4. 在 GitHub 仓库设置 Webhook：
   - Payload URL: `http://115.190.107.107:8000/webhook`
   - Content type: `application/json`
   - Secret: (设置密码)
   - Events: push events

**验收标准**:
- [ ] 云电脑端口 8000 可访问
- [ ] `cloud_build.py --webhook` 正常运行
- [ ] GitHub Webhook 配置成功
- [ ] GitHub "Test" 按钮能收到响应

**文件改动**:
- 无

---

### [ ] Task 4: 打通完整流程测试
**目标**: 验证"沙箱 → GitHub → 云电脑"完整链路

**实施方案**:
1. 在沙箱修改一个简单的测试文件
2. 执行 `make sync-all`
3. 验证：
   - 代码推送到 GitHub
   - GitHub Actions 自动编译
   - 云电脑收到 Webhook 并执行编译
4. 修复中间可能出现的问题

**验收标准**:
- [ ] `make sync-all` 成功
- [ ] GitHub Actions 显示编译状态
- [ ] 云电脑 Webhook 收到通知
- [ ] 云电脑执行编译（如果配置）

**文件改动**:
- 根据测试情况可能调整脚本

---

### [ ] Task 5: 配置通知机制（可选）
**目标**: 编译完成后自动通知

**实施方案**:
1. 根据选择的通知方式配置：
   - 邮件：GitHub Actions 自带
   - 飞书：配置飞书机器人 Webhook
   - 其他：根据选择实现
2. 在 GitHub Actions 添加通知步骤

**验收标准**:
- [ ] 编译完成后收到通知
- [ ] 通知包含编译结果（成功/失败）

**文件改动**:
- `.github/workflows/build.yml` (更新)

---

## 执行记录

| 日期 | 完成任务 | 状态 |
|------|----------|------|
| - | - | - |

---

## 命令清单

```bash
# 沙箱端
make sync-all         # 推送到 GitHub 并触发云电脑
make sync-status      # 查看编译状态

# 云电脑端
python3 scripts/cloud_build.py --webhook --port 8000  # 启动 Webhook 服务
```

---

*最后更新: 2024-04-21*

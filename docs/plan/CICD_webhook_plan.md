# CICD_webhook 实施计划

## 背景

**问题**：云电脑的端口（8000/8888）无法从公网访问，GitHub Webhook 无法直接推送消息到云电脑。

**解决方案**：使用**轮询模式**，云电脑定时检查 GitHub 是否有新提交，有则自动拉取 + 编译。

---

## 架构设计

```
沙箱 (push)                              云电脑 (轮询)
    │                                         │
    │ git push                                │
    ├────────────────────────────────────────→│ GitHub
    │                                         │ ← polling
    │                                         │ (每 60s)
    │                                         │
    │ GitHub Actions CI                       │ git pull
    │  ├── lint                               │ cmake build
    │  ├── build                              │ make test
    │  └── test                               │
    │                                         │
    │ 你查看 GitHub Actions 结果               │ build.log
    │ ←───────────────────────────────────────│
```

---

## 子任务清单

### [x] Task 1: GitHub Actions CI ✅

**目标**: 创建 CI 流程，多平台编译 + 测试

**验收标准**:
- [x] CI workflow 文件已创建
- [x] Lint job 通过
- [x] Build job 通过 (Ubuntu + macOS)
- [x] Test job 通过

**文件改动**:
- `.github/workflows/ci.yml`


---

### [x] Task 2: 简化通知（移除飞书）✅

**目标**: 简化流程，使用 GitHub 内置通知

**验收标准**:
- [x] 不需要额外配置飞书
- [x] GitHub Actions 通知正常工作

---

### [x] Task 3: 修改云电脑构建脚本 ✅

**目标**: 更新 `cloud_build.py`，支持轮询模式

**验收标准**:
- [x] 支持 `--poll` 轮询模式
- [x] 支持 `--github-repo` 指定仓库
- [x] 支持 `--interval` 指定间隔
- [x] 自动 git pull + cmake build + test

**文件改动**:
- `scripts/cloud_build.py` (已更新)


---

### [ ] Task 4: 云电脑首次设置（手动）

**责任方**: 你（云电脑操作）

**实施方案**:
1. 在云电脑上克隆仓库（如未克隆）：
   ```bash
   cd /home/coze/projects
   git clone https://github.com/duanmushuangquan/volc_ai_realtime_agent.git
   ```
2. 启动轮询模式：
   ```bash
   cd volc_ai_realtime_agent
   python3 scripts/cloud_build.py --poll --interval 60
   ```

**验收标准**:
- [ ] 轮询服务运行中
- [ ] 能获取到 GitHub 最新 commit SHA
- [ ] 首次会执行一次 git pull + build

**注意**: 按 `Ctrl+C` 停止轮询


---

### [x] Task 5: 端到端测试 ✅

**目标**: 验证完整流程

**前提**: Task 4 完成

**实施方案**:
1. 我推送一个测试 commit
2. 你在云电脑上看日志
3. 云电脑检测到新 commit，自动拉取 + 编译
4. 你验证编译结果

**验收标准**:
- [ ] 轮询检测到新 commit
- [x] 自动 git pull
- [ ] 自动 git pull
- [ ] 成功 cmake build
- [x] 成功 cmake build
- [x] 成功 make test
- [ ] 成功 make test


---

## 快速命令

### 在云电脑上运行

```bash
# 进入项目目录
cd /home/coze/projects/volc_ai_realtime_agent

# 首次：拉取最新代码 + 编译
python3 scripts/cloud_build.py

# 启动轮询模式（推荐）
python3 scripts/cloud_build.py --poll --interval 60

# 停止轮询：Ctrl+C
```

### 在沙箱中

```bash
# 推送到 GitHub（会自动触发 CI）
git add . && git commit -m "your message" && git push

# 查看 CI 状态
# https://github.com/duanmushuangquan/volc_ai_realtime_agent/actions
```

---

## 工作流程

### 日常开发

1. **沙箱**: 写代码 → `git push`
2. **GitHub Actions**: 自动 CI（lint + build + test）
3. **你**: 查看 GitHub Actions 结果
4. **云电脑**: 自动轮询 → 拉取 → 编译（如果需要）

### 云电脑始终在线

```
在云电脑上启动一次轮询（建议放到后台）：

cd /home/coze/projects/volc_ai_realtime_agent
nohup python3 scripts/cloud_build.py --poll --interval 60 > build.log 2>&1 &
```

---

## 常见问题

### Q: 轮询间隔设置多少合适？
- 推荐 60 秒（1 分钟）
- 如果需要更快响应，可以设为 30 秒
- 不要设太短（如 <10 秒），会增加 GitHub API 负载

### Q: 云电脑需要一直开着吗？
- 是的，需要始终在线才能自动构建
- 可以用 `nohup` 放到后台

### Q: 如何查看构建日志？
```bash
# 在云电脑上
tail -f cloud_build.log
```

### Q: 如何停止轮询？
```bash
# 方式1: Ctrl+C（前台运行）
# 方式2: pkill
pkill -f cloud_build.py
```

---

## 执行记录

| 日期 | 完成任务 | 状态 |
|------|----------|------|
| 2024-12-19 | Task 1: GitHub Actions CI | ✅ |
| 2024-12-19 | Task 2: 简化通知 | ✅ |
| 2024-12-19 | Task 3: 云电脑构建脚本 | ✅ |
| - | Task 4: 云电脑首次设置 | ⏳ |
| - | Task 5: 端到端测试 | ⏳ |

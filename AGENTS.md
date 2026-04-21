# AGENTS.md - 火山 RTC AI 机器人控制系统开发规范

## 作用范围
- 本规范适用于仓库根目录及所有子目录
- 面向 Coze 编程代理 / AI 编码助手
- 项目名：`volc_ai_realtime_agent`

---

## 1. 目录结构

```
volc_ai_realtime_agent/
├── src/                    # 源代码
│   ├── volc_ai_realtime_agent/  # 核心库
│   └── examples/           # 示例代码
├── tests/                  # 测试代码
│   ├── unit/
│   └── integration/
├── docs/                   # 文档
│   ├── research/           # 调研文件夹
│   └── plan/              # 计划文件夹
├── scripts/                # 辅助脚本
├── configs/                # 配置文件
├── Makefile               # 统一脚本入口
├── README.md
└── AGENTS.md
```

---

## 2. 调研规范 (docs/research/)

### 2.1 创建调研文档
```bash
make new-research TOPIC=volc_rtc
```

### 2.2 调研文档命名
- 格式：`{主题}.md`
- 示例：`volc_rtc.md`、`openclaw.md`、`dds.md`

### 2.3 调研文档结构
```markdown
# {主题} 调研

## 调研信息
- 调研时间：
- 信息来源：

## 核心发现
{详细记录发现的信息}

## 关键技术点
{关键技术点梳理}

## 结论
{基于调研得出的结论}

## 待确认
- [ ] 问题1

## 相关链接
- [文档链接]
```

---

## 3. 计划规范 (docs/plan/)

### 3.1 创建计划文档
```bash
make new-plan TOPIC=volc_rtc
```

### 3.2 计划文档命名
- 格式：`{主题}_plan.md`
- 示例：`volc_rtc_plan.md`

### 3.3 计划文档结构
```markdown
# {主题} 实施计划

## 背景
{基于调研的结论}

## 阶段目标
{最终要达成的目标}

---

## 子任务清单

### [ ] Task N: {子任务名称}
**目标**: {明确要解决的问题}

**实施方案**:
1. 步骤1
2. 步骤2

**验收标准**:
- [ ] 验收项1
- [ ] 验收项2

**文件改动**:
- `src/xxx.cpp`
- `tests/xxx.cpp`

---

## 执行记录

| 日期 | 完成任务 | 状态 |
|------|----------|------|
| YYYY-MM-DD | Task 1 | ✅ |
| YYYY-MM-DD | Task 2 | 🔄 |

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
make show-plan TOPIC=<主题>
# 或
cat docs/plan/<主题>_plan.md
```

### 标记任务完成
```bash
make done TASK=N TOPIC=<主题>
```
```

---

## 4. 开发规范

### 4.1 每次只做一个子任务
- 一个子任务对应一个小提交
- 每次提交只改动 1-3 个文件
- 保持提交粒度清晰

### 4.2 子任务执行流程
1. 阅读计划，确认当前子任务
2. 实现代码
3. 编写测试
4. 编写示例
5. 运行测试验证
6. 向用户报告结果
7. **等待用户确认后进入下一个**

### 4.3 提交信息格式
```bash
# 子任务完成
git commit -m "feat(topic): 完成 Task N - {任务名称}

- 完成内容1
- 完成内容2

验收标准:
- [x] 验收项1
- [x] 验收项2"
```

---

## 5. 测试规范

### 5.1 每个子任务必须包含
- 单元测试（必要）
- 集成测试（必要）
- 示例代码（必要）

### 5.2 测试命令
```bash
make test          # 运行所有测试
make test-unit     # 运行单元测试
make test-integration  # 运行集成测试
```

---

## 6. 云电脑工作流

### 6.1 代码同步
```bash
make sync-push     # 推送到云电脑
make sync-pull     # 从云电脑拉取
```

### 6.2 工作流程
```
Coze 沙箱: 代码设计 + 编写
    ↓ git commit
GitHub
    ↓ make sync-push
云电脑: 编译 + 运行验证
    ↓ make sync-pull
Coze 沙箱: 继续开发
```

---

## 7. CI/CD

### 7.1 GitHub Actions
- 触发条件: PR / Push to main
- 检查项: build, test, lint

### 7.2 命令
```bash
make ci            # 本地模拟 CI 检查
```

---

## 8. 火山 SDK 规范

### 8.1 SDK 下载
```bash
make download-sdk PRODUCT=rtc
make download-sdk PRODUCT=ai
```

### 8.2 环境变量
```bash
export VOLC_APP_ID=xxx
export VOLC_TOKEN=xxx
```

---

## 9. Makefile 命令清单

| 命令 | 功能 |
|------|------|
| `make new-research TOPIC=<topic>` | 创建调研文档 |
| `make new-plan TOPIC=<topic>` | 创建计划文档 |
| `make show-plan TOPIC=<topic>` | 显示计划进度 |
| `make done TASK=N TOPIC=<topic>` | 标记任务完成 |
| `make test` | 运行测试 |
| `make build` | 编译项目 |
| `make lint` | 代码检查 |
| `make sync-push` | 推送到云电脑 |
| `make sync-pull` | 从云电脑拉取 |
| `make download-sdk PRODUCT=<product>` | 下载火山 SDK |
| `make ci` | 本地 CI 检查 |

---

## 10. 禁止事项

- 禁止在 AGENTS.md 中写思考过程
- 禁止一次提交过多不相关改动
- 禁止跳过测试直接提交
- 禁止跳过示例代码

---

## 11. 参考链接

- 火山 RTC 文档: https://www.volcengine.com/docs/6348/
- OpenClaw: https://github.com/tier4/openclaw
- Fast DDS: https://fast-dds.docs.eprosima.com/

---

## 24. 云电脑同步规范 (Git + Webhook)

### 24.1 配置信息

| 配置项 | 值 | 说明 |
|--------|-----|------|
| **公网 IP** | `115.190.107.107` | 云电脑公网地址 |
| **SSH 用户** | `coze` | 云电脑用户名 |
| **SSH 端口** | `22` | 默认 SSH 端口 |
| **工作目录** | `/home/coze/projects/volc_ai_realtime_agent` | 代码存放位置 |
| **Webhook 端口** | `8000` | HTTP 服务端口 |

### 24.2 工作流

```
Coze 沙箱                        GitHub                      云电脑
    │                              │                          │
    │ git push                     │                          │
    ├─────────────────────────────→│                          │
    │                              │ webhook POST             │
    │                              ├────────────────────────→│
    │                              │                          │ git pull
    │                              │                          │ cmake build
    │                              │                          │ make test
    │                              │                          │
    │ curl /status                 │                          │
    ├←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←│                          │
    │ {status: "success"}          │                          │
```

### 24.3 使用命令

```bash
# 1. 推送代码到 GitHub 并触发云电脑编译
make sync-all

# 2. 查看云电脑编译状态
make sync-status

# 3. SSH 连接到云电脑调试
make cloud-ssh

# 4. 在云电脑上启动 Webhook 服务（首次需要）
make cloud-webhook
```

### 24.4 SSH 公钥配置

```bash
# 云电脑端：添加公钥
mkdir -p ~/.ssh
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5..." >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

公钥位置: `.ssh/id_ed25519.pub`

### 24.5 Python 脚本

| 脚本 | 功能 | 运行环境 |
|------|------|----------|
| `scripts/sync_to_cloud.py` | Git 推送 + Webhook 触发 | 沙箱 |
| `scripts/cloud_build.py` | 拉取 + 编译 + Webhook 服务 | 云电脑 |

### 24.6 故障排查

| 问题 | 解决方法 |
|------|----------|
| SSH 连接失败 | 检查公钥是否添加到云电脑 |
| Webhook 不可用 | 在云电脑上运行 `python3 scripts/cloud_build.py --webhook` |
| 编译失败 | SSH 到云电脑 `make cloud-ssh`，查看日志 |
| GitHub 推送失败 | 检查 git remote 配置 |

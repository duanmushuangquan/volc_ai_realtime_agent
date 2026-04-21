# CICD_webhook 调研

## 调研信息
- 调研时间：2024-04-21
- 调研人：Coze Agent
- 状态：进行中

---

## 一、概念科普（5分钟理解）

### 1.1 CI/CD 是什么？

```
CI = Continuous Integration（持续集成）
CD = Continuous Deployment（持续部署）
```

**类比理解**：

| 传统方式 | CI/CD 方式 |
|----------|------------|
| 手动编译代码 | 代码 push 后自动编译 |
| 手动测试 | 代码 push 后自动运行测试 |
| 手动部署 | 测试通过后自动部署 |
| 人工盯着屏幕等结果 | 结果自动通知你 |

**我们的场景**：

```
Coze 沙箱 (写代码)
    ↓ git push
GitHub
    ↓ webhook 自动通知
云电脑 (自动拉取 + 编译)
    ↓
结果通知 (成功/失败)
```

---

### 1.2 Webhook 是什么？

**Webhook = 自动打电话通知**

| 概念 | 解释 |
|------|------|
| **传统方式** | 你每隔 5 分钟去检查邮箱有没有新邮件 |
| **Webhook 方式** | 邮件来了就自动给你发短信通知 |
| **GitHub Webhook** | 代码 push 了，GitHub 自动"打电话"通知云电脑 |

**我们的工作流**：

```
1. 你: git push
2. GitHub: "有人提交代码了！" (自动)
3. GitHub: 发送 HTTP POST 到云电脑
4. 云电脑: 收到通知 → git pull → cmake build
5. 云电脑: 发消息告诉你结果
```

---

### 1.3 为什么不直接 SCP 推送？

| 方式 | 优点 | 缺点 |
|------|------|------|
| **SCP 直接推送** | 简单直接 | 需要配置 SSH，不安全，不方便管理 |
| **Git + Webhook** | 版本管理清晰，流程规范，可追溯 | 需要配置 GitHub Webhook |

**推荐：Git + Webhook**（我们项目选的方式）

---

## 二、当前项目现状

### 2.1 已有配置

```
Coze 沙箱                      GitHub                      云电脑
    │                              │                          │
    │ make sync-all               │                          │
    ├─────────────────────────────→│                          │
    │  (推送代码到 GitHub)         │                          │
    │                              │                          │
    │                              │ webhook POST             │
    │                              ├─────────────────────────→│
    │                              │                          │ git pull
    │                              │                          │ cmake build
    │                              │                          │
    │ make sync-status            │                          │
    ├←←←←←←←←←←←←←←←←←←←←←←←←←←←←│                          │
```

### 2.2 已有脚本

| 脚本 | 位置 | 功能 |
|------|------|------|
| `sync_to_cloud.py` | 沙箱 `scripts/` | 推送到 GitHub + 触发 Webhook |
| `cloud_build.py` | 沙箱 `scripts/` | 云电脑端：拉取 + 编译 + Webhook 服务 |

---

## 三、实现方案对比

### 方案 A：GitHub Actions（推荐）

| 项目 | 说明 |
|------|------|
| **价格** | 免费（公开仓库） |
| **配置** | `.github/workflows/` 目录 |
| **运行位置** | GitHub 服务器 |
| **适用场景** | 编译、测试、部署 |

**优点**：
- 不需要云电脑一直开着
- GitHub 免费提供服务器
- 社区成熟，模板多

**缺点**：
- 需要理解 YAML 配置
- Windows/Linux 虚拟机启动较慢（~30秒）

---

### 方案 B：云电脑 Webhook（已有基础）

| 项目 | 说明 |
|------|------|
| **价格** | 需要云电脑运行 |
| **配置** | `cloud_build.py --webhook` |
| **运行位置** | 你的云电脑 |
| **适用场景** | 需要硬件/图形界面的编译 |

**优点**：
- 可以访问云电脑的硬件（GPU 等）
- 可以运行需要图形界面的程序

**缺点**：
- 云电脑需要一直开着
- 需要配置端口映射

---

### 方案 C：混合模式（推荐）

| 场景 | 使用方式 |
|------|----------|
| 代码 push | GitHub Actions 自动编译 |
| 需要 GPU/硬件 | 云电脑 Webhook 编译 |

---

## 四、GitHub Actions 详解

### 4.1 工作原理

```
1. 你 push 代码到 GitHub
2. GitHub 检测到 push
3. GitHub 自动启动一个虚拟机（Ubuntu）
4. 虚拟机执行你的命令（安装依赖、编译、测试）
5. 完成后通知你结果
```

### 4.2 一个简单的例子

```yaml
# .github/workflows/build.yml
name: Build

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup CMake
        uses: cmake/setup-mcmake@v3
        
      - name: Build
        run: cmake -B build && cmake --build build
        
      - name: Test
        run: ctest --output-on-failure
```

### 4.3 我们的 CI 需要做什么？

| 任务 | 命令 |
|------|------|
| 编译 C++ | `cmake -B build && cmake --build build` |
| 运行测试 | `ctest --output-on-failure` |
| 代码检查 | `make lint` |
| 推送消息 | 可选：通知钉钉/飞书/Slack |

---

## 五、Webhook 配置详解

### 5.1 GitHub Webhook 设置步骤

```
1. GitHub 仓库 → Settings → Webhooks → Add webhook
2. Payload URL: https://你的云电脑IP:8000/webhook
3. Content type: application/json
4. Secret: 设置一个密码
5. Events: Just the push event
6. Add webhook
```

### 5.2 云电脑端需要做的

```bash
# 1. 确保端口 8000 可访问（防火墙）
# 2. 启动 Webhook 服务
python3 scripts/cloud_build.py --webhook --secret "你的密码"

# 3. 测试
#    在 GitHub 仓库点击 "Test" 按钮
```

---

## 六、引导问题

### 问题 1：你想实现什么？

| 选项 | 描述 |
|------|------|
| **A. 简单版** | 代码 push 后自动在云电脑编译，通知结果 |
| **B. 完整版** | A + 自动测试 + 多平台编译 + 通知 |

### 问题 2：通知方式

| 选项 | 描述 |
|------|------|
| **A. 邮件** | GitHub 自带，免费 |
| **B. 微信** | 需要企业微信（个人难申请） |
| **C. 飞书** | 需要飞书机器人 |
| **D. 暂不需要** | 只看 GitHub 状态即可 |

### 问题 3：云电脑 Webhook 端口

| 选项 | 描述 |
|------|------|
| **A. 8000** | 默认端口，简单 |
| **B. 其他端口** | 请指定 |

### 问题 4：编译任务

| 选项 | 描述 |
|------|------|
| **A. 基础编译** | cmake build |
| **B. 完整流程** | cmake build + test + lint |

---

## 七、下一步

请回答问题 1-4，我将：
1. 完善 `docs/plan/CICD_webhook_plan.md`
2. 生成对应的脚本和配置文件
3. 提供具体的操作步骤

---

## 相关链接

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Webhook 概念](https://docs.github.com/en/webhooks)
- [已有脚本位置](./scripts/sync_to_cloud.py)

---

*最后更新: 2024-04-21*

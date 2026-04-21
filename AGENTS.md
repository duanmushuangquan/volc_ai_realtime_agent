# AGENTS.md

## 作用范围
- 本规则适用于当前仓库根目录及其所有子目录。
- 本规则面向 **Coze 编程代理 / AI 编码助手**，用于开发一个基于 **火山引擎实时音视频（RTC）+ AI 音视频互动方案** 的多语言项目。
- 目标项目名统一使用：`volc_ai_realtime_agent`。

---

## 1. 项目目标
- 本仓库不是通用 Demo 收集站，而是一个 **可持续开发、可测试、可上线、可排障** 的实时 AI 音视频交互项目。
- 目标能力包括：
  - RTC 基础音视频通话
  - AI 实时语音/音视频互动
  - 接入第三方大模型或 Agent
  - Function Calling
  - AI 状态监听
  - AI 任务事件监听
  - 回调接收与去重
  - 最小示例、自动化测试、健康检查、日志与错误治理
- 默认优先参考火山引擎官方文档与 Demo；不要凭空发明接口、字段、回调名或流程。

---

## 2. 开发总原则
- 先跑通最小链路，再扩展功能。
- 先保留 Demo 的结构性正确性，再做工程化重构。
- 先写可复用生产代码，再写 `examples/` 调用示例。
- 每新增一个接口能力，必须同时补齐：
  - 生产代码
  - `tests/` 测试
  - `examples/` 最小使用案例
  - 必要 README 文档
- 严禁只在示例里堆逻辑，公共逻辑必须沉淀到正式源码目录。
- 优先做小步提交；避免大而散的无关重构。

---

## 3. 仓库定位与推荐目录
在不违背现有仓库实际结构的前提下，优先按下面思路组织：

```text
volc_ai_realtime_agent/
├─ src/
│  ├─ volc_ai_realtime_agent/
│  │  ├─ rtc/                 # RTC 基础封装
│  │  ├─ ai_chat/             # StartVoiceChat / UpdateVoiceChat / StopVoiceChat
│  │  ├─ llm/                 # 第三方 LLM / Agent 接入层
│  │  ├─ function_calling/    # 工具协议、调度、参数校验
│  │  ├─ callbacks/           # 回调接收、验签、去重、事件分发
│  │  ├─ state/               # AI 状态、任务事件、会话状态机
│  │  ├─ config/              # 配置加载与校验
│  │  ├─ logging_ext/         # 日志封装（轻量）
│  │  ├─ health/              # 健康检查
│  │  ├─ errors/              # 统一错误模型
│  │  └─ utils/
├─ tests/
│  ├─ unit/
│  ├─ integration/
│  └─ fixtures/
├─ examples/
│  ├─ python/
│  ├─ cpp/
│  └─ typescript/
├─ docs/
├─ configs/
├─ scripts/
├─ Makefile
├─ README.md
└─ AGENTS.md
```

如果当前仓库仍沿用旧结构，例如 `asr_benchmark/`，优先遵循当前结构，不要为了“好看”一次性大搬家；但新增模块时要向上面的工程分层靠拢。

---

## 4. 多语言开发规则
本项目允许 Python、C++、TypeScript 并存，但必须遵守统一原则：

### 4.1 通用要求
- 同一能力的跨语言实现必须尽量对齐：命名、配置键、错误语义、日志字段、示例流程应一致。
- 每种语言都必须有最小可运行示例。
- 不允许出现“Python 有 tests，C++/TS 没有最小 smoke test”的情况。
- 不允许把接口说明只写在某一种语言里。

### 4.2 Python
- 优先使用类型标注。
- 公共函数、类、模块需要有清晰 docstring。
- 生产代码禁止使用 `print` 做调试输出。
- 如仓库已沿用 Makefile 里的 `black` / `isort` / `flake8` / `mypy` / `pytest`，则继续沿用，不新增第二套风格体系。

### 4.3 C++
- 优先小而清晰的头源分离；避免巨型单文件。
- 明确区分接口层、实现层、示例层。
- 错误返回值、异常策略、线程生命周期必须写清楚。
- 至少提供一个构建 smoke test 或最小编译通过验证。

### 4.4 TypeScript
- 优先启用严格模式。
- 所有外部请求、回调 payload、状态对象都应定义类型。
- 避免 `any` 泛滥；仅在无法避免时局部使用并说明原因。
- 示例代码必须能清楚展示初始化、配置、调用、事件监听、清理五个步骤。

---

## 5. 与火山引擎 RTC / AI 音视频互动方案相关的强约束
- 必须基于官方文档与官方 Demo 进行实现。
- 代码中涉及以下能力时，必须保留清晰边界，不得耦合成一个大文件：
  - RTC 初始化与进房
  - AI 对话启动 / 更新 / 结束
  - LLM / Agent 配置
  - Function Calling
  - AI 状态监听
  - AI 任务事件监听
  - 服务端回调接收
- 如果新增对 AI 的控制能力，默认按以下抽象拆分：
  - `client`：面向业务方的统一调用入口
  - `transport`：HTTP/WebSocket/SDK 适配
  - `models`：请求/响应/事件数据结构
  - `service`：核心业务逻辑
  - `examples`：最小调用
  - `tests`：单元 + 集成

---

## 6. Coze 编程代理执行规则
- Coze 读取本 AGENTS.md 后生成代码时，必须先理解当前仓库已有结构与 Makefile，再决定改动位置。
- 不允许跳过 `tests/` 与 `examples/`。
- 不允许只输出伪代码、接口草图、注释占位。
- 不允许只改 README 而不写代码。
- 不允许只写 happy path，不处理失败路径。
- 生成代码时，默认按“最小闭环”交付：
  1. 可运行源码
  2. 最小示例
  3. 对应测试
  4. 日志
  5. 错误处理
  6. README 更新
- 当需求不明确时，优先保守实现，不要凭空补充不存在的火山字段。
- 如果官方文档字段或能力有版本差异，优先在代码中做兼容层，不要粗暴删除旧接口。

---

## 7. Git 机制
- 每次改动必须是一个独立、可解释、可回滚的最小提交单元。
- 提交前，至少自查：
  - 改了哪些文件
  - 为什么改
  - 是否补了测试
  - 是否补了示例
  - 是否影响 README
- 推荐提交信息格式：

```text
feat(rtc): add minimal ai voice chat wrapper
fix(callbacks): deduplicate rtc callback events by event_id
test(function_calling): add invalid payload regression case
docs(readme): document start voice chat example
refactor(config): split runtime and secret validation
```

- 禁止以下行为：
  - 一次提交混入多个无关主题
  - 顺手大改格式导致 diff 难审
  - 未验证就修改锁文件或依赖
  - 改功能但不更新文档

---

## 8. 健康检查机制
只要项目里有服务端进程、网关、回调服务、Agent 服务，就必须提供健康检查。

### 8.1 推荐健康检查端点
- `/health/live`：进程存活即可返回成功
- `/health/ready`：依赖就绪才返回成功
- `/health/startup`：启动阶段检查，可选

### 8.2 ready 检查至少覆盖
- 关键配置已加载
- 必要环境变量存在
- 对外依赖初始化完成（如 RTC 配置、模型配置、回调签名配置）
- 必要端口或服务绑定成功
- 线程池 / 任务循环 / 事件循环正常

### 8.3 禁止事项
- 不要把“进程还活着”误当作“服务可用”。
- 不要在健康检查里执行重型业务逻辑。
- 不要把密钥、Token、原始配置值直接返回给健康检查接口。

---

## 9. 日志机制
日志是本项目的硬要求，不是可选项。

### 9.1 基本要求
- 生产代码统一使用正式日志系统：
  - Python：`logging`
  - C++：项目统一日志封装或主流日志库
  - TypeScript：结构化 logger
- 严禁在生产代码里大量使用 `print` / `console.log` 代替日志。
- 日志必须包含足够上下文，至少建议包括：
  - timestamp
  - level
  - module
  - file:line
  - request_id / session_id / room_id / task_id（有则带）
  - event_name
  - elapsed_ms（适用时）

### 9.2 日志级别
- `DEBUG`：详细调试信息，仅开发定位使用
- `INFO`：主要生命周期事件
- `WARNING`：可恢复异常、降级、重试
- `ERROR`：当前请求/任务失败
- `CRITICAL` / `FATAL`：进程级不可恢复错误

### 9.3 日志内容边界
- 可以记录摘要，不要打印大段原始音频、视频、字幕、Token、密钥、签名原文。
- 对外部回调、函数调用参数、模型回复，默认记录“摘要 + 标识”，不要无脑全量落盘。
- 日志必须可用于排查以下问题：
  - 没进房
  - AI 没启动
  - Function Calling 未触发
  - 回调重复
  - 状态不一致
  - 第三方 Agent 超时或返回格式错误

---

## 10. 测试机制
测试是强制项。

### 10.1 基本要求
- 每个生产能力都必须有测试。
- 每个公开接口都必须有 `examples/` 中的最小使用案例。
- 每个功能至少覆盖：
  - happy path
  - 参数错误 / 缺字段
  - 外部依赖失败
  - 超时或异常路径（可 mock）

### 10.2 推荐测试层次
- `unit/`：纯逻辑、参数校验、数据模型、错误映射、状态机
- `integration/`：模块联调、回调接收、函数调用流转、配置装配
- `smoke/`（可选）：最小链路跑通

### 10.3 示例要求
以下示例不能省略：
- RTC 初始化最小示例
- 启动 AI 对话最小示例
- 更新 AI 会话最小示例
- 结束 AI 对话最小示例
- Function Calling 最小示例
- AI 状态监听最小示例
- AI 任务事件监听最小示例
- 服务端回调接收最小示例
- 第三方 LLM / Agent 接入最小示例

### 10.4 对旧 Makefile 的遵循
如果仓库保留现有 Makefile 机制，则默认继续遵循：
- `make fmt`
- `make lint`
- `make test`

新增语言时，也要尽量把对应的验证入口接入 Makefile，避免出现“只有人脑知道怎么测”。

---

## 11. 报错机制
必须建立统一错误模型。

### 11.1 错误分层
- `ConfigError`：配置缺失、配置格式非法
- `ValidationError`：请求参数不合法
- `AuthError`：鉴权失败、签名校验失败
- `TransportError`：网络请求失败、SDK 调用失败、连接异常
- `TimeoutError`：外部依赖超时
- `ProtocolError`：第三方返回格式不符合预期
- `BusinessError`：业务状态不允许，如会话已结束却继续更新
- `InternalError`：本地未预期异常

### 11.2 错误处理要求
- 不要吞异常。
- 不要只返回“失败了”。
- 错误信息必须包含下一步可行动建议，例如：
  - 缺哪个配置
  - 哪个字段非法
  - 是哪个外部调用失败
  - 是否可重试
  - 建议查看哪个日志字段
- 外部接口失败时，日志里要保留 request_id、trace_id 或事件标识。

### 11.3 回调相关
- 回调处理必须支持重复事件去重。
- 回调签名校验应作为可配置项；启用时必须验签，失败必须报警并拒绝处理。
- 回调处理必须快速返回，不要在主请求线程里塞满重型业务逻辑。

---

## 12. 配置与密钥管理
- 所有重要配置必须显式声明并校验。
- 使用环境变量或独立配置文件管理密钥，严禁硬编码到源码。
- 至少区分：
  - runtime config
  - secret config
  - feature flags
- 配置缺失时必须启动失败，而不是运行到一半再炸。
- README 与 `configs/` 示例必须同步。

---

## 13. 文档规则
任何影响以下内容的改动，都必须同步更新 `README.md`：
- 安装方式
- 运行方式
- 配置项
- 环境变量
- 回调地址
- 示例命令
- 测试方法
- 已支持接口

如果新增一个对外能力，README 至少要补：
- 这个能力是干什么的
- 入口文件在哪里
- 最小示例在哪
- 如何测试
- 常见错误怎么排查

---

## 14. 代码变更优先级
当 Coze 接到需求时，默认按下面顺序交付，而不是一次做满所有宏大设计：

1. 跑通最小调用链路
2. 抽出可复用源码
3. 补测试
4. 补最小示例
5. 加日志
6. 加错误分层
7. 加健康检查
8. 更新 README

---

## 15. 明确禁止事项
- 禁止只写伪代码占位
- 禁止省略 `tests/`
- 禁止省略 `examples/`
- 禁止把所有逻辑堆进单文件
- 禁止用示例代码代替生产代码
- 禁止凭空造官方接口字段
- 禁止吞异常
- 禁止把密钥、Token、签名明文打到日志
- 禁止未验证就引入新依赖
- 禁止做与当前需求无关的大规模重构

---

## 16. Coze 每次输出代码时的交付格式
每次完成一个需求后，输出必须包含：

1. 本次改动的文件列表
2. 改动目的
3. 关键设计说明
4. 最小运行方式
5. 测试方式
6. 已知限制

如果没有测试、没有示例、没有运行说明，则本次输出视为不完整。

---

## 17. 最小执行模板
当需求是“新增一个火山 AI 音视频能力”时，优先按这个最小模板执行：

1. 在正式源码目录新增能力模块
2. 新增对应数据结构与配置校验
3. 新增一个最小 `examples/` 示例
4. 新增至少一个 happy path 测试
5. 新增至少一个 failure path 测试
6. 补充日志
7. 补充 README 使用说明

---

## 18. 当前项目迁移建议（从旧 ASR 规则迁移到 RTC + AI）
- 保留旧项目中“测试、日志、Makefile、README 同步更新”的优点。
- 弱化旧项目中只适用于 Python ASR benchmark 的表述。
- 强化以下新内容：
  - 多语言并存
  - 实时交互链路
  - RTC / AI / 回调 / 状态事件分层
  - Function Calling 与 Agent 接入
  - 健康检查
  - 回调验签与去重

---

## 19. 一句话总要求
**Coze 在本仓库里写代码时，默认交付的不是“能看”的 Demo，而是“最小可运行、可测试、可排障、可继续演进”的工程化代码。**

---

## 20. 火山引擎 Demo 调研结果

### 20.1 已确认可用的 Demo

| Demo 类型 | 文档链接 | 平台 | 备注 |
|-----------|----------|------|------|
| **Linux 桌面版 Demo** | https://www.volcengine.com/docs/6348/131050 | Linux C++ | RTC 基础音视频通话 |
| **实时交互 SDK** | https://www.volcengine.com/docs/6348/75707 | 多平台 | 包含 Linux C++ SDK |
| **AI 音视频互动方案** | https://www.volcengine.com/docs/6348/2137638 | 多平台 | VoiceAgent 集成 |
| **示例工程下载** | https://www.volcengine.com/docs/6453/1163793 | - | 包含 QT 示例 |

### 20.2 待验证的 Demo（需要云电脑或本地环境）

| Demo 类型 | 平台 | 验证方式 |
|-----------|------|----------|
| veRTC Linux C++ Demo | Linux x86/ARM | 需要 gcc/cmake + 云电脑 |
| VoiceAgent (AI 语音聊天) | Linux | 需要完整 RTC + LLM 集成 |
| QT 桌面示例 | Windows/Linux | 需要 Qt 5.15+ 环境 |
| Android/iOS RTC Demo | 移动端 | 需要对应设备 |

### 20.3 Demo 跑通检查清单

在验证火山 Demo 时，按以下顺序检查：

```bash
# 1. 环境检查
- [ ] gcc/g++ >= 9.0
- [ ] CMake >= 3.20
- [ ] OpenSSL (用于 HTTPS)
- [ ] 音频驱动 (ALSA/PulseAudio)

# 2. SDK 下载
- [ ] 从文档获取 SDK 下载链接
- [ ] 解压到本地目录
- [ ] 检查头文件和 so/a 文件

# 3. 编译验证
- [ ] 官方 Makefile/CMakeLists 能编译通过
- [ ] 链接成功，无 undefined symbol

# 4. 运行验证
- [ ] 配置文件正确 (AppID/Token/RoomID)
- [ ] 能进房
- [ ] 能收发音视频流
```

### 20.4 火山 SDK 版本信息

```
veRTC SDK 版本: 3.60.102.xxxx (最新)
平台支持: Windows/macOS/Linux/Android/iOS/Web
C++ 标准: C++17
```

---

## 21. Coze 沙箱 vs 云电脑使用场景

### 21.1 能力对比

| 能力 | Coze 沙箱 | 云电脑 |
|------|-----------|--------|
| **Web 开发** | ✅ 完美支持 | ⚠️ 需要配置 |
| **Node.js/TypeScript** | ✅ 完美支持 | ✅ 完美支持 |
| **Python 脚本** | ✅ 支持 | ✅ 完美支持 |
| **C++ 编译** | ⚠️ 受限 (编译慢) | ✅ 完美支持 |
| **Qt 开发** | ❌ 不支持 | ✅ 完美支持 |
| **图形界面** | ❌ 不支持 | ✅ 完美支持 |
| **硬件访问** | ❌ 不支持 | ✅ 可配置 |
| **持久化存储** | ⚠️ /tmp 临时 | ✅ 持久化 |
| **网络访问** | ✅ 完整 | ✅ 完整 |

### 21.2 推荐使用场景

#### Coze 沙箱 适合：
- ✅ Web 前端开发（React/Next.js/Vue）
- ✅ 后端 API 开发（Node.js/Express）
- ✅ TypeScript 类型定义和接口设计
- ✅ 文档编写和架构设计
- ✅ 小型 Python 脚本
- ✅ 代码审查和优化
- ❌ **不适合需要 C++ 编译或 Qt 的场景**

#### 云电脑 适合：
- ✅ C++ 项目编译（gcc/cmake）
- ✅ Qt 桌面应用开发
- ✅ 火山 RTC Demo 验证
- ✅ 硬件驱动测试
- ✅ 图形界面应用
- ✅ **适合所有需要在真实 Linux 环境中运行的场景**

### 21.3 云电脑工作流（推荐）

```bash
# 方案：Coze 沙箱 → GitHub → 云电脑

# 1. Coze 沙箱：设计架构、编写代码骨架
$ coze init my-project --template vite
$ # 编写 C++ 源码（不编译）
$ git add . && git commit -m "feat: add rtc wrapper skeleton"

# 2. 推送到 GitHub
$ git remote add origin https://github.com/user/repo.git
$ git push origin main

# 3. 云电脑：拉取并编译验证
$ git clone https://github.com/user/repo.git
$ cd my-project
$ cmake -B build && cmake --build build
$ # 运行 Demo 验证

# 4. 结果同步回 Coze 沙箱
$ # 在云电脑上 commit 并 push
$ # Coze 沙箱 pull 最新代码
```

### 21.4 Git 同步脚本（可选）

```bash
#!/bin/bash
# sync_to_cloud.sh - 在 Coze 沙箱执行

REPO_URL="https://github.com/your-org/volc_ai_realtime_agent.git"
BRANCH="main"

# 添加远程（如果尚未添加）
git remote -v | grep -q cloud || git remote add cloud $REPO_URL

# 推送当前分支到远程
git push cloud HEAD:$BRANCH

echo "已推送到云电脑，请到云电脑执行："
echo "  cd /path/to/repo && git pull cloud $BRANCH"
```

---

## 22. 开发习惯适配

### 22.1 项目初始化偏好

- **优先使用 `coze init`**：使用 Coze CLI 初始化项目
- **模板优先级**：nextjs > vite > native-static
- **原生日志输出**：开发阶段允许 `console.log`/`print`

### 22.2 C++ 项目特殊处理

当涉及 C++ 项目时：

1. **代码设计在沙箱**：接口设计、头文件编写
2. **编译验证在云电脑**：cmake 编译、链接调试
3. **示例代码在沙箱**：完成后同步回仓库

### 22.3 多仓库管理

项目可能涉及多个仓库：

| 仓库 | 用途 | 位置 |
|------|------|------|
| `volc_ai_realtime_agent` | 核心 C++ 库 | GitHub/私有 |
| `volc_ai_web_dashboard` | Web 控制台 | Coze 沙箱 |
| `volc_ai_examples` | 示例集合 | GitHub |

### 22.4 快速验证命令

```bash
# 在云电脑上验证火山 Demo 的标准流程

# 1. 克隆/拉取最新代码
git clone https://github.com/your-org/volc_ai_realtime_agent.git
cd volc_ai_realtime_agent

# 2. 检查环境
gcc --version
cmake --version
cat /etc/os-release

# 3. 编译官方 Demo
cd examples/rtc_basic
mkdir build && cd build
cmake .. && make -j$(nproc)

# 4. 配置并运行
cp ../../configs/rtc.example.json configs/rtc.json
# 编辑 configs/rtc.json 填入 AppID/Token/RoomID
./rtc_basic

# 5. 验证清单
# - [ ] 编译无错误
# - [ ] 能进房
# - [ ] 能听到自己的声音（回音测试）
# - [ ] 多设备互通（如果有）
```

---

## 23. 下一步行动计划

### 23.1 近期任务（本周）

| 任务 | 负责 | 位置 |
|------|------|------|
| [ ] 整理火山 Demo 下载链接清单 | Coze 沙箱 | 文档 |
| [ ] 编写云电脑环境配置脚本 | 云电脑 | GitHub |
| [ ] 跑通 veRTC Linux C++ Demo | 云电脑 | 视频记录 |
| [ ] 整理编译常见问题 FAQ | Coze 沙箱 | 文档 |

### 23.2 中期任务（本月）

| 任务 | 负责 | 备注 |
|------|------|------|
| [ ] 基于火山 Demo 设计 C++ 封装层 | Coze 沙箱 | 接口设计 |
| [ ] 实现 ASR/TTS/LLM 统一接口 | Coze 沙箱 + 云电脑 | 交叉开发 |
| [ ] 验证本地模型接入 (FunASR/Qwen) | 云电脑 | Orin 环境 |
| [ ] 设计 Skills Executor 架构 | Coze 沙箱 | 接口定义 |

### 23.3 风险与备选

| 风险 | 应对 |
|------|------|
| 火山 Demo 无法下载 | 通过云电脑 VPN 访问 |
| 云电脑环境不一致 | 使用 Docker 容器化 |
| C++ 编译失败 | 逐步排查，先简化 CMakeLists |
| 网络不稳定 | 准备离线文档备份 |

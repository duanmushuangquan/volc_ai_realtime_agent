# web 实施计划 - 火山 RTC Web 部署

## 背景

基于火山 RTC Web SDK 调研，需要实现：
- Web 端实时音视频通话能力
- 与机器人控制系统的语音交互
- 支持本地开发预览和正式部署

## 阶段目标

**最终目标**：跑通火山 RTC Web Demo，实现浏览器与机器人的实时语音交互

## 里程碑

- [ ] M1: 搭建 Web 项目框架
- [ ] M2: 集成 veRTC SDK
- [ ] M3: 实现基础通话功能
- [ ] M4: 扩展语音交互功能
- [ ] M5: 完成端到端测试

---

## 子任务清单

### [ ] Task 1: 搭建 Web 项目框架

**目标**: 创建 React + TypeScript + Vite 项目结构

**实施方案**:
1. 初始化 Vite 项目：`pnpm create vite web --template react-ts`
2. 安装依赖：
   - `@volcengine/rtc` - 火山 RTC SDK
   - `tailwindcss` - 样式
3. 配置 TypeScript 和 Vite
4. 创建基础页面结构
5. 配置本地开发服务器

**验收标准**:
- [ ] 项目可运行 (`pnpm dev`)
- [ ] 页面可访问 (localhost:5000)
- [ ] 无编译错误

**文件改动**:
- `web/` (新建)
- `web/package.json`
- `web/vite.config.ts`
- `web/tsconfig.json`
- `web/src/App.tsx`

---

### [ ] Task 2: 集成 veRTC SDK

**目标**: 成功引入火山 RTC SDK

**实施方案**:
1. 安装 `@volcengine/rtc` NPM 包
2. 创建 RTC 工具模块 `src/utils/rtc.ts`
3. 实现 RTC Client 初始化
4. 配置 AppID 和 Token（使用测试配置）
5. 添加 SDK 加载日志

**验收标准**:
- [ ] SDK 加载成功
- [ ] RTC Client 可创建
- [ ] 无 SDK 相关报错

**文件改动**:
- `web/src/utils/rtc.ts` (新建)
- `web/src/types/rtc.ts` (新建)

---

### [ ] Task 3: 实现基础通话功能

**目标**: 实现加入房间、发布订阅流

**实施方案**:
1. 创建 `RtcRoom` 组件
2. 实现加入房间 (`join`)
3. 创建本地媒体流 (`createStream`)
4. 发布本地流 (`publish`)
5. 订阅远端流 (`subscribe`)
6. 实现离开房间 (`leave`)

**验收标准**:
- [ ] 可加入房间
- [ ] 可获取麦克风权限
- [ ] 可看到本地视频预览
- [ ] 可发布流

**文件改动**:
- `web/src/components/RtcRoom.tsx` (新建)
- `web/src/hooks/useRtc.ts` (新建)
- `web/src/App.tsx` (修改)

---

### [ ] Task 4: 实现 UI 控制界面

**目标**: 创建通话控制 UI

**实施方案**:
1. 创建 `Controls` 组件（麦克风、摄像头、挂断）
2. 实现音频/视频开关
3. 添加音量指示
4. 添加房间状态显示
5. 实现挂断功能

**验收标准**:
- [ ] 麦克风可开关
- [ ] 摄像头可开关
- [ ] 挂断按钮可点击
- [ ] UI 响应正常

**文件改动**:
- `web/src/components/Controls.tsx` (新建)
- `web/src/components/VideoPlayer.tsx` (新建)
- `web/src/App.css` (修改)

---

### [ ] Task 5: 配置火山控制台

**目标**: 获取正式 AppID 和 Token

**实施方案**:
1. 登录火山控制台
2. 创建 RTC 应用
3. 获取 AppID 和 AppKey
4. 生成测试 Token
5. 配置允许的域名

**验收标准**:
- [ ] 控制台创建应用成功
- [ ] 获取 AppID
- [ ] 获取 AppKey
- [ ] 域名配置完成

**文件改动**:
- `web/src/config.ts` (新建，存放配置)

---

### [ ] Task 6: 本地 HTTPS 配置（ngrok）

**目标**: 实现本地开发预览

**实施方案**:
1. 安装 ngrok
2. 配置 ngrok auth token
3. 启动 ngrok 隧道到 5000 端口
4. 在火山控制台配置域名
5. 测试 HTTPS 通话

**验收标准**:
- [ ] ngrok 可访问
- [ ] 域名可配置
- [ ] 可通过 HTTPS 加入房间

**文件改动**:
- `web/.env.example` (新增)

---

### [ ] Task 7: 端到端测试

**目标**: 完整测试通话流程

**实施方案**:
1. 启动本地开发服务器
2. 启动 ngrok
3. 两人同时加入房间
4. 测试音频通话
5. 测试视频通话
6. 测试切换设备

**验收标准**:
- [ ] 两人可互相通话
- [ ] 音频清晰
- [ ] 视频流畅
- [ ] 无明显延迟

**文件改动**:
- `web/README.md` (新增)

---

### [ ] Task 8: 集成测试

**目标**: 添加自动化测试

**实施方案**:
1. 安装测试依赖 (`vitest`, `@testing-library/react`)
2. 编写 RTC 工具函数测试
3. 编写组件测试
4. 配置 CI 测试

**验收标准**:
- [ ] 单元测试通过
- [ ] 组件测试通过
- [ ] CI 测试通过

**文件改动**:
- `web/src/__tests__/` (新建)
- `web/vitest.config.ts` (新建)

---

## 执行记录

| 日期 | 完成任务 | 状态 | 备注 |
|------|----------|------|------|
| | | | |

---

## 使用说明

### 查看计划进度
```bash
make show-plan TOPIC=web
```

### 标记任务完成
```bash
make done TASK=1 TOPIC=web
```

### 开始开发
```bash
cd web
pnpm install
pnpm dev
```

### 常用命令
```bash
pnpm dev        # 开发预览
pnpm build      # 构建
pnpm test       # 测试
pnpm lint       # 代码检查
```

---

## 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Vite | 5.x | 构建工具 |
| React | 19 | UI 框架 |
| TypeScript | 5.x | 类型安全 |
| @volcengine/rtc | 最新 | 火山 RTC SDK |
| Tailwind CSS | 4.x | 样式 |
| Vitest | 2.x | 测试 |

---

*创建时间: 2026-04-21*

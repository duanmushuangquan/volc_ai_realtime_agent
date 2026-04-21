# web 调研 - 火山 RTC Web 部署

## 调研信息
- 调研时间：2026-04-21
- 调研人：
- 状态：进行中
- 参考文档：https://www.volcengine.com/docs/6348/77374?lang=zh

## 信息来源
- [火山 RTC Web 端文档](https://www.volcengine.com/docs/6348/77374?lang=zh)
- [火山 RTC 示例工程](https://www.volcengine.com/docs/6453/1163793?lang=zh)
- [火山 RTC 实时交互 SDK](https://www.volcengine.com/docs/6348/75707?lang=zh)
- [veRTC GitHub](https://github.com/VolcEngine/volcengine-rtc-sdk-js)

## 核心发现

### 1. 火山 RTC Web SDK 概述

| 项目 | 说明 |
|------|------|
| **技术** | WebRTC |
| **平台** | Web 浏览器（Chrome/Firefox/Safari/Edge） |
| **功能** | 实时音视频通话、语音聊天、屏幕共享 |
| **SDK 包** | NPM: `@volcengine/rtc` |
| **CDN** | 可通过 CDN 引入 |
| **协议** | SRTP (加密音视频)、DTLs (加密协商) |

### 2. Web SDK 部署模式

火山 RTC Web 支持两种部署模式：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **CDN 引入** | 通过 `<script>` 标签引入 | 快速原型、简单页面 |
| **NPM 包** | 通过 npm/pnpm 安装 | 正规项目、构建工具集成 |

#### CDN 引入方式
```html
<!-- 引入 RTC SDK -->
<script src="https://xxx.volcengine.com/rtc/xxx.js"></script>

<!-- 初始化 -->
<script>
  const client = new VE RTC.Client({ appId, token });
</script>
```

#### NPM 方式
```bash
npm install @volcengine/rtc
```
```typescript
import { Client } from '@volcengine/rtc';
const client = new Client({ appId, token });
```

### 3. Web RTC 通话流程

```
┌─────────────┐                    ┌─────────────┐
│   用户 A    │ ──── WebRTC ────→ │   用户 B    │
│  (浏览器)   │ ←─── 媒体流 ──── │  (浏览器)   │
└─────────────┘                    └─────────────┘
      │                                  │
      └────────── 信令服务器 ──────────────┘
               (火山 RTC 提供)
```

**步骤**：
1. 初始化 RTC Client
2. 加入房间 (join)
3. 创建本地流 (createStream)
4. 发布流 (publish)
5. 订阅远端流 (subscribe)
6. 离开房间 (leave)

### 4. 部署架构

```
┌─────────────────────────────────────────────────────────────┐
│                      部署架构                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                  用户浏览器                           │   │
│   │  ┌───────────────────────────────────────────────┐  │   │
│   │  │  Web 页面 (HTML/JS)                           │  │   │
│   │  │  ├── veRTC SDK (CDN/NPM)                     │  │   │
│   │  │  ├── 业务逻辑 (UI 控制)                       │  │   │
│   │  │  └── 麦克风/摄像头访问                        │  │   │
│   │  └───────────────────────────────────────────────┘  │   │
│   └─────────────────────────┬───────────────────────────┘   │
│                             │ HTTPS/WSS                       │
│   ┌─────────────────────────┴───────────────────────────┐   │
│   │                  火山 RTC 云服务                      │   │
│   │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐  │   │
│   │  │  信令服务器  │ │  TURN 服务器 │ │  SFU 服务器  │  │   │
│   │  │  (房间管理)  │ │  (中继)      │ │  (转发)      │  │   │
│   │  └─────────────┘ └─────────────┘ └─────────────┘  │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                  业务服务器 (可选)                   │   │
│   │  - 房间管理 - Token 发放 - 用户认证                  │   │
│   └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 5. 部署要求

| 项目 | 要求 | 说明 |
|------|------|------|
| **HTTPS** | 必须 | 浏览器要求 HTTPS 才能访问麦克风/摄像头 |
| **域名** | 需要 | 火山控制台配置 AppID 时需要域名 |
| **证书** | 有效 | 自签名证书不可用 |
| **端口** | 443 | WebRTC 需要 UDP/TCP 443 |

### 6. 本地开发

| 方案 | 说明 | 端口 |
|------|------|------|
| **localhost** | 浏览器允许 HTTP | 3000/5000 |
| **ngrok** | 内网穿透 + HTTPS | 随机 |
| **Cloudflare Tunnel** | 免费内网穿透 | 随机 |
| **本地 HTTPS** | 自签证书 + hosts | 需信任证书 |

### 7. 项目结构建议

```
web/
├── public/                 # 静态资源
│   └── index.html         # 入口页面
├── src/                   # 源码
│   ├── components/        # React 组件
│   │   ├── RtcRoom.tsx   # 房间组件
│   │   ├── VideoPlayer.tsx
│   │   └── Controls.tsx  # 控制按钮
│   ├── hooks/             # 自定义 hooks
│   │   └── useRtc.ts     # RTC 封装
│   ├── utils/             # 工具函数
│   │   └── rtc.ts        # RTC 初始化
│   ├── App.tsx            # 主组件
│   └── main.tsx           # 入口
├── package.json
├── vite.config.ts         # Vite 配置
└── tsconfig.json
```

## 关键技术点

| 技术 | 说明 | 备注 |
|------|------|------|
| **WebRTC** | 实时通信核心 | ICE/STUN/TURN |
| **@volcengine/rtc** | 火山 RTC SDK | NPM 包 |
| **Vite** | 构建工具 | 快速热更新 |
| **React 19** | UI 框架 | 可选 |
| **TypeScript** | 类型安全 | 推荐 |
| **Tailwind CSS** | 样式 | 可选 |

## 火山控制台配置

1. **创建应用**：https://console.volcengine.com/rtc
2. **获取 AppID**：应用唯一标识
3. **获取 AppKey**：用于生成 Token
4. **配置域名**：用于 CDN 和 HTTPS
5. **创建 Token**：服务端生成（或前端使用 AppKey 测试）

## 待确认问题

### Q1: 技术栈选择
- **A**: React + TypeScript + Vite（推荐）
- **B**: 原生 HTML/JS + CDN
- **C**: Vue / Svelte

### Q2: 功能范围
- **A**: 基础 Demo（双人通话）
- **B**: 语音聊天室（多人）
- **C**: 完整功能（语音 + 视频 + 聊天 + 控制）

### Q3: 认证方式
- **A**: 简化版（直接使用 AppID，无需 Token）
- **B**: 正式版（服务端生成 Token）

### Q4: 部署目标
- **A**: 本地开发预览（ngrok）
- **B**: 部署到云服务器
- **C**: 部署到 Cloudflare Pages/Vercel

### Q5: 页面部署在哪里？
- **A**: Coze 沙箱（5000 端口预览）
- **B**: 云电脑
- **C**: 其他服务器

## 结论

火山 RTC Web SDK 提供完整的实时音视频能力：
- 支持 NPM 和 CDN 引入
- 部署需要 HTTPS（生产环境）
- 本地开发可用 ngrok 穿透
- 多人通话需要信令服务器（火山提供）

## 相关链接

- [火山 RTC 控制台](https://console.volcengine.com/rtc)
- [Web 端快速开始](https://www.volcengine.com/docs/6348/77374?lang=zh)
- [示例工程下载](https://www.volcengine.com/docs/6453/1163793?lang=zh)
- [veRTC SDK npm](https://www.npmjs.com/package/@volcengine/rtc)

# volc_rtc 调研

## 调研信息
- 调研时间：2024-04-21
- 调研人：Coze Agent
- 状态：已完成

## 信息来源
- [火山 RTC 文档](https://www.volcengine.com/docs/6348/)
- [火山 RTC C++ Linux 开发](https://www.volcengine.com/docs/6348/131050)
- [火山实时交互 SDK](https://www.volcengine.com/docs/6348/75707)
- [火山 AI 音视频互动](https://www.volcengine.com/docs/6348/2137638)

## 核心发现

### 1. 火山 RTC SDK 能力

| 能力 | 说明 |
|------|------|
| 实时音视频通话 | 基于 WebRTC，支持全球低延迟 |
| 跨平台 | Windows/macOS/Linux/Android/iOS/Web |
| C++ SDK | 提供 Linux 原生 SDK |
| 消息通道 | 支持实时文字消息 |
| AI 集成 | AI 音视频互动方案 |

### 2. AI 音视频互动方案

火山提供两种模式：

| 模式 | 说明 | 延迟 |
|------|------|------|
| **三段式** | ASR + LLM + TTS | ~500ms |
| **端到端 S2S** | 语音 → 语音直接转换 | ~300ms |

### 3. SDK 下载

| SDK | 下载位置 | 平台 |
|-----|----------|------|
| veRTC SDK | 火山控制台 | 多平台 |
| AI 音视频 SDK | 火山控制台 | 多平台 |
| Linux C++ Demo | [示例工程](https://www.volcengine.com/docs/6453/1163793) | Linux |

### 4. 离线方案

火山提供边缘部署方案：
- **边缘大模型网关**：可部署在边缘节点
- **端智能**：在边缘运行模型
- 需要企业合作申请

备选开源方案：
- **ASR**: FunASR (完全离线，Orin 可运行)
- **TTS**: Coqui XTTS-v2 (支持音色克隆)

## 关键技术点

| 技术 | 说明 | 推荐度 |
|------|------|--------|
| veRTC SDK | 实时音视频核心 | ⭐⭐⭐⭐⭐ |
| ASR API | 流式语音识别 | ⭐⭐⭐⭐⭐ |
| TTS API | 流式语音合成 | ⭐⭐⭐⭐⭐ |
| FunASR | 离线 ASR | ⭐⭐⭐⭐⭐ |
| Coqui XTTS | 离线 TTS | ⭐⭐⭐⭐ |

## 结论

1. 火山 RTC 适合作为实时音视频通信层
2. ASR/TTS 可通过火山 API 调用，也可切换到本地模型
3. 推荐先跑通 Linux C++ Demo，验证 RTC 能力
4. 离线方案需要备选（FunASR + Coqui XTTS）

## 待确认
- [x] 火山 RTC Linux C++ Demo 下载链接
- [ ] 实际编译和运行验证（需要在云电脑）
- [ ] SDK 版本确认

## 相关链接
- [火山 RTC 文档首页](https://www.volcengine.com/docs/6348/)
- [Linux C++ 开发指南](https://www.volcengine.com/docs/6348/131050)
- [AI 音视频互动](https://www.volcengine.com/docs/6348/2137638)

---

*最后更新: 2024-04-21*

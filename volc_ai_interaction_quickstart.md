
Title: 客户端 SDK
URL: https://www.volcengine.com/docs/6348/1544163?lang=zh
Publish Time: None
File Type: None
========================================

Content:
客户端 SDK

## 3.60 

该版本于 2025 年 10 月 15 日发布。此次升级包含的客户端系统有：Android、iOS、macOS、Windows、Linux。

### 升级必看 

如果你需要将应用中使用的旧版本 RTC SDK 升级为最新版，参看各端 
。

### 特性变更 

本次版本升级的核心变动可概括如下，详细变更请参看各端 
。

- **核心类与流标识符**

    - **核心类与接口重命名** ：SDK 核心基础类由 RTCVideo 更名为 RTCEngine，相关的事件回调也同步变更。

    - **统一的流标识符** ：引入 streamId 作为音视频流的唯一标识符，取代了旧版本中依赖用户 ID 或流索引 (streamIndex) 等多种方式的流管理方式。相关 API 均已适配此变更。

- **接口拆分与统一**

    - **音视频流接口拆分与统一** ：发布、订阅等流操作 API 已按音频和视频进行拆分，如 publishStream 由 publishStreamVideo 和 publishStreamAudio 替代。同时，通过布尔类型参数统一了“开启/关闭”或“订阅/取消订阅”的操作逻辑，使接口行为更直观。

    - **统一屏幕共享与主流 API** ：废除了 publishScreen、subscribeScreen 等屏幕共享专用接口，屏幕共享与摄像头音视频流共用同一套接口，通过 StreamId 进行区分。

    - **统一转推直播与 WTN（原公共流）接口** ：将独立的合流转推 CDN 与推公共流（WTN）的接口进行合并。例如，使用统一的 startPushMixedStream 接口，通过参数即可配置不同的推流目标。

- **新增功能模块**

    - **新增 RTS（实时消息）模块** ：将 RTS 相关能力独立为 RTSRoom 模块。若仅需使用实时消息功能，可单独创建 RTSRoom 实例，实现功能解耦和轻量化集成。

    - **新增游戏语音（GameRoom）模块** ：新增了 GameRoom 模块，提供了一套专为游戏语音场景设计的 API。为游戏场景下的范围语音、小队语音等功能提供了专门的 API。

- **接口易用性优化**
对部分 API 的参数和回调进行了优化，例如将整数状态码替换为更明确的枚举类型。同时，为保持接口的简洁性，正式移除了部分长期废弃的旧接口。

## 3.58 

该版本于 2024 年 3 月 12 日发布。此次升级包含的客户端系统有：Android、iOS、macOS、Windows、Linux、Electron。

Flutter SDK 3.58 版本于 2024 年 7 月 8 日发布。新增特性和升级指南参看 
。

### 升级必看 

如果你需要将应用中使用的旧版本 RTC SDK 升级为最新版，参看：
。

### 新增特性 

1. 支持内部采集信号静音控制（不改变本端硬件）。可以选择静音或取消静音麦克风采集，而不影响 SDK 音频流发布状态。参看：

| 功能简述 | Android | iOS | macOS | Windows | Linux | Unity |
	|---|---|---|---|---|---|---|
	| 设置是否将录音信号静音（不改变本端硬件） | 
 | `muteAudioCapture:mute:` | `muteAudioCapture:mute:` | 
 | 
 | 
 |

2. 支持对外部采集的 RGBA 视频帧中的 Alpha 通道进行编码，使移动端作为订阅端时可内部渲染带有背景透明效果的 RGBA 视频帧。该功能适用于需要将视频中的主体与背景分离的场景。参看：

| 功能简述 | Android | iOS | Windows | Electron |
	|---|---|---|---|---|
	| 开启外部采集视频帧的 Alpha 通道编码功能。 | 
 | `enableAlphaChannelVideoEncode:withAlphaLayout:` | 
 | 
 |
	| 关闭外部采集视频帧的 Alpha 通道编码功能。 | 
 | `disableAlphaChannelVideoEncode:` | 
 | 
 |

3. 在 Android 平台，在支持渲染 View 对象的基础上，新增支持渲染 Surface 对象。

4. 在 Android 平台，支持动态加载主库 `libvolcenginertc.so`，集成指南参看
。

### 功能优化 

1. 在 Android 系统上，加入房间，使用手机音量键调节的音量是 RTC 房间的播放音量。此前，在个别 Android 手机上，加入房间未播放音频时，使用音量键调节的是铃声音量，而非音频音量。

    - 当 SDK 将音频模式设置为通话模式时，调节通话模式音量；

    - 当 SDK 将音频模式设置为媒体模式时，调节媒体模式音量。

## 3.57 (Unity) 

该版本于 2024 年 2 月 27 日发布。

### 新增特性 

| 功能模块 | 说明 | 相关文档 |
|---|---|---|
| 音视频传输 | 摄像头处于关闭状态时，支持使用静态图片填充本地推送的视频流。 | 
 |
| 跨房间转发媒体流，适用于跨房间连麦等场景。 | 
 | |
| 设置发流端音画同步。 | 
 | |
| 视频处理 | 设置本端采集的视频帧的旋转角度。 | 
 |
| 在指定视频流上添加、移除水印。 | 
 | |
| 开启、关闭基础美颜，调整美颜强度。 | 
 | |
| 智能美化特效接口，对本地采集的视频添加美颜、滤镜、贴纸等特效。 | 
 | |
| 本地摄像头数码变焦设置。 | 
 | |
| 音频处理 | 设置音频变声、变调、均衡、混响等效果。 | 
 |

## 3.57 

该版本于 2024 年 1 月 5 日发布。此次升级包含的客户端系统有：Android、iOS、macOS、Windows、Linux、Electron。

Flutter SDK 3.57 版本于 2024 年 2 月 4 日发布。新增特性和升级指南参看 
。

### 升级必看 

如果你需要将应用中使用的旧版本 RTC SDK 升级为最新版，参看
。

### 新增特性 

1. 自 3.57 版本起，RTC SDK 支持动态加载除主库外的 `.so` 文件，SDK 在 `EngineConfig` 类中提供 `nativeLoadPath` 属性，支持在 App 运行时从指定的私有目录动态加载所需的 `.so` 文件，从而减小 App 的安装包体积。如需动态加载 `.so` 文件，参看
。

2. 该版本提供 SAMI 音频技术动态库插件、VP8 编解码插件、AAC 软件编解码插件、APM 稳定性监控插件，详情参看
。

3. Android 和 iOS 端支持将摄像头画面旋转为指定角度，适用于**无重力感应设备** 的视频采集画面适配，例如，金融行业的人脸采集设备等。参看：

| 功能简述 | Android | iOS |
	|---|---|---|
	| 旋转采集画面 | 
 | 
 |

对于手机和平板等具备重力感应的设备，旋转视频采集画面应使用 `setVideoRotationMode`，参看 
。

4. PC 端提供视频增强处理能力，当视频采集处于在暗光环境下时，开启本功能，可提高画面亮度。参看：

| 功能简述 | macOS | Windows | Electron |
	|---|---|---|---|
	| 设置视频暗光增强处理 | 
 | 
 | 
 |

5. 各端支持定向物联网卡通信。

6. Linux 端音频编码器全链路支持 G722。

7. 对远端流进行内部渲染时，支持将某一路远端流镜像渲染。

| 功能简述 | Android | iOS | macOS | Windows | Linux |
	|---|---|---|---|---|---|
	| 使用内部渲染时，为远端流开启镜像 | 
 | 
 | 
 | 
 | 
 |

8. 转推直播功能新增以下特性：

| 功能简述 | Android | iOS | macOS | windows |
|---|---|---|---|---|
| 支持在房间内无用户发布流的场景下，发起转推直播任务 | `MixedStreamServerControlConfig.setPushStreamMode` | 
 | 
 | 
 |
| 支持使用占位图代替视频流发起转推直播任务，并设置占位图的填充模式 | `MixedStreamLayoutRegionConfig.setAlternateImageURL``MixedStreamLayoutRegionConfig.setAlternateImageFillMode` | 
 | 
 | 
 |
| 合流推到 CDN 时支持推送纯音频流 | `MixedStreamServerControlConfig.setMediaType` | 
 | 
 | 
 |
| 支持设置合流后整体画布的背景图片 | `MixedStreamLayoutConfig.setBackgroundImageURL` | 
 | 
 | 
 |

9. Electron 新增特性

    1.
支持自定义音频、视频采集。参看：

| 功能简述 | Electron |
		|---|---|
		| 设置向 SDK 输入的视频源 | 
 |
		| 推送外部视频帧 | 
 |
		| 切换音频采集方式 | 
 |
		| 推送自定义采集的音频数据到 RTC SDK | 
 |
		| 启动音频裸数据混音 | `openWithCustomSource` |
		| 推送用于混音的 PCM 音频帧数据 | `pushExternalAudioFrame` |

    2.
获取时间戳。参看：

| 功能简述 | Electron |
		|---|---|
		| 获取时间戳, 单位毫秒 | `getTimestampMs` |
		| 获取时间戳, 单位微秒 | `getTimestampUs` |

10. 转推直播配置新增服务端合流控制参数

    1.
支持在合流转推发送 SEI 时设置 PayLoadType，以适配特定播放器作为接收端时接收 SEI 信息。参看：

| 功能简述 | Android | iOS | macOS | Windows |
		|---|---|---|---|---|
		| 设置合流转推 SEI 信息的 payload type | `setSeiPayloadType` | 
 | 
 | 
 |
		| 设置合流转推 SEI 信息的 Payload UUID | `setSeiPayloadUuid` | 
 | 
 | 
 |

    2.
支持控制 SEI 发送内容。此前服务端合流默认发送全量 SEI 信息，新版本支持单独发送音量提示 SEI，在需要高频发送音量信息的场景下，大幅减少性能开销。参看：

| 功能简述 | Android | iOS | macOS | Windows |
		|---|---|---|---|---|
		| 设置是否开启单独发送声音提示 SEI 的功能 | `setEnableVolumeIndication` | 
 | 
 | 
 |
		| 设置 SEI 内容 | `setSeiContentMode` | 
 | 
 | 
 |
		| 设置声音信息 SEI 是否包含音量值 | `setIsAddVolumeValue` | 
 | 
 | 
 |
		| 设置声音信息提示间隔 | `setVolumeIndicationInterval` | 
 | 
 | 
 |
		| 设置有效音量大小 | `setTalkVolume` | 
 | 
 | 
 |

11. Android 端新增功能，支持插入多个外接摄像头，用户可以根据需要切换选择摄像头。具体参看 API：

    - 创建视频设备管理实例：


    - 获取当前系统内视频采集设备列表：


    - 设置当前视频采集设备：


### 功能优化 

1. 硬件耳返功能新增支持了 OPPO，VIVO，XIAOMI 等多个机型。

2. 客户端字幕翻译功能新增支持同时显示原文和译文字幕。

3. 新增了 `onActiveVideoLayer` 回调。在使用自定义视频编解码功能时，发送端可以根据此回调，按需编码，节约编码消耗的性能资源。

| 功能简述 | Android | iOS | macOS | Windows | Linux |
	|---|---|---|---|---|---|
	| 视频流可发送状态发生变化时的回调 | 
 | 
 | 
 | 
 | 
 |

4. 优化了自定义视频编解码功能，支持在音频自定义订阅场景下使用。如果你要在音频自定义订阅场景下使用自定义视频编解码功能，你应在解码端，通过 `setVideoDecoderConfig` 接口，将任意远端主流/屏幕流的解码参数设置为自定义编解码。

5. 增加了客户端截取视频画面时的报错场景：超过 1s 时没有截取到视频画面会收到错误码。参看：

| 功能简述 | Android | iOS | macOS | Windows |
	|---|---|---|---|---|
	| 截取本地视频画面时的回调 | 
 | `onTakeLocalSnapshotResult:streamIndex:image:errorCode:` | `onTakeLocalSnapshotResult:streamIndex:image:errorCode:` | 
 |
	| 截取远端视频画面时的回调 | 
 | `onTakeRemoteSnapshotResult:streamKey:image:errorCode:` | `onTakeRemoteSnapshotResult:streamKey:image:errorCode:` | 
 |

6. Android 端应用在使用 RTC SDK 进行视频内部采集时，长时间退后台（>1min）后再次进入前台时，RTC 将自动恢复视频采集，无需额外操作。

7. 在通过回调获取本地音频信息时，支持获取人声基频信息。参看：

| 功能简述 | Android | iOS | macOS | Windows | Linux |
	|---|---|---|---|---|---|
	| 启用音频信息提示 | 
 | 
 | 
 | 
 | 
 |
	| 获取本地音频信息 | 
 | 
 | 
 | 
 | 
 |

8. 支持自定义本地日志文件名前缀，最终的日志文件名为 `前缀 + "_" + 文件创建时间 + "_rtclog".log`。

| 功能简述 | Android | iOS | macOS | Windows | Linux |
	|---|---|---|---|---|---|
	| 设置本地日志文件名前缀 | 
 | 
 | 
 | 
 | 
 |

9. 基础美颜新增清晰子项，并优化美颜参数默认值。使用清晰子项需要集成 v4.4.2+ 版本的特效 SDK。各基础美颜子项的默认强度调整为：美白 0.7，磨皮 0.8，锐化 0.5，清晰 0.7。

| 功能简述 | Android | iOS | macOS | Windows |
	|---|---|---|---|---|
	| 开启/关闭基础美颜 | 
 | 
 | 
 | 
 |
	| 调整基础美颜强度 | 
 | 
 | 
 | 
 |

## 3.55 (Unity) 

该版本于 2023 年 10 月 27 日发布。

### 新增特性 

| 功能模块 | 说明 | 相关文档 |
|---|---|---|
| 音频路由 | 支持将默认的音频播放设备设置为听筒或扬声器。 支持获取当前的音频路由设置。  | 
 |
| 音频回调 | 支持开启和关闭指定的音频数据帧回调。 | 
 |
| 音频录制 | 新增录制本地通话的功能。 | 
 |
| 音视频传输 | 支持订阅所有用户和取消订阅所有用户。在上麦人数固定的场景中，可以快速实现麦位切换。 | 
 |
| 范围语音 | 增加音量衰减模式的选择接口，可根据场景需要，选择音量根据距离线性衰减或非线形衰减。音量随距离增大进行非线性衰减更符合真实世界中声音的表现。 支持在启用范围语音功能时，设置相互通话不受衰减影响的小队。 | 
 |
| 空间音频 | 新增关闭本地用户朝向对本地用户发声效果影响的接口。 | 
 |
| 房间管理 | 新增创建房间失败回调。 | 
 |
| 消息 | 新增消息发送和接收回调。 | 
 |

### 升级必看 

| 功能模块 | 说明 | 相关文档 |
|---|---|---|
|  音频管理  自定义流处理  | 返回值由 `void` 变为 `int`。 | 
 |

## 3.54 

该版本于 2023 年 9 月 1 日发布。

### 升级必看 

如果你需要将应用中使用的旧版本 RTC SDK 升级为最新版，参看：
。

### 新增特性 

1. 该版本 iOS、Windows、macOS、Linux 端新增音频编解码器插件、视频编解码器插件，iOS 端新增视频锐化插件。各端插件详情参看
文档。

2. 支持获取房间 ID。参看：

| 功能简述 | Android | iOS | macOS | Windows | Linux |
	|---|---|---|---|---|---|
	| 获取房间 ID | 
 | 
 | 
 | 
 | 
 |

3. 在 Android，iOS 和 macOS 平台上，支持获取 C++ 层的 `IRTCVideo`。在一些场景下，获取 C++ 层 `IRTCVideo`，并通过其完成操作，相较于通过 Java / OC 封装层完成有显著更高的执行效率。典型的场景有：视频/音频帧自定义处理，音视频通话加密等。参看：

| 功能简述 | Android | iOS | macOS |
	|---|---|---|---|
	| 获取 C++ 层 IRTCVideo 句柄 | 
 | 
 | 
 |

4. 在 Android 和 iOS 平台上，在通过 RTC SDK 内部机制采集视频时，支持关闭人脸自动曝光功能和动态采集帧率功能。

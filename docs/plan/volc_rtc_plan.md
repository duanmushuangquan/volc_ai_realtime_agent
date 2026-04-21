# volc_rtc_plan 实施计划

## 背景
基于 volc_rtc 调研，火山 RTC SDK 是项目的核心通信层。需要先跑通基础 Demo，验证 RTC 能力后再进行封装。

## 阶段目标
1. 跑通火山 RTC Linux C++ Demo
2. 封装 RTC 基础能力（进房/退房/发布订阅）
3. 集成到项目中

## 里程碑
- [ ] 云电脑环境配置完成
- [ ] Demo 编译通过
- [ ] Demo 运行验证（能进房/收发音视频）
- [ ] RTC 封装层实现

---

## 子任务清单

### [ ] Task 1: 云电脑环境配置
**目标**: 在云电脑上配置好编译环境

**实施方案**:
1. 安装 gcc/g++ >= 9.0
2. 安装 CMake >= 3.20
3. 安装 OpenSSL 开发库
4. 配置音频驱动 (ALSA/PulseAudio)
5. 克隆项目代码

**验收标准**:
- [ ] gcc --version 显示 >= 9.0
- [ ] cmake --version 显示 >= 3.20
- [ ] openssl version 显示版本
- [ ] 项目代码克隆到本地

**文件改动**:
- 无

---

### [ ] Task 2: 下载并解压火山 RTC SDK
**目标**: 获取火山 RTC Linux C++ SDK

**实施方案**:
1. 访问火山控制台获取下载链接
2. 下载 veRTC SDK
3. 解压到 vendor/veRTC_SDK/
4. 检查头文件和 .so 文件

**验收标准**:
- [ ] vendor/veRTC_SDK/ 目录存在
- [ ] 包含头文件 (veRTCEngine.h 等)
- [ ] 包含库文件 (.so 或 .a)

**文件改动**:
- vendor/veRTC_SDK/ (新增目录)

---

### [ ] Task 3: 编译 Linux Demo
**目标**: 编译成功，无链接错误

**实施方案**:
1. 查看 Demo 的 CMakeLists.txt
2. 配置 CMake
3. 执行 make 编译
4. 修复编译错误（如有）

**验收标准**:
- [ ] cmake 配置成功
- [ ] make 编译无错误
- [ ] 生成可执行文件

**文件改动**:
- 无（仅编译）

---

### [ ] Task 4: 运行 Demo 验证
**目标**: 能进房，能收发音视频流

**实施方案**:
1. 配置 AppID/Token/RoomID
2. 运行 Demo
3. 验证进房成功
4. 测试双端音视频互通

**验收标准**:
- [ ] 日志显示进房成功
- [ ] 能听到自己的声音（回音测试）
- [ ] 两个设备能互通

**文件改动**:
- configs/rtc_demo.json (配置文件)

---

### [ ] Task 5: 设计 RTC 封装层接口
**目标**: 设计出符合项目需求的 RTC 封装接口

**实施方案**:
1. 定义 IRTCClient 接口
2. 定义回调接口 (IRTCEventHandler)
3. 定义发布/订阅接口
4. 编写接口文档

**验收标准**:
- [ ] IRTCClient 接口定义完成
- [ ] IRTCEventHandler 接口定义完成
- [ ] 接口文档编写完成
- [ ] 代码通过编译

**文件改动**:
- `src/volc_ai_realtime_agent/rtc/rtc_client.h`
- `src/volc_ai_realtime_agent/rtc/rtc_client.cpp`

---

### [ ] Task 6: 实现 RTC 封装层
**目标**: 实现 RTC 封装层，与 Demo 逻辑分离

**实施方案**:
1. 实现 RTCClient 类
2. 实现事件回调处理
3. 集成到项目中
4. 编写单元测试

**验收标准**:
- [ ] RTCClient 类实现完成
- [ ] 单元测试通过
- [ ] Demo 能运行（封装后的接口）
- [ ] 示例代码编写完成

**文件改动**:
- `src/volc_ai_realtime_agent/rtc/rtc_client.cpp`
- `tests/unit/rtc_client_test.cpp`
- `examples/rtc_basic.cpp`

---

## 执行记录

| 日期 | 完成任务 | 状态 | 备注 |
|------|----------|------|------|
| | | | |

---

## 使用说明

### 查看计划进度
```bash
make show-plan TOPIC=volc_rtc
```

### 标记任务完成
```bash
make done TASK=1 TOPIC=volc_rtc
```

---

*创建时间: 2024-04-21*

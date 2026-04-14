
Title: Linux 桌面版
URL: https://www.volcengine.com/docs/6348/131050?lang=zh
Publish Time: 2024-12-02T19:05:50+08:00
File Type: None
========================================

Content:
跑通示例项目

Linux 桌面版

复制全文

下载 pdf

Linux 桌面版

快速开始 Demo 是 RTC 提供的基本音视频通话功能的开源示例工程文件。获取该工程文件后，你可以快速构建应用，感受 RTC 的通话效果；也能通过阅读代码，了解基本音视频通话的最佳实践。

应用使用说明 

使用该工程文件构建应用后，你可以使用该应用实现基本音视频通话功能。

你和你的同事必须使用同一 Appid 且加入同一个房间，才能成功进行音视频通话。

本文以 Ubuntu 系统为例进行说明。

前提条件 

- 安装在 x86 架构硬件上的 Linux 系统，其中 glibc 2.27+

- 已安装音视频相关的库：
 、 
、libva2

    - 安装 OpenGL 命令： `sudo apt install libgl-dev`

    - 安装 PulseAudio 命令：`sudo apt install libpulse-dev`

    - 安装 libva2 命令：`sudo apt-get install libva2`

- 已安装 CMake 3.13+

- 已安装 Qt 5.11+

    - 安装 qtbase5-dev 命令： `sudo apt install qtbase5-dev`

    - 或
进行安装

- 已获取 RTC 


操作步骤 


## 步骤 1：配置环境变量

配置 QT 环境变量（全局基本和用户基本）：

- 全局环境变量

```
#sudo	gedit	/etc/profile export	QTDIR=QT安装目录
export	PATH=$QTDIR/bin:$PATH export	LD_LIBRARY_PATH=$QTDIR/lib:$LD_LIBRARY_PATH 

bash
```
- 用户环境变量

```
#gedit $HOME/.bashrc	或者	gedit	~/.bashrc	 export QTDIR=QT安装目录
export PATH=$QTDIR/bin:$PATH export LD_LIBRARY_PATH=$QTDIR/lib:$LD_LIBRARY_PATH 

bash
```
## 步骤 2：获取 AppId 和临时 Token

关于在控制台获取 AppId 和临时 Token，参看
。

临时 Token 生成时填写的房间 ID 和用户 ID 与 Demo 登录页的房间 ID 和用户 ID 一致，若输入的房间 ID 或用户 ID 不一致，将无法进入正确房间与其他用户进行音视频通话。 临时 Token 仅用于测试或跑通 Demo，你可以通过阅读
了解更多 Token 相关信息。

## 步骤 3：配置 Demo 工程文件

1. 修改 AppID。 使用在控制台获取的 `AppId` 覆盖 `sources/Constants.h` 里 `APP_ID` 的值。

2. 修改 TOKEN。 使用在控制台获取的`临时 Token` 覆盖 `sources/Constants.h` 里 `TOKEN` 的值。



3. 打开 终端 窗口下，进入 `QuickStart_Demo` 目录，执行 `cmake -B build`命令，在 `build` 目录下生成工程。

## 步骤 4：编译 Demo 

执行 `cmake --build build` 命令进行编译。

## 步骤 5：运行 Demo 

运行程序 `./build/QuickStart`。


运行开始界面如下。




## 步骤 6：体验音视频通话功能 

为更好地体验实时音视频互动效果，你可以邀请一位朋友使用另一台设备运行该示例项目（需确保两个设备配置示例项目时填入的 App ID 和 AppKey 一致）。当你们输入相同的房间名加入房间后，即可在同一房间中体验音视频通话。

## 后续步骤 

在完成音视频互动后，你可以阅读以下文档进一步了解：

- 在测试或生产环境中，你需要使用 Token 进行鉴权。为保证通信安全，推荐从服务器中获取 Token，详情请参考
。

- 在实现不同的视频通话场景时，你需要配置不同的视频发布参数以达到最佳效果，详情请参考
。

演示视频 

常见问题 


1. Demo 运行后，出现错误弹窗。
SDK 内部遇到不可恢复的错误，参看
。

2. 快速开始 Demo 跑通后，两个测试设备距离较近会产生啸叫。
通信两端的设备在同一房间内，且处于公放状态，连环增益大于 1 时会产生近场啸叫，与 Demo 本身无关。请将各测试设备保持一定距离。

最近更新时间：2024.12.02 19:05:50













相关文档







相关产品






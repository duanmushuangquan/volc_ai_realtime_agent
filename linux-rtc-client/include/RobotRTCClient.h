/**
 * RobotRTCClient.h
 * 
 * 机器人RTC客户端 - Linux版本
 * 用于火山引擎AI音视频互动方案
 * 
 * 功能：
 * 1. RTC房间管理
 * 2. 音频采集和播放
 * 3. 消息收发（文本、二进制）
 * 4. 事件回调处理
 */

#ifndef ROBOT_RTC_CLIENT_H
#define ROBOT_RTC_CLIENT_H

#include <string>
#include <memory>
#include <functional>
#include <vector>
#include <map>

// 音频帧结构
struct AudioFrame {
    const uint8_t* data;    // 音频数据
    size_t len;            // 数据长度
    uint64_t timestamp;    // 时间戳
    int sample_rate;       // 采样率
    int channels;          // 声道数
    int bits_per_sample;   // 位深度
};

// RTC房间配置
struct RTCRoomConfig {
    std::string room_id;       // 房间ID
    std::string user_id;       // 用户ID
    std::string token;         // 认证token
    bool enable_audio;         // 启用音频
    bool enable_video;         // 启用视频
};

// RTC引擎事件处理器
class IRTCEngineEventHandler {
public:
    virtual ~IRTCEngineEventHandler() = default;
    
    // 连接事件
    virtual void onConnected() = 0;
    virtual void onDisconnected(int reason) = 0;
    virtual void onError(int error_code, const std::string& message) = 0;
    
    // 用户事件
    virtual void onUserJoined(const std::string& user_id) = 0;
    virtual void onUserLeft(const std::string& user_id) = 0;
    
    // 音频事件
    virtual void onRemoteAudioFrame(const std::string& user_id, const AudioFrame& frame) = 0;
    virtual void onAudioVolumeIndication(const std::string& user_id, int volume) = 0;
    
    // 消息事件
    virtual void onUserTextMessage(const std::string& user_id, const std::string& text) = 0;
    virtual void onUserBinaryMessage(const std::string& user_id, const uint8_t* data, size_t len) = 0;
    
    // 统计事件
    virtual void onStatistics(const std::string& user_id, int bitrate, int packet_loss) = 0;
};

// RTC引擎接口
class IRTCEngine {
public:
    virtual ~IRTCEngine() = default;
    
    // 初始化
    virtual int initialize(const std::string& app_id) = 0;
    
    // 房间操作
    virtual int joinRoom(const RTCRoomConfig& config) = 0;
    virtual int leaveRoom() = 0;
    
    // 音频操作
    virtual int startAudioCapture() = 0;
    virtual int stopAudioCapture() = 0;
    virtual int playAudio(const uint8_t* data, size_t len) = 0;
    virtual int sendAudioFrame(const AudioFrame& frame) = 0;
    
    // 消息操作
    virtual int sendUserTextMessage(const std::string& user_id, const std::string& text) = 0;
    virtual int sendUserBinaryMessage(const std::string& user_id, const uint8_t* data, size_t len) = 0;
    
    // 配置
    virtual int setAudioConfig(int sample_rate, int channels, int bits_per_sample) = 0;
    virtual int setEventHandler(IRTCEngineEventHandler* handler) = 0;
    
    // 生命周期
    virtual void release() = 0;
};

// 创建RTC引擎工厂
std::unique_ptr<IRTCEngine> CreateRTCEngine();

#endif // ROBOT_RTC_CLIENT_H

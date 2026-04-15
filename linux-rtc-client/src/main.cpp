/**
 * main.cpp
 * 
 * 机器人RTC客户端主程序
 * 演示如何集成火山引擎AI音视频互动方案
 */

#include "RobotRTCClient.h"
#include <iostream>
#include <string>
#include <csignal>
#include <thread>
#include <chrono>

// 全局引擎指针
std::unique_ptr<IRTCEngine> g_engine;
bool g_running = true;

// 信号处理
void signal_handler(int signal) {
    std::cout << "\n[Main] Received signal " << signal << ", shutting down..." << std::endl;
    g_running = false;
    
    if (g_engine) {
        g_engine->leaveRoom();
        g_engine->stopAudioCapture();
        g_engine->release();
    }
    
    exit(0);
}

// 事件处理器实现
class RobotEventHandler : public IRTCEngineEventHandler {
public:
    void onConnected() override {
        std::cout << "[Event] Connected to room" << std::endl;
    }
    
    void onDisconnected(int reason) override {
        std::cout << "[Event] Disconnected, reason: " << reason << std::endl;
    }
    
    void onError(int error_code, const std::string& message) override {
        std::cerr << "[Event] Error " << error_code << ": " << message << std::endl;
    }
    
    void onUserJoined(const std::string& user_id) override {
        std::cout << "[Event] User joined: " << user_id << std::endl;
    }
    
    void onUserLeft(const std::string& user_id) override {
        std::cout << "[Event] User left: " << user_id << std::endl;
    }
    
    void onRemoteAudioFrame(const std::string& user_id, const AudioFrame& frame) override {
        // 播放远程音频
        if (g_engine) {
            g_engine->playAudio(frame.data, frame.len);
        }
    }
    
    void onAudioVolumeIndication(const std::string& user_id, int volume) override {
        // std::cout << "[Event] User " << user_id << " volume: " << volume << std::endl;
    }
    
    void onUserTextMessage(const std::string& user_id, const std::string& text) override {
        std::cout << "[Event] Text message from " << user_id << ": " << text << std::endl;
    }
    
    void onUserBinaryMessage(const std::string& user_id, const uint8_t* data, size_t len) override {
        std::cout << "[Event] Binary message from " << user_id << ": " << len << " bytes" << std::endl;
        
        // 解析控制指令（TLV格式）
        parseControlMessage(data, len);
    }
    
    void onStatistics(const std::string& user_id, int bitrate, int packet_loss) override {
        std::cout << "[Stats] " << user_id << " - Bitrate: " << bitrate 
                  << " kbps, Packet loss: " << packet_loss << "%" << std::endl;
    }
    
private:
    // 解析控制消息
    void parseControlMessage(const uint8_t* data, size_t len) {
        if (len < 8) {
            std::cerr << "[Error] Invalid control message length" << std::endl;
            return;
        }
        
        // 解析TLV格式
        // magic_number (4 bytes) + length (4 bytes) + value
        std::string magic(reinterpret_cast<const char*>(data), 4);
        
        if (magic != "ctrl") {
            std::cerr << "[Error] Invalid magic number: " << magic << std::endl;
            return;
        }
        
        // 解析长度（大端序）
        uint32_t json_length = (data[4] << 24) | (data[5] << 16) | 
                                (data[6] << 8) | data[7];
        
        if (json_length > len - 8) {
            std::cerr << "[Error] Invalid JSON length" << std::endl;
            return;
        }
        
        // 解析JSON
        std::string json_str(reinterpret_cast<const char*>(data + 8), json_length);
        std::cout << "[Control] Command: " << json_str << std::endl;
    }
};

// 发送触发新一轮对话指令（手动触发模式）
void sendFinishRecognitionMessage(IRTCEngine* engine, const std::string& bot_id) {
    nlohmann::json json_data;
    json_data["Command"] = "FinishSpeechRecognition";
    
    std::string message = json_data.dump();
    
    // TLV格式封装
    auto binary_message = buildTLVMessage("ctrl", message);
    
    if (engine) {
        engine->sendUserBinaryMessage(bot_id, binary_message.data(), binary_message.size());
    }
}

// 发送打断指令
void sendInterruptMessage(IRTCEngine* engine, const std::string& bot_id) {
    nlohmann::json json_data;
    json_data["Command"] = "Interrupt";
    
    std::string message = json_data.dump();
    auto binary_message = buildTLVMessage("ctrl", message);
    
    if (engine) {
        engine->sendUserBinaryMessage(bot_id, binary_message.data(), binary_message.size());
    }
}

// 构建TLV消息
std::vector<uint8_t> buildTLVMessage(const std::string& type, const std::string& value) {
    std::vector<uint8_t> message;
    
    // 添加magic number
    message.insert(message.end(), type.begin(), type.end());
    
    // 添加长度（大端序）
    uint32_t length = value.size();
    message.push_back((length >> 24) & 0xFF);
    message.push_back((length >> 16) & 0xFF);
    message.push_back((length >> 8) & 0xFF);
    message.push_back(length & 0xFF);
    
    // 添加值
    message.insert(message.end(), value.begin(), value.end());
    
    return message;
}

// 打印帮助信息
void print_help() {
    std::cout << "\n=== Robot RTC Client ===" << std::endl;
    std::cout << "Commands:" << std::endl;
    std::cout << "  help          - Show this help" << std::endl;
    std::cout << "  join <room>   - Join a room" << std::endl;
    std::cout << "  leave         - Leave current room" << std::endl;
    std::cout << "  start         - Start audio capture" << std::endl;
    std::cout << "  stop          - Stop audio capture" << std::endl;
    std::cout << "  send <text>   - Send text message" << std::endl;
    std::cout << "  trigger       - Send trigger message" << std::endl;
    std::cout << "  interrupt     - Send interrupt message" << std::endl;
    std::cout << "  quit          - Quit the program" << std::endl;
    std::cout << std::endl;
}

// 主程序
int main(int argc, char* argv[]) {
    std::cout << "========================================" << std::endl;
    std::cout << "   Robot RTC Client - Linux Version" << std::endl;
    std::cout << "   For AI Audio-Video Interaction" << std::endl;
    std::cout << "========================================" << std::endl;
    
    // 解析命令行参数
    std::string app_id;
    std::string room_id;
    std::string user_id;
    
    for (int i = 1; i < argc; i++) {
        std::string arg = argv[i];
        
        if (arg == "--app-id" && i + 1 < argc) {
            app_id = argv[++i];
        } else if (arg == "--room-id" && i + 1 < argc) {
            room_id = argv[++i];
        } else if (arg == "--user-id" && i + 1 < argc) {
            user_id = argv[++i];
        } else if (arg == "--help") {
            std::cout << "Usage: " << argv[0] << " [options]" << std::endl;
            std::cout << "Options:" << std::endl;
            std::cout << "  --app-id <id>    Set App ID" << std::endl;
            std::cout << "  --room-id <id>    Set Room ID" << std::endl;
            std::cout << "  --user-id <id>   Set User ID" << std::endl;
            return 0;
        }
    }
    
    // 设置默认值
    if (app_id.empty()) app_id = "your_app_id";
    if (room_id.empty()) room_id = "robot-room-001";
    if (user_id.empty()) user_id = "robot-client-001";
    
    // 设置信号处理
    signal(SIGINT, signal_handler);
    signal(SIGTERM, signal_handler);
    
    // 创建RTC引擎
    g_engine = CreateRTCEngine();
    
    if (!g_engine) {
        std::cerr << "[Error] Failed to create RTC engine" << std::endl;
        return 1;
    }
    
    // 初始化引擎
    int ret = g_engine->initialize(app_id);
    if (ret != 0) {
        std::cerr << "[Error] Failed to initialize RTC engine" << std::endl;
        return 1;
    }
    
    // 设置事件处理器
    RobotEventHandler event_handler;
    g_engine->setEventHandler(&event_handler);
    
    // 配置音频参数
    g_engine->setAudioConfig(16000, 1, 16);
    
    // 加入房间
    std::cout << "[Main] Joining room: " << room_id << std::endl;
    
    RTCRoomConfig config;
    config.room_id = room_id;
    config.user_id = user_id;
    config.token = "";
    config.enable_audio = true;
    config.enable_video = false;
    
    ret = g_engine->joinRoom(config);
    if (ret != 0) {
        std::cerr << "[Error] Failed to join room" << std::endl;
        return 1;
    }
    
    // 开始音频采集
    g_engine->startAudioCapture();
    
    // 打印帮助
    print_help();
    
    // 命令循环
    std::string input;
    std::string ai_user_id = "robot-assistant";  // AI Agent的用户ID
    
    while (g_running) {
        std::cout << "\nrobot> ";
        std::getline(std::cin, input);
        
        if (input.empty()) continue;
        
        // 解析命令
        if (input == "help") {
            print_help();
        }
        else if (input.substr(0, 4) == "join") {
            std::string new_room = input.substr(5);
            if (!new_room.empty()) {
                room_id = new_room;
                config.room_id = room_id;
                g_engine->joinRoom(config);
            }
        }
        else if (input == "leave") {
            g_engine->leaveRoom();
        }
        else if (input == "start") {
            g_engine->startAudioCapture();
        }
        else if (input == "stop") {
            g_engine->stopAudioCapture();
        }
        else if (input.substr(0, 4) == "send") {
            std::string text = input.substr(5);
            if (!text.empty()) {
                g_engine->sendUserTextMessage(ai_user_id, text);
            }
        }
        else if (input == "trigger") {
            sendFinishRecognitionMessage(g_engine.get(), ai_user_id);
        }
        else if (input == "interrupt") {
            sendInterruptMessage(g_engine.get(), ai_user_id);
        }
        else if (input == "quit" || input == "exit") {
            break;
        }
        else {
            std::cout << "Unknown command: " << input << std::endl;
            std::cout << "Type 'help' for available commands" << std::endl;
        }
    }
    
    // 清理
    std::cout << "[Main] Cleaning up..." << std::endl;
    g_engine->stopAudioCapture();
    g_engine->leaveRoom();
    g_engine->release();
    
    std::cout << "[Main] Goodbye!" << std::endl;
    return 0;
}

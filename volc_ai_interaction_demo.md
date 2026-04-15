
Title: 判停与对话触发
URL: https://www.volcengine.com/docs/6348/1544164?lang=zh
Publish Time: 2026-01-23T14:05:56+08:00
File Type: None
========================================

Content:
开发指南

判停与对话触发

能否准确判断用户发言是否结束并触发 AI 响应，会直接影响对话自然度和流畅性。判停或触发时机不当，会导致 AI “抢话”（过早响应）或“反应迟钝”（过晚响应）。您可以通过自动或手动方式来控制 AI 的响应触发。

- **自动方式** ：基于用户静音时长或语义判停，自动判断用户发言是否结束并触发 AI 响应。适用于大多数自然对话的场景。

- **手动方式** ：通过 API 指令（比如按键）或字幕结果，手动触发 AI 响应。适用于需要精确控制交互流程的场景。

## 应用场景 

| 场景<br> | 说明 |
|---|---|
| 咨询陪练 | 自动触发：用户自由叙述或提问后，自动触发新一轮对话。手动触发：用户通过“按住说话”按钮进行输入，松开按钮即刻触发 AI 回应。 |
| 在线教育 | 自动触发：学生随时向 AI 助教提问，系统自动识别问题结束并给予解答。手动触发：学生点击“提问”按钮开始说话，再次点击结束，确保问题完整提交后触发解答。 |

## 自动触发 

### 默认策略 

默认情况下，系统会实时监测语音活动。当用户停顿超过预设的静音时长 `ASRConfig.VADConfig.SilenceTime`（默认为 600 ms），系统即认为一轮发言结束，并触发 AI 响应。

- **默认配置**

    - `ASRConfig.TurnDetectionMode`： 0，即开启自动触发新一轮对话。

    - `ASRConfig.VADConfig.SilenceTime`：默认为 600 ms。用户停顿时间若高于该值设定时间，则认为一句话结束。

- **局限性**

    - **反应迟钝** ：对于快节奏对话，600 ms 的等待可能过长，导致用户说完话后，AI 需要额外等待片刻才响应，体感上 AI 响应延迟。

    - **错误打断（抢话）** ：对于慢语速或需要思考停顿的复杂对话，600 ms 可能过短，用户在句子间的正常停顿可能被误判为结束，导致一句话切分成多轮无效的对话。

### 进阶配置：语义判停与预填充 

为了在不同场景下达到最佳的断句效果和响应延迟，建议组合使用配置。

| 参数<br> | 配置建议 |
|---|---|
| `ASRConfig.VADConfig.AIVAD` | 设置为 `true`，以开启智能语义断句。启用后，系统会通过 LLM 对语义完整性进行分析，并结合静音时长进行双重判断，从而更准确地识别长句中的自然停顿，避免将用户完整的一句话错误地切分为多轮对话。<br>注意<br>AIVAD 功能目前在限时免费公测阶段。 |
| `ASRConfig.VADConfig.SilenceTime` | 判停时间。用户停顿时间若高于该值设定时间，则认为一句话结束。请根据实际场景合理配置（比如根据用户语速调整）：<br>**长句或复杂对话（如教学）** ：建议设置为 1000 ms 或更高，为 `AIVAD` 提供更充分的语义判断时间。**短句或简单问答** ：建议设置为一个较短的值，例如 800 ms，以实现快速响应。 |
| `LLMConfig.Prefill` | 设置为 `true`，将 ASR 识别中间结果提前发送给 LLM 进行处理，实现 AI 在用户说话的同时就开始“思考”，从而在用户话音结束时更快地给出响应。 |

## 手动触发 

根据收到的结束信令或字幕结果来触发新一轮对话，实现精准、可靠的交互控制。

### 步骤 1：定义触发时机

在您的业务逻辑中明确触发 AI 回应的节点。常见方式包括：

- **基于业务信令** ：由应用内的特定事件触发，需要您自定义。例如：用户松开“按住说话”按钮、点击 UI 上的“发送”按钮、或完成支付验证等。

- **基于字幕结果** ：在获取到一句完整的语音识别结果后触发。例如，当字幕回调消息中的 `paragraph` 字段为 `true` 时，代表用户的一整段发言已结束，以此触发新一轮对话。如何接收字幕回调并解析，请参见
。

### 步骤 2：启用手动触发模式

调用 `StartVoiceChat` 接口时，将 `ASRConfig.TurnDetectionMode` 设置为 `1`。

### 步骤 3：执行手动触发

收到输入业务信令或字幕结果后，根据您的业务架构，可通过服务端或客户端发送指令来触发新一轮对话。

#### 通过服务端触发

调用 `UpdateVoiceChat` 接口，并将 `Command` 设置为 `FinishSpeechRecognition`。配置示例如下：

```
{
  "AppId": "YOUR_AppId",     // 与 StartVoiceChat 的一致
  "RoomId": "YOUR_RoomId",      // 与 StartVoiceChat 的一致
  "TaskId": "YOUR_TaskId",      // 与 StartVoiceChat 的一致
  "Command": "FinishSpeechRecognition" //必须为该值 } 

json
```
#### 通过客户端触发

调用 RTC SDK 的 
 接口发送特定格式的二进制消息，触发新一轮对话。

- `userId`： AI 的 ID，须与 `StartVoiceChat` 中定义的一致。

- `buffer`：一个二进制数据块，需遵循 TLV (Type-Length-Value) 格式封装。如下所示：



| 参数名<br> | 类型<br> | 描述 |
	|---|---|---|
	| magic_number | binary | 消息格式标识符，固定为 `ctrl`。 |
	| length | binary | 消息体 `control_message` 的字节长度，采用大端序（Big-endian）存储。 |
	| control_message | binary | 消息内容，其本身为 JSON 格式的字符串。内容如下（`Command` 为固定值）：<br>`{"Command": "FinishSpeechRecognition"}`。 |

##### 配置示例

C++

Java

TypeScript

```
// 发送触发新一轮对话指令 void sendFinishRecognitionMessage(const std::string &uid) {
 nlohmann::json json_data;
 json_data["Command"] = "FinishSpeechRecognition";
 sendUserBinaryMessage(uid, json_data.dump());
}
void buildBinaryMessage(const std::string& magic_number, const std::string& message, size_t& binary_message_length, std::shared_ptr<uint8_t[]>& binary_message) { //将字符串包装成 TLV
    auto magic_number_length = magic_number.size();
 auto message_length = message.size();

 binary_message_length = magic_number_length + 4 + message_length;
 binary_message = std::shared_ptr<uint8_t[]>(new uint8_t[binary_message_length]);
 std::memcpy(binary_message.get(), magic_number.data(), magic_number_length);
 binary_message[magic_number_length] = static_cast<uint8_t>((message_length >> 24) & 0xFF);
 binary_message[magic_number_length+1] = static_cast<uint8_t>((message_length >> 16) & 0xFF);
 binary_message[magic_number_length+2] = static_cast<uint8_t>((message_length >> 8) & 0xFF);
 binary_message[magic_number_length+3] = static_cast<uint8_t>(message_length & 0xFF);
 std::memcpy(binary_message.get()+magic_number_length+4, message.data(), message_length);
}

int sendUserBinaryMessage(const std::string &uid, const std::string& message) {
 if (rtcRoom_ != nullptr)
 {
 size_t length = 0;
 std::shared_ptr<uint8_t[]> binary_message = nullptr;
 buildBinaryMessage("ctrl", message, length, binary_message);
 return rtcRoom_->sendUserBinaryMessage(uid.c_str(), static_cast<int>(length), binary_message.get());
 }
 return -1;}
C++
```
```
// 发送触发新一轮对话指令 public void sendFinishRecognitionMessage(String userId) {
 JSONObject json = new JSONObject();
 try {
 json.put("Command", "FinishSpeechRecognition");
 } catch (JSONException e) {
 throw new RuntimeException(e);
 }
 String jsonString = json.toString();
 byte[] buildBinary = buildBinaryMessage("ctrl", jsonString);
 sendUserBinaryMessage(userId, buildBinary);
}
private byte[] buildBinaryMessage(String magic_number, String content) { //将字符串包装成 TLV
    byte[] prefixBytes = magic_number.getBytes(StandardCharsets.UTF_8);
 byte[] contentBytes = content.getBytes(StandardCharsets.UTF_8);
 int contentLength = contentBytes.length;

 ByteBuffer buffer = ByteBuffer.allocate(prefixBytes.length + 4 + contentLength);
 buffer.order(ByteOrder.BIG_ENDIAN);
 buffer.put(prefixBytes);
 buffer.putInt(contentLength);
 buffer.put(contentBytes);
 return buffer.array();
}

public void sendUserBinaryMessage(String userId, byte[] buffer) {
 if (rtcRoom_ != null) {
 rtcRoom_.sendUserBinaryMessage(userId, buffer, MessageConfig.RELIABLE_ORDERED);
 }
}
Java
```
```
import VERTC from '@volcengine/rtc';

/**
 * @brief 智能体配置
 */ const BotName = 'RobotMan_'; // 智能体名称 const CommandKey = 'ctrl'; // 控制命令 const engine = VERTC.createEngine('Your AppID'); // RTC 应用 AppId /**
 * @brief 指令类型
 */ enum COMMAND {
 /**
 * @brief 触发新一轮对话指令
 */
  FinishSpeechRecognition = 'FinishSpeechRecognition',
};

/**
 * @brief 将字符串包装成 TLV
 */ function stringToTLV(inputString: string, type = '') {
 const typeBuffer = new Uint8Array(type.length);

 for (let i = 0; i < type.length; i++) {
 typeBuffer[i] = type.charCodeAt(i);
 }

 const lengthBuffer = new Uint32Array(1);
 const valueBuffer = new TextEncoder().encode(inputString);

 lengthBuffer[0] = valueBuffer.length;

 const tlvBuffer = new Uint8Array(typeBuffer.length + 4 + valueBuffer.length);

 tlvBuffer.set(typeBuffer, 0);

 tlvBuffer[4] = (lengthBuffer[0] >> 24) & 0xff;
 tlvBuffer[5] = (lengthBuffer[0] >> 16) & 0xff;
 tlvBuffer[6] = (lengthBuffer[0] >> 8) & 0xff;
 tlvBuffer[7] = lengthBuffer[0] & 0xff;

 tlvBuffer.set(valueBuffer, 8);

 return tlvBuffer.buffer;
};

/**
 * @brief 发送触发新一轮对话指令
 */
engine.sendUserBinaryMessage(
 BotName,
 stringToTLV(
 JSON.stringify({
 Command: COMMAND.FinishSpeechRecognition,
 }),
 CommandKey,
 )
);

TypeScript
```
最近更新时间：2026.01.23 14:05:56













相关文档







相关产品






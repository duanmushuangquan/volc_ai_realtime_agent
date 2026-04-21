# Token 生成工具

火山 RTC Token 生成工具，支持 Python 和 C++ 实现。

## Python 版本

### 安装依赖

```bash
# 无需额外依赖，Python 3.6+ 内置
```

### 使用方法

#### 命令行参数

```bash
cd src/web/tools/token

# 使用命令行参数
python3 token_generator.py --app-id 123456 --app-key abc123 --room-id test --user-id user1

# 指定有效期（秒）
python3 token_generator.py --app-id 123456 --app-key abc123 --room-id test --user-id user1 --expire 7200
```

#### 配置文件

```bash
# 使用配置文件
python3 token_generator.py --config ../../../config/volc.json --room-id test --user-id user1
```

### 输出示例

```
Token: a1b2c3d4e5f6...==:123456_test_user1_1699999999
Room ID: test
User ID: user1
有效期: 3600 秒

JSON 格式:
{
  "token": "a1b2c3d4e5f6...==:123456_test_user1_1699999999",
  "roomId": "test",
  "userId": "user1",
  "expireIn": 3600,
  "expireAt": 1699999999
}
```

## C++ 版本（待实现）

C++ 版本更适合嵌入到现有 C++ 项目中使用。

### 编译

```bash
cd web/tools/token/cpp
mkdir build
cd build
cmake ..
make
```

### 使用方法

```bash
./token_generator --app-id 123456 --app-key abc123 --room-id test --user-id user1
```

## 原理说明

Token 生成使用 HMAC-SHA256 签名算法：

1. 构造消息：`{appId}_{roomId}_{userId}_{expireTime}`
2. HMAC-SHA256 签名
3. Base64 编码

详见 [docs/research/token.md](../../docs/research/token.md)

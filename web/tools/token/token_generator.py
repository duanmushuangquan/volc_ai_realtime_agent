#!/usr/bin/env python3
"""
火山 RTC Token 生成工具

基于 HMAC-SHA256 签名算法生成 Token

用法:
    python3 token_generator.py --app-id <app_id> --app-key <app_key> --room-id <room_id> --user-id <user_id>

示例:
    python3 token_generator.py --app-id 123456 --app-key abc123 --room-id test_room --user-id user_001

配置文件方式:
    python3 token_generator.py --config ../../config/volc.json --room-id test_room --user-id user_001
"""

import argparse
import hmac
import hashlib
import base64
import json
import time
from pathlib import Path
from typing import Optional


def generate_token(
    app_id: str,
    app_key: str,
    room_id: str,
    user_id: str,
    expire: int = 3600
) -> str:
    """
    生成火山 RTC Token

    Args:
        app_id: 应用 ID
        app_key: 应用密钥
        room_id: 房间 ID
        user_id: 用户 ID
        expire: 有效期（秒），默认 1 小时

    Returns:
        Base64 编码的 Token
    """
    # 计算过期时间
    expire_time = int(time.time()) + expire

    # 构造消息体
    # 格式: {appId}_{roomId}_{userId}_{expireTime}
    message = f"{app_id}_{room_id}_{user_id}_{expire_time}"

    # 使用 HMAC-SHA256 签名
    signature = hmac.new(
        app_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    # 组合 token: 签名 + ":" + 消息体
    token_content = f"{signature}:{message}"

    # Base64 编码
    token = base64.b64encode(token_content.encode('utf-8')).decode('utf-8')

    return token


def generate_token_from_config(
    config_path: str,
    room_id: str,
    user_id: str,
    expire: int = 3600
) -> str:
    """
    从配置文件生成 Token

    Args:
        config_path: 配置文件路径
        room_id: 房间 ID
        user_id: 用户 ID
        expire: 有效期（秒）

    Returns:
        Base64 编码的 Token
    """
    config_file = Path(config_path)

    if not config_file.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # 从配置文件读取 appId 和 appKey
    app_id = config.get('appId')
    app_key = config.get('appKey')

    if not app_id:
        raise ValueError("配置文件中缺少 appId")
    if not app_key:
        raise ValueError("配置文件中缺少 appKey")

    return generate_token(
        app_id=app_id,
        app_key=app_key,
        room_id=room_id,
        user_id=user_id,
        expire=expire
    )


def main():
    parser = argparse.ArgumentParser(
        description='火山 RTC Token 生成工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用命令行参数
  python3 token_generator.py --app-id 123456 --app-key abc123 --room-id test --user-id user1

  # 使用配置文件
  python3 token_generator.py --config ../../config/volc.json --room-id test --user-id user1

  # 指定有效期
  python3 token_generator.py --app-id 123456 --app-key abc123 --room-id test --user-id user1 --expire 7200
        """
    )

    parser.add_argument('--app-id', help='应用 ID')
    parser.add_argument('--app-key', help='应用密钥')
    parser.add_argument('--room-id', required=True, help='房间 ID')
    parser.add_argument('--user-id', required=True, help='用户 ID')
    parser.add_argument('--expire', type=int, default=3600,
                        help='有效期（秒），默认 3600')
    parser.add_argument('--config', help='配置文件路径（优先级高于命令行参数）')

    args = parser.parse_args()

    try:
        if args.config:
            # 从配置文件读取
            token = generate_token_from_config(
                config_path=args.config,
                room_id=args.room_id,
                user_id=args.user_id,
                expire=args.expire
            )
            print(f"从配置文件生成: {args.config}")
        else:
            # 从命令行参数读取
            if not args.app_id or not args.app_key:
                print("错误: 必须提供 --app-id 和 --app-key，或使用 --config")
                print("使用 --help 查看帮助")
                return 1

            token = generate_token(
                app_id=args.app_id,
                app_key=args.app_key,
                room_id=args.room_id,
                user_id=args.user_id,
                expire=args.expire
            )

        # 输出结果
        print(f"\nToken: {token}")
        print(f"Room ID: {args.room_id}")
        print(f"User ID: {args.user_id}")
        print(f"有效期: {args.expire} 秒")
        print(f"过期时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time()) + args.expire))}")

        # JSON 格式输出
        print(f"\nJSON 格式:")
        print(json.dumps({
            "token": token,
            "roomId": args.room_id,
            "userId": args.user_id,
            "expireIn": args.expire,
            "expireAt": int(time.time()) + args.expire
        }, indent=2, ensure_ascii=False))

        return 0

    except FileNotFoundError as e:
        print(f"错误: {e}")
        return 1
    except ValueError as e:
        print(f"错误: {e}")
        return 1
    except Exception as e:
        print(f"错误: {e}")
        return 1


if __name__ == '__main__':
    exit(main())

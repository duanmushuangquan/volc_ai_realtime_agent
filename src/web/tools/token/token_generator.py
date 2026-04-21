#!/usr/bin/env python3
"""
火山 RTC Token 生成工具

使用官方 AccessToken.py 生成正确的 Token 格式
"""

import argparse
import sys
import os
import time

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from AccessToken import AccessToken, PrivSubscribeStream, PrivPublishStream


def generate_token(app_id: str, app_key: str, room_id: str, user_id: str, expire: int = 604800) -> str:
    """
    生成火山 RTC Token
    
    Args:
        app_id: 应用 ID (24位字符串)
        app_key: 应用密钥
        room_id: 房间 ID
        user_id: 用户 ID
        expire: 有效期（秒），默认 7 天
    
    Returns:
        Token 字符串
    """
    # 创建 Token 对象
    token = AccessToken(app_id, app_key, room_id, user_id)
    
    # 添加权限
    # PrivSubscribeStream: 订阅流权限，0 表示不限制
    token.add_privilege(PrivSubscribeStream, 0)
    
    # PrivPublishStream: 发布流权限，设置过期时间
    expire_ts = int(time.time()) + expire
    token.add_privilege(PrivPublishStream, expire_ts)
    
    # 设置 Token 整体过期时间
    token.expire_time(expire_ts)
    
    # 序列化生成 Token
    return token.serialize()


def generate_token_from_config(config_path: str, room_id: str, user_id: str, expire: int = 604800) -> str:
    """
    从配置文件生成 Token
    
    Args:
        config_path: 配置文件路径 (.ini 格式)
        room_id: 房间 ID
        user_id: 用户 ID
        expire: 有效期（秒）
    
    Returns:
        Token 字符串
    """
    import configparser
    
    config = configparser.ConfigParser()
    config.read(config_path)
    
    # 读取配置并去除引号
    app_id = config.get('volc', 'app_id').strip().strip('"\'')
    app_key = config.get('volc', 'app_key').strip().strip('"\'')
    
    return generate_token(
        app_id=app_id,
        app_key=app_key,
        room_id=room_id,
        user_id=user_id,
        expire=expire
    )


def main():
    parser = argparse.ArgumentParser(description='火山 RTC Token 生成工具')
    parser.add_argument('--app-id', help='应用 ID (24位字符串)')
    parser.add_argument('--app-key', help='应用密钥')
    parser.add_argument('--room-id', required=True, help='房间 ID')
    parser.add_argument('--user-id', required=True, help='用户 ID')
    parser.add_argument('--expire', type=int, default=604800, help='有效期（秒），默认 604800 (7天)')
    parser.add_argument('--config', help='配置文件路径（优先级高于命令行参数）')
    
    args = parser.parse_args()
    
    if args.config:
        # 从配置文件读取
        token = generate_token_from_config(
            config_path=args.config,
            room_id=args.room_id,
            user_id=args.user_id,
            expire=args.expire
        )
    else:
        # 从命令行参数读取
        if not args.app_id or not args.app_key:
            print("错误: 必须提供 --app-id 和 --app-key，或使用 --config")
            return 1
        
        token = generate_token(
            app_id=args.app_id,
            app_key=args.app_key,
            room_id=args.room_id,
            user_id=args.user_id,
            expire=args.expire
        )
    
    print(f"Token: {token}")
    print(f"有效期: {args.expire} 秒")
    
    return 0


if __name__ == '__main__':
    exit(main())

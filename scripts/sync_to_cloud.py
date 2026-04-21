#!/usr/bin/env python3
"""
Cloud Sync Tool - Git + Webhook 工作流

功能：
1. 推送到 GitHub
2. 触发云电脑 Webhook
3. 等待编译结果

用法：
    python3 scripts/sync_to_cloud.py                    # 推送并触发编译
    python3 scripts/sync_to_cloud.py --push-only     # 仅推送
    python3 scripts/sync_to_cloud.py --wait-result    # 等待结果
    python3 scripts/sync_to_cloud.py --check-status   # 检查云电脑状态
"""

import argparse
import subprocess
import time
import requests
import sys
import os
from pathlib import Path

# ============ 配置 ============
CLOUD_CONFIG = {
    "ip": "115.190.107.107",
    "user": "coze",
    "ssh_key": ".ssh/id_ed25519",
    "work_dir": "/home/coze/projects/volc_ai_realtime_agent",
    "webhook_port": 8888,  # Webhook 端口
}

GITHUB_REMOTE = "origin"
GITHUB_BRANCH = "main"


def run_cmd(cmd: str, check: bool = True) -> subprocess.CompletedProcess:
    """执行 shell 命令"""
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"  [ERROR] {result.stderr}")
        sys.exit(1)
    return result


def check_ssh_connection() -> bool:
    """检查 SSH 连接"""
    try:
        result = subprocess.run(
            f"ssh -i {CLOUD_CONFIG['ssh_key']} "
            f"-o StrictHostKeyChecking=no "
            f"-o ConnectTimeout=5 "
            f"{CLOUD_CONFIG['user']}@{CLOUD_CONFIG['ip']} 'echo ok'",
            shell=True, capture_output=True, text=True
        )
        return result.returncode == 0
    except Exception:
        return False


def sync_to_github(auto_commit: bool = True) -> bool:
    """推送代码到 GitHub"""
    print("\n[1/3] 同步到 GitHub...")

    # 检查 Git 状态
    result = run_cmd("git status --porcelain", check=False)
    if not result.stdout.strip():
        print("  没有需要推送的更改")
        return False

    if auto_commit:
        # 添加所有文件
        run_cmd("git add -A")

        # 获取提交消息（从最新提交或自动生成）
        result = run_cmd("git log -1 --pretty=%s", check=False)
        message = result.stdout.strip() or "chore: sync from Coze sandbox"

        # 提交
        run_cmd(f"git commit -m '{message}'")

    # 推送
    result = run_cmd(f"git push {GITHUB_REMOTE} {GITHUB_BRANCH}", check=False)
    if result.returncode != 0:
        print(f"  [WARN] GitHub 推送失败: {result.stderr}")
        return False

    print("  GitHub 推送成功")
    return True


def trigger_webhook(secret: str = "") -> bool:
    """触发云电脑 Webhook"""
    print("\n[2/3] 触发云电脑 Webhook...")

    webhook_url = f"http://{CLOUD_CONFIG['ip']}:{CLOUD_CONFIG['webhook_port']}/webhook/git"

    try:
        payload = {
            "event": "git_push",
            "branch": GITHUB_BRANCH,
            "timestamp": time.time()
        }

        headers = {"Content-Type": "application/json"}
        if secret:
            import hashlib, hmac
            import json
            signature = "sha1=" + hmac.new(
                secret.encode(),
                json.dumps(payload).encode(),
                hashlib.sha1
            ).hexdigest()
            headers["X-Hub-Signature"] = signature

        response = requests.post(
            webhook_url,
            json=payload,
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            print("  Webhook 触发成功")
            return True
        else:
            print(f"  Webhook 返回: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"  Webhook 连接失败: 云电脑端口 {CLOUD_CONFIG['webhook_port']} 未开放")
        print(f"  请确保云电脑已启动: python3 scripts/cloud_build.py --webhook")
        return False
    except requests.exceptions.RequestException as e:
        print(f"  Webhook 触发失败: {e}")
        return False


def check_build_status() -> dict:
    """检查云电脑编译状态"""
    print(f"\n检查云电脑状态...")

    try:
        url = f"http://{CLOUD_CONFIG['ip']}:{CLOUD_CONFIG['webhook_port']}/webhook/git"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  服务状态: {data.get('status', 'unknown')}")
            if 'build' in data:
                build = data['build']
                print(f"  构建状态: {build.get('status', 'unknown')}")
                print(f"  消息: {build.get('message', '')}")
                print(f"  进度: {build.get('progress', 0)}%")
            return data
        else:
            print(f"  HTTP {response.status_code}")
            return {}
    except requests.exceptions.ConnectionError:
        print(f"  无法连接到云电脑")
        return {}


def wait_for_result(timeout: int = 600) -> bool:
    """等待编译结果"""
    print(f"\n[3/3] 等待编译结果 (超时 {timeout}s)...")

    start_time = time.time()
    last_status = None

    while time.time() - start_time < timeout:
        try:
            url = f"http://{CLOUD_CONFIG['ip']}:{CLOUD_CONFIG['webhook_port']}/webhook/git"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()

                if 'build' in data:
                    build = data['build']
                    status = build.get('status', 'unknown')

                    # 状态变化时打印
                    if status != last_status:
                        print(f"  状态: {status} - {build.get('message', '')}")
                        last_status = status

                    if status == "success":
                        print("\n  编译成功!")
                        return True
                    elif status == "failed":
                        print(f"\n  编译失败: {build.get('message', '')}")
                        return False

            time.sleep(10)
        except requests.exceptions.RequestException:
            time.sleep(10)

    print("  等待超时")
    return False


def ssh_to_cloud():
    """SSH 连接到云电脑"""
    print(f"\n连接到云电脑...")
    print(f"  IP: {CLOUD_CONFIG['ip']}")
    print(f"  用户: {CLOUD_CONFIG['user']}")
    print(f"  工作目录: {CLOUD_CONFIG['work_dir']}")
    print()
    os.system(
        f"ssh -i {CLOUD_CONFIG['ssh_key']} "
        f"-o StrictHostKeyChecking=no "
        f"{CLOUD_CONFIG['user']}@{CLOUD_CONFIG['ip']}"
    )


def main():
    parser = argparse.ArgumentParser(description="同步代码到云电脑")
    parser.add_argument("--push-only", action="store_true", help="仅推送，不触发 webhook")
    parser.add_argument("--wait-result", action="store_true", help="等待编译结果")
    parser.add_argument("--check-status", action="store_true", help="检查云电脑状态")
    parser.add_argument("--ssh", action="store_true", help="SSH 连接到云电脑")
    parser.add_argument("--commit-msg", type=str, default="", help="自定义提交消息")
    args = parser.parse_args()

    print("=" * 50)
    print("Cloud Sync Tool - Git + Webhook")
    print("=" * 50)

    # 检查状态模式
    if args.check_status:
        check_build_status()
        return

    # SSH 模式
    if args.ssh:
        ssh_to_cloud()
        return

    # 检查 SSH 连接
    print("\n[0/3] 检查 SSH 连接...")
    if check_ssh_connection():
        print("  SSH 连接正常")
    else:
        print("  SSH 连接失败，请检查公钥是否添加到云电脑")
        print(f"  公钥文件: .ssh/id_ed25519.pub")
        print("\n  添加公钥到云电脑:")
        print(f"  ssh coze@115.190.107.107 'mkdir -p ~/.ssh && echo \"$(cat .ssh/id_ed25519.pub)\" >> ~/.ssh/authorized_keys'")
        sys.exit(1)

    # 推送到 GitHub
    pushed = sync_to_github(auto_commit=not args.commit_msg)
    if args.commit_msg:
        run_cmd("git add -A")
        run_cmd(f"git commit -m '{args.commit_msg}'")
        run_cmd(f"git push {GITHUB_REMOTE} {GITHUB_BRANCH}")

    if args.push_only or not pushed:
        print("\n[Done] 推送模式完成")
        return

    # 触发 Webhook
    webhook_ok = trigger_webhook()

    if not webhook_ok:
        print("\n[Warn] Webhook 不可用，请手动在云电脑上执行:")
        print(f"  cd {CLOUD_CONFIG['work_dir']} && git pull && python3 scripts/cloud_build.py")
        return

    # 等待结果
    if args.wait_result:
        if not wait_for_result():
            sys.exit(1)
    else:
        print("\n[Done] Webhook 已触发，请在云电脑查看编译结果")
        print(f"  查看状态: make cloud-status")
        print(f"  SSH 连接: make cloud-ssh")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Cloud Sync Tool - Git + Webhook 工作流

功能：
1. 推送到 GitHub
2. 触发云电脑 Webhook
3. 等待编译结果

用法：
    python3 scripts/sync_to_cloud.py                    # 推送并触发编译
    python3 scripts/sync_to_cloud.py --push-only       # 仅推送
    python3 scripts/sync_to_cloud.py --wait-result     # 等待结果
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
    "webhook_url": "http://115.190.107.107:8000/webhook/git",  # 需要在云电脑上启动
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


def sync_to_github() -> bool:
    """推送代码到 GitHub"""
    print("\n[1/3] 同步到 GitHub...")

    # 检查 Git 状态
    result = run_cmd("git status --porcelain", check=False)
    if not result.stdout.strip():
        print("  没有需要推送的更改")
        return False

    # 添加所有文件
    run_cmd("git add -A")

    # 提交
    run_cmd("git commit -m 'chore: sync from Coze sandbox'")

    # 推送
    result = run_cmd(f"git push {GITHUB_REMOTE} {GITHUB_BRANCH}", check=False)
    if result.returncode != 0:
        print(f"  [WARN] GitHub 推送失败: {result.stderr}")
        return False

    print("  GitHub 推送成功")
    return True


def trigger_webhook() -> bool:
    """触发云电脑 Webhook"""
    print("\n[2/3] 触发云电脑 Webhook...")

    try:
        response = requests.post(
            CLOUD_CONFIG['webhook_url'],
            json={"event": "git_push", "branch": GITHUB_BRANCH},
            timeout=10
        )
        if response.status_code == 200:
            print("  Webhook 触发成功")
            return True
        else:
            print(f"  Webhook 返回: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"  Webhook 触发失败: {e}")
        print("  (云电脑需要启动 webhook 服务)")
        return False


def wait_for_result(timeout: int = 300) -> bool:
    """等待编译结果"""
    print(f"\n[3/3] 等待编译结果 (超时 {timeout}s)...")

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(
                f"http://{CLOUD_CONFIG['ip']}:8000/status",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                status = data.get("status", "unknown")
                print(f"  状态: {status}")

                if status == "success":
                    print("\n  编译成功!")
                    return True
                elif status == "failed":
                    print("\n  编译失败!")
                    return False

            time.sleep(10)
        except requests.exceptions.RequestException:
            time.sleep(10)

    print("  等待超时")
    return False


def main():
    parser = argparse.ArgumentParser(description="同步代码到云电脑")
    parser.add_argument("--push-only", action="store_true", help="仅推送，不触发 webhook")
    parser.add_argument("--wait-result", action="store_true", help="等待编译结果")
    args = parser.parse_args()

    print("=" * 50)
    print("Cloud Sync Tool - Git + Webhook")
    print("=" * 50)

    # 检查 SSH 连接
    print("\n[0/3] 检查 SSH 连接...")
    if check_ssh_connection():
        print("  SSH 连接正常")
    else:
        print("  SSH 连接失败，请检查公钥是否添加到云电脑")
        print(f"  公钥: .ssh/id_ed25519.pub")
        sys.exit(1)

    # 推送到 GitHub
    pushed = sync_to_github()

    if args.push_only:
        print("\n[Done] 仅推送模式，跳过 Webhook")
        return

    # 触发 Webhook
    webhook_ok = trigger_webhook()

    if not webhook_ok:
        print("\n[Warn] Webhook 不可用，请手动在云电脑上执行:")
        print(f"  cd {CLOUD_CONFIG['work_dir']} && git pull")
        return

    # 等待结果
    if args.wait_result:
        if not wait_for_result():
            sys.exit(1)
    else:
        print("\n[Done] 请在云电脑上查看编译结果")


if __name__ == "__main__":
    main()

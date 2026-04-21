#!/usr/bin/env python3
"""
Cloud Build Script - 云电脑端编译脚本

功能：
1. 拉取最新代码
2. 配置 CMake
3. 编译项目
4. 运行 Demo
5. 返回结果

用法（在云电脑上运行）：
    python3 scripts/cloud_build.py --project volc_ai_realtime_agent
"""

import argparse
import subprocess
import time
import sys
import os
import json
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# ============ 配置 ============
PROJECT_DIR = Path("/home/coze/projects")
BUILD_DIR = PROJECT_DIR / "build"
STATUS_FILE = PROJECT_DIR / "build_status.json"


def run_cmd(cmd: str, cwd: str = None, check: bool = True) -> subprocess.CompletedProcess:
    """执行 shell 命令"""
    print(f"  $ {cmd}")
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, cwd=cwd
    )
    if check and result.returncode != 0:
        print(f"  [ERROR] {result.stderr}")
        raise RuntimeError(f"命令执行失败: {cmd}")
    return result


def update_status(status: str, message: str = "", progress: int = 0):
    """更新构建状态"""
    data = {
        "status": status,
        "message": message,
        "progress": progress,
        "timestamp": time.time()
    }
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f)


def git_pull(project_dir: Path):
    """拉取最新代码"""
    print("\n[1/5] 拉取最新代码...")
    update_status("pulling", "拉取代码中...", 10)

    result = run_cmd("git pull", cwd=str(project_dir), check=False)
    if result.returncode != 0:
        print(f"  [WARN] Git pull 失败: {result.stderr}")
    else:
        print("  代码拉取成功")


def cmake_configure(project_dir: Path, build_dir: Path):
    """CMake 配置"""
    print("\n[2/5] CMake 配置...")
    update_status("configuring", "CMake 配置中...", 30)

    build_dir.mkdir(exist_ok=True)
    run_cmd("cmake ..", cwd=str(build_dir))
    print("  CMake 配置成功")


def cmake_build(build_dir: Path):
    """CMake 编译"""
    print("\n[3/5] CMake 编译...")
    update_status("building", "编译中...", 50)

    # 并行编译
    nproc = subprocess.run("nproc", shell=True, capture_output=True, text=True)
    jobs = nproc.stdout.strip() or "4"

    run_cmd(f"cmake --build . -j{jobs}", cwd=str(build_dir))
    print("  编译成功")


def run_tests(build_dir: Path):
    """运行测试"""
    print("\n[4/5] 运行测试...")
    update_status("testing", "运行测试中...", 80)

    # 检查是否有测试
    if (build_dir / "test").exists():
        run_cmd("./test/run_tests", cwd=str(build_dir), check=False)
    else:
        print("  没有测试目录，跳过")


def main():
    parser = argparse.ArgumentParser(description="云电脑编译脚本")
    parser.add_argument("--project", default="volc_ai_realtime_agent", help="项目名称")
    parser.add_argument("--webhook", action="store_true", help="启用 Webhook 服务")
    args = parser.parse_args()

    print("=" * 50)
    print("Cloud Build Script")
    print("=" * 50)

    project_dir = PROJECT_DIR / args.project
    build_dir = project_dir / "build"

    try:
        # 1. 拉取代码
        update_status("pulling")
        git_pull(project_dir)

        # 2. CMake 配置
        cmake_configure(project_dir, build_dir)

        # 3. 编译
        cmake_build(build_dir)

        # 4. 运行测试
        run_tests(build_dir)

        # 5. 完成
        update_status("success", "编译成功", 100)
        print("\n" + "=" * 50)
        print("构建成功!")
        print("=" * 50)

    except Exception as e:
        update_status("failed", str(e), 0)
        print(f"\n构建失败: {e}")
        sys.exit(1)


class WebhookHandler(BaseHTTPRequestHandler):
    """Webhook HTTP 处理器"""

    def do_POST(self):
        """处理 Webhook 请求"""
        if self.path == "/webhook/git":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            print("\n" + "=" * 50)
            print("收到 Webhook 请求!")
            print("=" * 50)

            # 触发构建
            threading.Thread(target=self.trigger_build).start()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        else:
            self.send_response(404)
            self.end_headers()

    def trigger_build(self):
        """在新线程中触发构建"""
        time.sleep(2)  # 等待 HTTP 响应
        main()

    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[Webhook] {format % args}")


def start_webhook_server(port: int = 8000):
    """启动 Webhook 服务"""
    server = HTTPServer(("0.0.0.0", port), WebhookHandler)
    print(f"Webhook 服务启动: http://0.0.0.0:{port}")
    print("等待 GitHub Webhook...")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nWebhook 服务停止")


if __name__ == "__main__":
    import sys
    if "--webhook" in sys.argv:
        start_webhook_server()
    else:
        main()

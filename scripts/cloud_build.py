#!/usr/bin/env python3
"""
Cloud Build Script - 云电脑端编译脚本

功能：
1. 拉取最新代码
2. 配置 CMake
3. 编译项目
4. 运行测试
5. Webhook 服务（可选）

用法（在云电脑上运行）：
    # 直接编译
    python3 scripts/cloud_build.py

    # 启动 Webhook 服务（端口 8888）
    python3 scripts/cloud_build.py --webhook --port 8888

    # 带 Secret 验证的 Webhook
    python3 scripts/cloud_build.py --webhook --port 8888 --secret your-github-webhook-secret
"""

import argparse
import hashlib
import hmac
import subprocess
import time
import sys
import os
import json
import logging
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# ============ 配置 ============
PROJECT_DIR = Path("/home/coze/projects")
BUILD_DIR = PROJECT_DIR / "build"
STATUS_FILE = PROJECT_DIR / "build_status.json"

# 日志配置
LOG_FILE = PROJECT_DIR / "cloud_build.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_cmd(cmd: str, cwd: str = None, check: bool = True) -> subprocess.CompletedProcess:
    """执行 shell 命令"""
    logger.info(f"执行命令: {cmd}")
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, cwd=cwd
    )
    if check and result.returncode != 0:
        logger.error(f"命令执行失败: {result.stderr}")
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
        json.dump(data, f, indent=2)


def git_pull(project_dir: Path):
    """拉取最新代码"""
    logger.info("=" * 50)
    logger.info("[1/5] 拉取最新代码...")
    update_status("pulling", "拉取代码中...", 10)

    result = run_cmd("git pull", cwd=str(project_dir), check=False)
    if result.returncode != 0:
        logger.warning(f"Git pull 失败: {result.stderr}")
    else:
        logger.info("  代码拉取成功")


def cmake_configure(project_dir: Path, build_dir: Path):
    """CMake 配置"""
    logger.info("[2/5] CMake 配置...")
    update_status("configuring", "CMake 配置中...", 30)

    build_dir.mkdir(exist_ok=True)

    # 检查是否有 CMakeLists.txt
    if not (project_dir / "CMakeLists.txt").exists():
        logger.warning("  没有找到 CMakeLists.txt，跳过 CMake 配置")
        return False

    run_cmd("cmake ..", cwd=str(build_dir))
    logger.info("  CMake 配置成功")
    return True


def cmake_build(build_dir: Path):
    """CMake 编译"""
    logger.info("[3/5] CMake 编译...")
    update_status("building", "编译中...", 50)

    # 检查是否有 build 目录
    if not build_dir.exists() or not list(build_dir.glob("CMakeCache.txt")):
        logger.warning("  没有 CMake 缓存，跳过编译")
        return False

    # 并行编译
    nproc = subprocess.run("nproc", shell=True, capture_output=True, text=True)
    jobs = nproc.stdout.strip() or "4"

    run_cmd(f"cmake --build . -j{jobs}", cwd=str(build_dir))
    logger.info("  编译成功")
    return True


def run_tests(build_dir: Path):
    """运行测试"""
    logger.info("[4/5] 运行测试...")
    update_status("testing", "运行测试中...", 80)

    # 检查是否有测试脚本
    test_script = build_dir.parent / "scripts" / "test.sh"
    if test_script.exists():
        run_cmd("bash scripts/test.sh", cwd=str(build_dir.parent), check=False)
        logger.info("  测试执行完成")
    else:
        logger.info("  没有测试脚本，跳过")


def build(project_dir: Path, build_dir: Path):
    """执行完整构建流程"""
    try:
        # 1. 拉取代码
        update_status("pulling")
        git_pull(project_dir)

        # 2. CMake 配置
        has_cmake = cmake_configure(project_dir, build_dir)

        # 3. 编译
        if has_cmake:
            cmake_build(build_dir)
        else:
            logger.info("[3/5] 跳过编译（无 CMakeLists.txt）")

        # 4. 运行测试
        run_tests(build_dir)

        # 5. 完成
        update_status("success", "编译成功", 100)
        logger.info("=" * 50)
        logger.info("构建成功!")
        logger.info("=" * 50)
        return True

    except Exception as e:
        logger.exception(f"构建失败: {e}")
        update_status("failed", str(e), 0)
        return False


def main():
    parser = argparse.ArgumentParser(description="云电脑编译脚本")
    parser.add_argument("--project", default="volc_ai_realtime_agent", help="项目名称")
    parser.add_argument("--webhook", action="store_true", help="启用 Webhook 服务")
    parser.add_argument("--port", type=int, default=8888, help="Webhook 端口（默认 8888）")
    parser.add_argument("--secret", default="", help="GitHub Webhook Secret（用于验证）")
    args = parser.parse_args()

    logger.info("=" * 50)
    logger.info("Cloud Build Script")
    logger.info(f"项目目录: {PROJECT_DIR / args.project}")
    logger.info("=" * 50)

    project_dir = PROJECT_DIR / args.project
    build_dir = project_dir / "build"

    if args.webhook:
        # 启动 Webhook 服务
        start_webhook_server(args.port, args.secret, project_dir, build_dir)
    else:
        # 直接执行构建
        build(project_dir, build_dir)


def verify_github_signature(payload: bytes, signature: str, secret: str) -> bool:
    """验证 GitHub Webhook 签名"""
    if not secret:
        return True  # 没有设置 secret，跳过验证

    expected_signature = "sha1=" + hmac.new(
        secret.encode(),
        payload,
        hashlib.sha1
    ).hexdigest()

    return hmac.compare_digest(expected_signature, signature)


class WebhookHandler(BaseHTTPRequestHandler):
    """Webhook HTTP 处理器"""

    def do_GET(self):
        """处理 GET 请求（健康检查）"""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        status = {"status": "ok", "service": "cloud-build-webhook"}
        if STATUS_FILE.exists():
            with open(STATUS_FILE) as f:
                status["build"] = json.load(f)

        self.wfile.write(json.dumps(status).encode())

    def do_POST(self):
        """处理 POST 请求（Webhook 触发）"""
        # 检查路径
        if self.path != "/webhook/git":
            self.send_response(404)
            self.end_headers()
            return

        # 获取请求内容
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        # 验证 GitHub 签名（如果配置了 secret）
        github_signature = self.headers.get("X-Hub-Signature", "")
        if self.server.secret and not verify_github_signature(body, github_signature, self.server.secret):
            logger.warning("Webhook 签名验证失败!")
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'{"error": "Invalid signature"}')
            return

        logger.info("=" * 50)
        logger.info("收到 GitHub Webhook 请求!")
        logger.info(f"  来源: {self.client_address}")
        logger.info(f"  事件: {self.headers.get('X-GitHub-Event', 'unknown')}")
        logger.info("=" * 50)

        # 触发构建（在后台线程）
        threading.Thread(
            target=self.trigger_build,
            args=(body.decode('utf-8', errors='ignore'),),
            daemon=True
        ).start()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status": "ok", "message": "Build triggered"}')

    def trigger_build(self, payload: str = ""):
        """在新线程中触发构建"""
        try:
            # 解析 payload 获取信息
            try:
                data = json.loads(payload)
                event = data.get('head_commit', {}).get('message', 'unknown')
                logger.info(f"触发构建: {event}")
            except json.JSONDecodeError:
                pass

            time.sleep(1)  # 等待 HTTP 响应完成
            build(self.server.project_dir, self.server.build_dir)
        except Exception as e:
            logger.exception(f"构建线程异常: {e}")

    def log_message(self, format, *args):
        """自定义日志格式"""
        logger.info(f"[Webhook] {format % args}")


class ThreadedHTTPServer(HTTPServer):
    """支持多线程的 HTTP 服务器"""
    def __init__(self, server_address, RequestHandlerClass, secret="", project_dir=None, build_dir=None):
        super().__init__(server_address, RequestHandlerClass)
        self.secret = secret
        self.project_dir = project_dir
        self.build_dir = build_dir


def start_webhook_server(port: int = 8888, secret: str = "", project_dir: Path = None, build_dir: Path = None):
    """启动 Webhook 服务"""
    if project_dir is None:
        project_dir = PROJECT_DIR / "volc_ai_realtime_agent"
    if build_dir is None:
        build_dir = project_dir / "build"

    server = ThreadedHTTPServer(
        ("0.0.0.0", port),
        WebhookHandler,
        secret=secret,
        project_dir=project_dir,
        build_dir=build_dir
    )

    logger.info("=" * 50)
    logger.info("Cloud Build Webhook 服务启动")
    logger.info(f"  端口: {port}")
    logger.info(f"  Secret 验证: {'已启用' if secret else '未启用'}")
    logger.info(f"  健康检查: http://0.0.0.0:{port}/webhook/git (GET)")
    logger.info(f"  Webhook 端点: http://0.0.0.0:{port}/webhook/git (POST)")
    logger.info("=" * 50)
    logger.info("等待 GitHub Webhook...")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("\nWebhook 服务停止")


if __name__ == "__main__":
    main()

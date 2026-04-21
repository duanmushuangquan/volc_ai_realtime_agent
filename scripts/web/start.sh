#!/bin/bash
# 启动 Web 开发服务器

set -e

cd "$(dirname "$0")/../.."

echo "启动火山 RTC Web Demo..."
cd src/web/volc_web_sdk
pnpm start

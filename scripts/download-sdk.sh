#!/bin/bash
# download-sdk.sh - 下载火山 SDK

set -e

PRODUCT=$1

if [ -z "$PRODUCT" ]; then
    echo "Error: PRODUCT is required"
    echo "Usage: make download-sdk PRODUCT=<product>"
    echo ""
    echo "支持的 PRODUCT:"
    echo "  rtc    - veRTC SDK"
    echo "  ai     - AI 音视频互动 SDK"
    exit 1
fi

SDK_DIR="vendor"
mkdir -p "$SDK_DIR"

echo "=========================================="
echo "  下载火山 SDK: $PRODUCT"
echo "=========================================="
echo ""

case $PRODUCT in
    rtc)
        echo "veRTC SDK 下载..."
        echo ""
        echo "请访问以下链接下载:"
        echo "  https://www.volcengine.com/docs/6348/75707"
        echo ""
        echo "下载后解压到 vendor/veRTC_SDK/"
        echo ""
        echo "或使用命令行下载 (如果提供下载链接):"
        echo "  mkdir -p vendor/veRTC_SDK"
        echo "  # 请手动下载 SDK"
        ;;
    ai)
        echo "AI 音视频互动 SDK 下载..."
        echo ""
        echo "请访问以下链接下载:"
        echo "  https://www.volcengine.com/docs/6348/2137638"
        echo ""
        echo "下载后解压到 vendor/ai_audio_SDK/"
        ;;
    *)
        echo "Error: 不支持的 PRODUCT: $PRODUCT"
        echo "支持的: rtc, ai"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "  请手动下载并解压 SDK"
echo "=========================================="

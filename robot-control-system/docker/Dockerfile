# Robot Control System Dockerfile
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libgl1-mesa-glx \
    libpulse-dev \
    libva2 \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY python/ ./python/
COPY config/ ./config/
COPY web/ ./web/

# 创建必要的目录
RUN mkdir -p /tmp/vector_db /tmp/robot_control /tmp/conversations

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/python

# 暴露端口
EXPOSE 5000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# 启动命令
CMD ["python", "-m", "api.main"]

# 或者使用gunicorn（生产环境推荐）
# CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:5000", "api.main:app"]

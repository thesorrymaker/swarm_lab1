# 使用Python 3.9轻量版作为基础镜像
FROM python:3.9-slim

# 设置工作目录为/app
WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY app.py .
COPY templates/ ./templates/

# 暴露5000端口（Flask默认端口）
EXPOSE 5000

# 设置环境变量默认值
ENV PORT=5000
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

# 启动命令
CMD ["python", "app.py"]
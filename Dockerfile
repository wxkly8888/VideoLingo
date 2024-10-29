# 使用 Python 官方镜像
FROM python:3.11-slim

# 将当前目录内容复制到容器中
WORKDIR /app
COPY . .
# 安装系统依赖项（特别是 OpenCV 需要的库）
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0
# 安装必要的依赖项
RUN pip install -r requirements.txt

# 运行 install.py 脚本
RUN python installServer.py

# 运行 Cloud Run 服务的入口
CMD ["python", "app.py"]
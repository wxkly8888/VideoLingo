# 使用 Python 官方镜像
FROM python:3.11-slim

# 将当前目录内容复制到容器中
WORKDIR /app
COPY . .

# 安装必要的依赖项
RUN pip install -r requirements.txt

# 运行 install.py 脚本
RUN python install.py

# 运行 Cloud Run 服务的入口
CMD ["python", "app.py"]
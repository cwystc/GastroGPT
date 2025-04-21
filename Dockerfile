# FROM python:3.9-slim

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     git \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# WORKDIR /app
# COPY . /app

# RUN pip install --no-cache-dir --upgrade pip \
#  && pip install --no-cache-dir -r requirements.txt

# #  Set env so nltk knows where to find resources
# ENV NLTK_DATA=/root/nltk_data

# # Download nltk resources to that path
# RUN python -m nltk.downloader -d /root/nltk_data punkt stopwords wordnet

# CMD ["python", "main.py"]
#  基础镜像
FROM python:3.9-slim

# 安装系统依赖：构建 Python 和 Node.js 都需要
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    wget \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 安装 Node.js LTS 版本（从 Node 官方源）
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && node -v && npm -v

# 设定工作目录
WORKDIR /app

# 拷贝项目文件
COPY . /app

# 安装 Python 依赖
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 设置 NLTK 数据目录
ENV NLTK_DATA=/root/nltk_data

# 下载 NLTK 所需资源
RUN python -m nltk.downloader -d /root/nltk_data punkt stopwords wordnet

# 默认命令：跑后端（可进入容器手动切换跑前端）
CMD ["python", "main.py"]

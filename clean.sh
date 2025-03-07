#!/bin/bash

echo "开始清理项目资源..."

# 停止并删除所有容器和网络
echo "停止并删除Docker容器和网络..."
docker-compose -f docker-compose.dev.yml down

# 删除所有相关的Docker卷
echo "删除Docker卷..."
docker volume rm jmr_mongo-data jmr_comic-data 2>/dev/null || true

# 删除下载的图片文件
echo "删除下载的文件..."
rm -rf downloads/*

# 删除MongoDB数据文件（如果有）
echo "删除MongoDB数据文件..."
rm -rf backend/data/db/* 2>/dev/null || true

# 删除Python缓存文件
echo "删除Python缓存文件..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type f -name "*.pyd" -delete

# 删除构建的Docker镜像
echo "删除Docker镜像..."
docker rmi jmr_backend mongo:6 mongo-express 2>/dev/null || true

echo "清理完成！" 
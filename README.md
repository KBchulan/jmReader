# 漫画阅读网站

一个简单的漫画阅读网站，使用FastAPI和Vue.js构建。

## 项目简介

本项目是一个漫画阅读网站，包含以下功能：

- 漫画列表展示
- 漫画详情页
- 漫画阅读器
- 漫画搜索

## 技术栈

### 后端

- FastAPI: 高性能的Python Web框架
- jmcomic: 漫画下载库

### 前端

- Vue 3: 渐进式JavaScript框架
- Vite: 下一代前端构建工具
- TypeScript: JavaScript的超集
- Tailwind CSS: 实用优先的CSS框架

## 项目结构

```
.
├── backend/             # 后端代码
│   ├── app/             # 应用代码
│   │   ├── config/      # 配置
│   │   ├── middleware/  # 中间件
│   │   ├── models/      # 数据模型
│   │   ├── routes/      # 路由
│   │   └── services/    # 服务
│   ├── mock_data/       # 漫画数据存储目录
│   └── download_comics.py # 漫画下载脚本
└── src/                 # 前端代码
    ├── api/             # API调用
    ├── assets/          # 静态资源
    ├── components/      # 组件
    ├── router/          # 路由
    ├── stores/          # 状态管理
    ├── types/           # 类型定义
    ├── utils/           # 工具函数
    └── views/           # 页面
```

## 快速开始

### 下载漫画

在开始之前，需要先下载一些漫画：

```bash
cd backend
python download_comics.py 416330 # 可以添加多个漫画ID
```

### 启动后端

```bash
cd backend
# 创建虚拟环境
conda create -n jmr python=3.11
conda activate jmr
# 安装依赖
pip install -r requirements.txt
# 启动服务
uvicorn app.main:app --host 0.0.0.0 --port 3000 --reload
```

### 启动前端

```bash
# 安装依赖
npm install
# 启动开发服务器
npm run dev
```

## 访问服务

- 前端: http://localhost:5173
- 后端API: http://localhost:3000/api
- API文档: http://localhost:3000/docs

## 使用说明

1. 首先使用 `download_comics.py`脚本下载漫画
2. 启动后端和前端服务
3. 访问前端页面浏览漫画

## 注意事项

- 本项目仅供学习和研究使用
- 请勿用于任何商业用途
- 请遵守相关法律法规

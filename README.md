# JMR - 漫画阅读网站

一个简洁高效的漫画阅读网站，使用FastAPI和Vue.js构建。

## 项目简介

本项目是一个专注于漫画阅读体验的网站，包含以下功能：

- 漫画下载与管理
- 漫画列表展示
- 漫画详情页
- 漫画阅读器
- 漫画搜索

## 技术栈

### 后端

- FastAPI: 高性能的Python Web框架
- jmcomic: 漫画下载库
- 后台任务处理: 异步下载漫画

### 前端

- Vue 3: 渐进式JavaScript框架
- Element Plus: 基于Vue 3的组件库
- Vite: 下一代前端构建工具
- TypeScript: JavaScript的超集
- SCSS: CSS预处理器

## 项目结构

```
.
├── backend/                 # 后端代码
│   ├── app/                 # 应用代码
│   │   ├── main.py          # 主应用入口
│   │   └── download_and_process.py # 漫画下载处理脚本
└── src/                     # 前端代码
    ├── api/                 # API调用
    ├── assets/              # 静态资源
    │   └── mock/            # 漫画数据存储目录
    ├── components/          # 组件
    ├── router/              # 路由
    ├── stores/              # 状态管理
    ├── types/               # 类型定义
    ├── utils/               # 工具函数
    └── views/               # 页面
```

## 特色功能

- **简化的后端**: 专注于漫画下载功能，减少不必要的复杂性
- **前端优先**: 将更多精力放在前端优化上，提升用户体验
- **一键下载**: 只需输入漫画ID，即可自动下载并展示漫画
- **响应式设计**: 适配各种屏幕尺寸，提供最佳阅读体验

## 快速开始

### 启动后端

```bash
cd backend
# 创建虚拟环境
conda create -n jmr python=3.11
conda activate jmr
# 安装依赖
pip install -r requirements.txt
pip install jmcomic
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
- 后端API: http://localhost:3000

## 使用说明

1. 访问前端页面，在首页顶部的"下载漫画"区域输入6位漫画ID
2. 点击"下载"按钮，后端会自动下载并处理漫画
3. 下载完成后，页面会自动刷新并显示新下载的漫画
4. 点击漫画卡片进入详情页，可以查看章节列表
5. 点击章节进入阅读页面，享受流畅的阅读体验

## 漫画ID获取方法

您可以通过以下方式获取漫画ID：

1. 访问漫画源网站，查看漫画页面URL中的数字部分
2. 使用搜索引擎搜索特定漫画名称加上网站名称

## 注意事项

- 本项目仅供学习和研究使用
- 请勿用于任何商业用途
- 请遵守相关法律法规
- 下载的漫画版权归原作者所有

## 未来计划

- [ ] 添加下载进度显示
- [ ] 添加漫画搜索功能
- [ ] 优化漫画阅读体验
- [ ] 添加用户收藏功能
- [ ] 支持更多漫画源

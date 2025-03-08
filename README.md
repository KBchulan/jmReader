# 漫画阅读网站

一个现代化的漫画阅读网站，提供丰富的漫画内容、分类浏览、排行榜、搜索等功能。

## 功能特点

- **首页展示**：轮播图展示热门漫画，推荐漫画、最新更新和全部漫画列表
- **分类浏览**：按标签分类浏览漫画
- **排行榜**：热门排行、评分排行、收藏排行和更新排行
- **最新更新**：按时间筛选最新更新的漫画
- **搜索功能**：支持按名称、ID和标签搜索漫画
- **漫画阅读**：流畅的漫画阅读体验
- **漫画下载**：支持通过ID下载漫画
- **响应式设计**：适配各种设备屏幕尺寸

## 技术栈

- **前端框架**：Vue 3 + TypeScript
- **构建工具**：Vite
- **UI组件库**：Element Plus
- **状态管理**：Pinia
- **路由管理**：Vue Router
- **HTTP客户端**：Axios
- **样式预处理器**：SCSS
- **后端**：Python

## 安装和使用

### 前提条件

- Node.js (v14.0.0+)
- npm 或 yarn

### 安装步骤

1. 克隆仓库

```bash
git clone https://github.com/KBchulan/JMR.git
cd JMR
```

2. 安装依赖

```bash
npm install
# 或
yarn install
```

3. 启动开发服务器

```bash
npm run dev
# 或
yarn dev
```

4. 构建生产版本

```bash
npm run build
# 或
yarn build
```

## 项目结构

```
src/
├── api/            # API请求
├── assets/         # 静态资源
├── components/     # 公共组件
├── composables/    # 组合式函数
├── layouts/        # 布局组件
├── router/         # 路由配置
├── stores/         # Pinia状态管理
├── types/          # TypeScript类型定义
└── views/          # 页面视图
    ├── category/   # 分类页面
    ├── comic/      # 漫画详情页面
    ├── home/       # 首页
    ├── latest/     # 最新更新页面
    ├── ranking/    # 排行榜页面
    ├── reader/     # 阅读器页面
    └── search/     # 搜索页面
```

## 配置

项目使用环境变量进行配置，可以在 `.env` 文件中设置：

```
VITE_APP_TITLE=漫画阅读
VITE_API_BASE_URL=http://localhost:3000
VITE_COMICS_PER_PAGE=24
```

## 贡献

欢迎贡献代码、报告问题或提出改进建议。请遵循以下步骤：

1. Fork 仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件

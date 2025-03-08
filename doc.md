# 漫画阅读网站项目文档

本文档详细描述了项目中各个文件和目录的作用，帮助开发者快速了解项目结构和功能实现。

## 目录结构

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

## 核心文件说明

### 入口文件

- **src/main.ts**: 应用程序入口文件，负责初始化Vue应用、注册全局组件和插件。
- **src/App.vue**: 应用程序根组件，包含全局布局和路由视图。
- **index.html**: HTML入口文件，包含应用挂载点和全局样式。

### API请求

- **src/api/comic.ts**: 漫画相关的API请求函数，包括获取漫画列表、详情、章节等。
- **src/api/index.ts**: API模块的统一导出文件。

### 组件

#### 布局组件

- **src/layouts/DefaultLayout.vue**: 默认布局组件，包含页头、页脚和主内容区域。
- **src/layouts/AppHeader.vue**: 应用头部组件，包含导航菜单、搜索框和用户操作。
- **src/layouts/AppFooter.vue**: 应用底部组件，包含版权信息和链接。

#### 公共组件

- **src/components/ComicCard.vue**: 漫画卡片组件，用于展示漫画的基本信息。
- **src/components/ComicGrid.vue**: 漫画网格组件，用于以网格形式展示漫画列表。
- **src/components/SectionTitle.vue**: 分区标题组件，用于各个页面的分区标题。
- **src/components/BackToTop.vue**: 返回顶部组件，提供快速返回页面顶部的功能。
- **src/components/NetworkStatus.vue**: 网络状态组件，显示网络连接状态。

### 页面视图

#### 首页

- **src/views/home/HomeView.vue**: 首页组件，包含轮播图、推荐漫画、最新更新和全部漫画。

#### 分类页面

- **src/views/category/CategoryView.vue**: 分类页面，按标签分类展示漫画。

#### 排行榜页面

- **src/views/ranking/RankingView.vue**: 排行榜页面，展示不同类型的漫画排行。

#### 最新更新页面

- **src/views/latest/LatestView.vue**: 最新更新页面，展示最新更新的漫画。

#### 搜索页面

- **src/views/search/SearchView.vue**: 搜索页面，提供漫画搜索功能。

#### 漫画详情页面

- **src/views/comic/ComicDetail.vue**: 漫画详情页面，展示漫画的详细信息和章节列表。

#### 阅读器页面

- **src/views/reader/ReaderView.vue**: 漫画阅读器页面，提供漫画阅读功能。

### 状态管理

- **src/stores/comic.ts**: 漫画相关的状态管理，包括漫画列表、详情、章节等数据。
- **src/stores/index.ts**: Pinia状态管理的统一导出文件。

### 路由配置

- **src/router/index.ts**: 路由配置文件，定义应用的路由规则。

### 类型定义

- **src/types/index.ts**: TypeScript类型定义文件，定义漫画、章节等数据结构。

### 组合式函数

- **src/composables/useTheme.ts**: 主题相关的组合式函数，提供主题切换功能。
- **src/composables/useWindowSize.ts**: 窗口大小相关的组合式函数，提供响应式窗口尺寸。

## 功能模块详解

### 1. 漫画展示模块

#### 轮播图组件

轮播图组件位于首页，用于展示热门漫画。主要功能包括：

- 自动轮播
- 手动切换
- 点击跳转到漫画详情页

实现文件：`src/views/home/HomeView.vue`

关键代码：

```vue
<div class="banner-section">
  <div class="carousel-3d-container">
    <!-- 轮播图内容 -->
  </div>
</div>
```

#### 漫画卡片组件

漫画卡片组件用于展示单个漫画的基本信息，包括封面、标题、标签等。

实现文件：`src/components/ComicCard.vue`

关键功能：

- 展示漫画封面
- 展示漫画标题和标签
- 点击跳转到漫画详情页
- 悬停效果

### 2. 分类浏览模块

分类页面允许用户按标签浏览漫画，主要功能包括：

- 标签选择
- 按标签筛选漫画
- 分页展示

实现文件：`src/views/category/CategoryView.vue`

关键代码：

```vue
<div class="category-tags">
  <el-tag 
    v-for="tag in categoryTags" 
    :key="tag.id" 
    :class="{ active: activeTag === tag.id }"
    @click="setActiveTag(tag.id)"
  >
    {{ tag.name }}
  </el-tag>
</div>
```

### 3. 排行榜模块

排行榜页面展示不同类型的漫画排行，包括热门排行、评分排行、收藏排行和更新排行。

实现文件：`src/views/ranking/RankingView.vue`

关键功能：

- 切换不同排行类型
- 展示排名信息
- 点击跳转到漫画详情页

### 4. 最新更新模块

最新更新页面展示最新更新的漫画，并支持按时间范围筛选。

实现文件：`src/views/latest/LatestView.vue`

关键功能：

- 时间范围筛选（全部、今天、本周、本月）
- 分页展示
- 按更新时间排序

### 5. 搜索模块

搜索页面提供漫画搜索功能，支持按名称、ID和标签搜索。

实现文件：`src/views/search/SearchView.vue`

关键功能：

- 关键词搜索
- 标签筛选
- 排序方式选择
- 分页展示搜索结果

### 6. 漫画详情模块

漫画详情页展示漫画的详细信息和章节列表。

实现文件：`src/views/comic/ComicDetail.vue`

关键功能：

- 展示漫画基本信息（标题、作者、标签等）
- 展示漫画简介
- 展示章节列表
- 点击章节跳转到阅读页面

### 7. 阅读器模块

阅读器页面提供漫画阅读功能。

实现文件：`src/views/reader/ReaderView.vue`

关键功能：

- 漫画页面展示
- 翻页功能
- 缩放功能
- 章节切换
- 阅读进度保存

### 8. 下载模块

下载功能允许用户通过ID下载漫画。

实现文件：`src/layouts/AppHeader.vue`（下载对话框部分）

关键功能：

- 输入漫画ID
- 发送下载请求
- 显示下载状态和结果

## 状态管理详解

### 漫画状态管理

漫画状态管理使用Pinia实现，主要管理以下状态：

- 漫画列表
- 推荐漫画
- 最新更新漫画
- 当前漫画详情
- 当前章节
- 当前页面
- 加载状态
- 错误信息

实现文件：`src/stores/comic.ts`

主要方法：

- `fetchComics`: 获取漫画列表
- `fetchLatestComics`: 获取最新漫画
- `fetchRecommendedComics`: 获取推荐漫画
- `fetchComicDetail`: 获取漫画详情
- `fetchChapterPages`: 获取章节页面
- `searchComics`: 搜索漫画
- `fetchComicsByTag`: 按标签获取漫画

## API接口详解

### 漫画API

漫画API提供与漫画相关的数据接口。

实现文件：`src/api/comic.ts`

主要接口：

- `getComics`: 获取漫画列表
- `getComicDetail`: 获取漫画详情
- `getChapterPages`: 获取章节页面
- `getLatestComics`: 获取最新漫画
- `getRecommendedComics`: 获取推荐漫画
- `searchComics`: 搜索漫画

## 路由配置详解

路由配置定义了应用的页面路由规则。

实现文件：`src/router/index.ts`

主要路由：

- `/`: 首页
- `/category`: 分类页面
- `/ranking`: 排行榜页面
- `/latest`: 最新更新页面
- `/search`: 搜索页面
- `/comic/:id`: 漫画详情页面
- `/reader/:id`: 阅读器页面

## 样式设计

项目使用SCSS作为CSS预处理器，主要样式特点：

- 响应式设计，适配不同屏幕尺寸
- 深色主题，提供舒适的阅读体验
- 动画效果，提升用户体验
- 组件化样式，便于维护和复用

## 性能优化

项目采用了以下性能优化措施：

- 路由懒加载，减少首屏加载时间
- 组件按需导入，减少不必要的资源加载
- 图片懒加载，提高页面加载速度
- 状态缓存，减少重复请求
- 分页加载，减少一次性加载的数据量

## 扩展与维护

### 添加新功能

1. 在相应目录创建新组件或页面
2. 在路由配置中添加新路由（如需要）
3. 在状态管理中添加新状态和方法（如需要）
4. 在API中添加新接口（如需要）

### 修改现有功能

1. 找到相应的组件或页面文件
2. 修改组件逻辑或样式
3. 测试修改效果
4. 更新文档（如需要）

## 常见问题与解决方案

### 1. 图片加载失败

可能原因：

- 网络问题
- 图片路径错误
- 图片资源不存在

解决方案：

- 添加图片加载失败处理
- 使用默认图片替代
- 添加重试机制

### 2. 数据加载缓慢

可能原因：

- 网络延迟
- 数据量过大
- 服务器响应慢

解决方案：

- 添加加载状态提示
- 实现分页加载
- 优化数据请求逻辑
- 添加数据缓存

### 3. 移动端适配问题

可能原因：

- 样式未适配移动端
- 交互方式不适合移动端

解决方案：

- 使用响应式设计
- 针对移动端优化交互方式
- 使用媒体查询适配不同屏幕尺寸

// 漫画类型定义
export interface Comic {
  id: string | number;
  title: string;
  cover: string;
  author: string;
  description: string;
  tags: string[];
  updateTime: string;
  status: 'ongoing' | 'completed';
  chapters?: Chapter[];
}

// 章节类型定义
export interface Chapter {
  id: string | number;
  comicId: string | number;
  title: string;
  order: number;
  updateTime: string;
  pageCount: number;
}

// 页面类型定义
export interface Page {
  id: string | number;
  chapterId: string | number;
  url: string;
  order: number;
}

// 搜索参数类型定义
export interface SearchParams {
  keyword: string;
  page?: number;
  pageSize?: number;
  sort?: 'newest' | 'popular';
  tags?: string[];
}

// 分页结果类型定义
export interface PaginatedResult<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}

// 主题模式类型定义
export type ThemeMode = 'light' | 'dark' | 'auto';

// API响应类型定义
export interface ApiResponse<T = any> {
  code: number;
  data: T;
  message: string;
  success: boolean;
} 
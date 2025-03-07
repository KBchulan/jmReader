import { get } from '@/utils/request'
import type { Comic, Chapter, Page, PaginatedResult, SearchParams } from '@/types'
import * as mockApi from './mock'

// 判断是否启用mock
const enableMock = import.meta.env.VITE_ENABLE_MOCK === 'true'

// 获取漫画列表
export async function getComics(page = 1, pageSize = 20): Promise<PaginatedResult<Comic>> {
  if (enableMock) {
    return mockApi.getComics(page, pageSize)
  }
  return get<PaginatedResult<Comic>>('/comics', { page, pageSize })
}

// 获取漫画详情
export async function getComicDetail(id: number | string): Promise<Comic | null> {
  if (enableMock) {
    return mockApi.getComicDetail(id)
  }
  return get<Comic>(`/comics/${id}`)
}

// 获取章节页面
export async function getChapterPages(chapterId: number | string): Promise<Page[]> {
  if (enableMock) {
    return mockApi.getChapterPages(chapterId)
  }
  return get<Page[]>(`/chapters/${chapterId}/pages`)
}

// 搜索漫画
export async function searchComics(params: SearchParams): Promise<PaginatedResult<Comic>> {
  if (enableMock) {
    return mockApi.searchComics(params)
  }
  return get<PaginatedResult<Comic>>('/comics/search', params)
}

// 获取最新更新的漫画
export async function getLatestComics(limit = 10): Promise<Comic[]> {
  if (enableMock) {
    const result = mockApi.getComics(1, limit)
    // 按更新时间排序
    return result.items.sort((a, b) => 
      new Date(b.updateTime).getTime() - new Date(a.updateTime).getTime()
    )
  }
  return get<Comic[]>('/comics/latest', { limit })
}

// 获取推荐漫画
export async function getRecommendedComics(limit = 6): Promise<Comic[]> {
  if (enableMock) {
    const allComics = mockApi.getAllComics()
    // 随机选择几个作为推荐
    const shuffled = [...allComics].sort(() => 0.5 - Math.random())
    return shuffled.slice(0, limit)
  }
  return get<Comic[]>('/comics/recommended', { limit })
} 
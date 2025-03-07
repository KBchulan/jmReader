import { get } from '@/utils/request'
import type { Comic, Chapter, Page, PaginatedResult, SearchParams } from '@/types'
import * as mockApi from './mock'

// 判断是否启用mock
const enableMock = import.meta.env.VITE_ENABLE_MOCK === 'true'

// 获取漫画列表
export async function getComics(page = 1, pageSize = 20): Promise<PaginatedResult<Comic>> {
  try {
    if (!enableMock) {
      const result = await get<PaginatedResult<Comic>>('/comics', { page, pageSize })
      if (result && result.items.length > 0) {
        return result
      }
    }
    // 如果启用了mock或者没有真实数据，使用mock数据
    return mockApi.getComics(page, pageSize)
  } catch (error) {
    console.warn('获取漫画列表失败, 使用mock数据', error)
    return mockApi.getComics(page, pageSize)
  }
}

// 获取漫画详情
export async function getComicDetail(id: number | string): Promise<Comic | null> {
  try {
    if (!enableMock) {
      const result = await get<Comic>(`/comics/${id}`)
      if (result) {
        return result
      }
    }
    return mockApi.getComicDetail(id)
  } catch (error) {
    console.warn('获取漫画详情失败, 使用mock数据', error)
    return mockApi.getComicDetail(id)
  }
}

// 获取章节页面
export async function getChapterPages(chapterId: number | string): Promise<Page[]> {
  try {
    if (!enableMock) {
      const result = await get<Page[]>(`/chapters/${chapterId}/pages`)
      if (result && result.length > 0) {
        return result
      }
    }
    return mockApi.getChapterPages(chapterId)
  } catch (error) {
    console.warn('获取章节页面失败, 使用mock数据', error)
    return mockApi.getChapterPages(chapterId)
  }
}

// 搜索漫画
export async function searchComics(params: SearchParams): Promise<PaginatedResult<Comic>> {
  try {
    if (!enableMock) {
      const result = await get<PaginatedResult<Comic>>('/comics/search', params)
      if (result && result.items.length > 0) {
        return result
      }
    }
    return mockApi.searchComics(params)
  } catch (error) {
    console.warn('搜索漫画失败，使用mock数据', error)
    return mockApi.searchComics(params)
  }
}

// 获取最新更新的漫画
export async function getLatestComics(limit = 10): Promise<Comic[]> {
  try {
    if (!enableMock) {
      const result = await get<Comic[]>('/comics/latest', { limit })
      if (result && result.length > 0) {
        return result
      }
    }
    const mockResult = mockApi.getComics(1, limit)
    return mockResult.items.sort((a, b) =>
      new Date(b.updateTime).getTime() - new Date(a.updateTime).getTime()
    )
  } catch (error) {
    console.warn('获取最新漫画失败, 使用mock数据', error)
    const mockResult = mockApi.getComics(1, limit)
    return mockResult.items.sort((a, b) =>
      new Date(b.updateTime).getTime() - new Date(a.updateTime).getTime()
    )
  }
}

// 获取推荐漫画
export async function getRecommendedComics(limit = 6): Promise<Comic[]> {
  try {
    if (!enableMock) {
      const result = await get<Comic[]>('/comics/recommended', { limit })
      if (result && result.length > 0) {
        return result
      }
    }
    const allComics = mockApi.getAllComics()
    const shuffled = [...allComics].sort(() => 0.5 - Math.random())
    return shuffled.slice(0, limit)
  } catch (error) {
    console.warn('获取推荐漫画失败, 使用mock数据', error)
    const allComics = mockApi.getAllComics()
    const shuffled = [...allComics].sort(() => 0.5 - Math.random())
    return shuffled.slice(0, limit)
  }
} 
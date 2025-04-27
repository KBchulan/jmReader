import { get } from '@/utils/request'
import type { Comic, Page, PaginatedResult, SearchParams } from '@/types'

// 获取漫画列表
export async function getComics(page = 1, pageSize = 20): Promise<PaginatedResult<Comic>> {
  try {
    const result = await get<PaginatedResult<Comic>>('/comics', { page, pageSize })
    return result
  } catch (error) {
    console.error('获取漫画列表失败', error)
    return {
      items: [],
      total: 0,
      page,
      pageSize,
      hasMore: false
    }
  }
}

// 获取漫画详情
export async function getComicDetail(id: number | string): Promise<Comic | null> {
  try {
    const result = await get<Comic>(`/comics/${id}`)
    return result
  } catch (error) {
    console.error('获取漫画详情失败', error)
    return null
  }
}

// 获取章节页面
export async function getChapterPages(chapterId: number | string): Promise<Page[]> {
  try {
    const result = await get<Page[]>(`/chapters/${chapterId}/pages`)
    return result
  } catch (error) {
    console.error('获取章节页面失败', error)
    return []
  }
}

// 搜索漫画
export async function searchComics(params: SearchParams): Promise<PaginatedResult<Comic>> {
  try {
    const result = await get<PaginatedResult<Comic>>('/comics/search', params)
    return result
  } catch (error) {
    console.error('搜索漫画失败', error)
    return {
      items: [],
      total: 0,
      page: params.page || 1,
      pageSize: params.pageSize || 20,
      hasMore: false
    }
  }
}

// 获取最新更新的漫画
export async function getLatestComics(limit = 10): Promise<Comic[]> {
  try {
    const result = await get<Comic[]>('/comics/latest', { limit })
    return result
  } catch (error) {
    console.error('获取最新漫画失败', error)
    return []
  }
}

// 获取推荐漫画
export async function getRecommendedComics(limit = 6): Promise<Comic[]> {
  try {
    const result = await get<Comic[]>('/comics/recommended', { limit })
    return result
  } catch (error) {
    console.error('获取推荐漫画失败', error)
    return []
  }
}
import type { Comic, Chapter, Page, PaginatedResult, SearchParams } from '@/types'
import { ref } from 'vue'

// 小魔仙图片路径数组 - 修改为使用相对路径
const mockImagePaths = Array.from({ length: 16 }, (_, i) => {
  const index = i + 1
  const paddedNum = index.toString().padStart(5, '0')
  // 使用相对路径，确保Vite可以正确处理
  return `/src/assets/mock/小魔仙/${paddedNum}.png`
})

// 尝试加载comics.json文件
let comicsFromJson: Comic[] = []
try {
  // 使用动态导入加载JSON文件
  const comicsJsonModule = import.meta.glob('/src/assets/mock/comics.json', { eager: true })
  const comicsJsonPath = Object.keys(comicsJsonModule)[0]
  if (comicsJsonPath) {
    const jsonData = (comicsJsonModule[comicsJsonPath] as any).default || []
    // 确保status字段的值是'completed'或'ongoing'
    comicsFromJson = jsonData.map((comic: any) => ({
      ...comic,
      status: comic.status === 'completed' ? 'completed' : 'ongoing'
    })) as Comic[]
  }
} catch (error) {
  console.warn('无法加载comics.json文件', error)
}

// 尝试加载chapters.json文件
let chaptersFromJson: Chapter[] = []
try {
  // 使用动态导入加载JSON文件
  const chaptersJsonModule = import.meta.glob('/src/assets/mock/chapters.json', { eager: true })
  const chaptersJsonPath = Object.keys(chaptersJsonModule)[0]
  if (chaptersJsonPath) {
    chaptersFromJson = (chaptersJsonModule[chaptersJsonPath] as any).default || []
  }
} catch (error) {
  console.warn('无法加载chapters.json文件', error)
}

// 生成小魔仙漫画数据
function generateMockComics(): Comic[] {
  const defaultComics: Comic[] = [
    {
      id: "1",
      title: '小魔仙',
      cover: mockImagePaths[0],
      author: '小魔仙作者',
      description: '百合小漫画',
      tags: ['百合',],
      updateTime: new Date().toISOString().split('T')[0],
      status: 'completed'
    }
  ]
  
  // 合并默认漫画和从JSON加载的漫画
  return [...defaultComics, ...comicsFromJson]
}

// 生成小魔仙章节数据
function generateMockChapters(comicId: number | string): Chapter[] {
  // 如果是小魔仙，返回默认章节
  if (comicId.toString() === '1') {
    return [
      {
        id: `${comicId}-1`,
        comicId,
        title: '第1话:神秘的开始',
        order: 1,
        updateTime: new Date().toISOString().split('T')[0],
        pageCount: mockImagePaths.length,
        cover: mockImagePaths[0]
      }
    ]
  }
  
  // 否则从JSON加载的章节中查找
  const chapters = chaptersFromJson.filter(chapter => 
    chapter.comicId.toString() === comicId.toString()
  )
  
  return chapters.length > 0 ? chapters : []
}

// 生成章节页面数据
export function getChapterPages(chapterId: number | string): Page[] {
  // 如果是小魔仙的章节，返回默认页面
  if (chapterId.toString() === '1-1') {
    return mockImagePaths.map((path, index) => ({
      id: `${chapterId}-${index + 1}`,
      chapterId,
      order: index + 1,
      url: path
    }))
  }
  
  // 否则尝试查找对应的漫画和章节
  const [comicId, chapterOrder] = chapterId.toString().split('-')
  if (!comicId || !chapterOrder) return []
  
  // 查找漫画
  const comic = getComicDetail(comicId)
  if (!comic) return []
  
  // 查找章节
  const chapter = comic.chapters?.find(ch => ch.id === chapterId)
  if (!chapter) return []
  
  // 生成页面数据
  const pageCount = chapter.pageCount || 0
  const pages: Page[] = []
  
  for (let i = 1; i <= pageCount; i++) {
    const paddedNum = i.toString().padStart(5, '0')
    pages.push({
      id: `${chapterId}-${i}`,
      chapterId,
      order: i,
      url: `/src/assets/mock/${comicId}/${paddedNum}.webp`
    })
  }
  
  return pages
}

// 漫画数据缓存
let comicsCache: Comic[] | null = null

// 获取所有漫画数据
export function getAllComics(): Comic[] {
  if (!comicsCache) {
    comicsCache = generateMockComics()
  }
  return comicsCache
}

// 获取分页漫画数据
export function getComics(page = 1, pageSize = 20): PaginatedResult<Comic> {
  const allComics = getAllComics()
  const start = (page - 1) * pageSize
  const end = start + pageSize
  const items = allComics.slice(start, end)
  
  return {
    items,
    total: allComics.length,
    page,
    pageSize,
    hasMore: end < allComics.length
  }
}

// 获取漫画详情
export function getComicDetail(id: number | string): Comic | null {
  const comic = getAllComics().find(c => c.id.toString() === id.toString())
  
  if (comic && !comic.chapters) {
    // 生成章节数据
    comic.chapters = generateMockChapters(id)
  }
  
  return comic || null
}

// 搜索漫画
export function searchComics(params: SearchParams): PaginatedResult<Comic> {
  const { keyword, tags } = params
  let allComics = getAllComics()
  
  // 关键词过滤
  if (keyword) {
    allComics = allComics.filter(comic => 
      comic.title.toLowerCase().includes(keyword.toLowerCase()) ||
      comic.author.toLowerCase().includes(keyword.toLowerCase()) ||
      comic.description.toLowerCase().includes(keyword.toLowerCase())
    )
  }
  
  // 标签过滤
  if (tags && tags.length > 0) {
    allComics = allComics.filter(comic => 
      tags.every(tag => comic.tags.includes(tag))
    )
  }
  
  // 分页
  const page = params.page || 1
  const pageSize = params.pageSize || 20
  const start = (page - 1) * pageSize
  const end = start + pageSize
  const items = allComics.slice(start, end)
  
  return {
    items,
    total: allComics.length,
    page,
    pageSize,
    hasMore: end < allComics.length
  }
} 
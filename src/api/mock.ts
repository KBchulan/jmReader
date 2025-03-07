import type { Comic, Chapter, Page, PaginatedResult, SearchParams } from '@/types'

// 生成随机漫画数据
function generateMockComics(count = 50): Comic[] {
  const comics: Comic[] = []
  const statuses: ('ongoing' | 'completed')[] = ['ongoing', 'completed']
  const tags = ['热血', '冒险', '搞笑', '恋爱', '科幻', '奇幻', '魔法', '校园', '悬疑', '推理', '恐怖', '战斗']

  for (let i = 1; i <= count; i++) {
    const randomTagCount = Math.floor(Math.random() * 4) + 1
    const selectedTags: string[] = []
    
    // 随机选择标签
    for (let j = 0; j < randomTagCount; j++) {
      const randomTag = tags[Math.floor(Math.random() * tags.length)]
      if (!selectedTags.includes(randomTag)) {
        selectedTags.push(randomTag)
      }
    }

    // 随机生成更新日期（过去3个月内）
    const now = new Date()
    const threeMonthsAgo = new Date(now.getTime() - 90 * 24 * 60 * 60 * 1000)
    const randomDate = new Date(
      threeMonthsAgo.getTime() + Math.random() * (now.getTime() - threeMonthsAgo.getTime())
    )
    const updateTime = randomDate.toISOString().split('T')[0]

    // 生成漫画数据
    comics.push({
      id: i,
      title: `测试漫画 ${i}`,
      cover: `https://picsum.photos/id/${(i % 30) + 100}/300/400`,
      author: `作者 ${Math.floor(i / 5) + 1}`,
      description: `这是测试漫画 ${i} 的描述。这部漫画讲述了一个精彩的故事，包含了${selectedTags.join('、')}等元素。`,
      tags: selectedTags,
      updateTime,
      status: statuses[Math.floor(Math.random() * statuses.length)]
    })
  }

  return comics
}

// 生成随机章节数据
function generateMockChapters(comicId: number | string, count = 20): Chapter[] {
  const chapters: Chapter[] = []
  
  for (let i = 1; i <= count; i++) {
    // 生成更新日期（模拟章节发布时间，越新的章节日期越近）
    const daysPast = (count - i) * 7 // 每周更新一次
    const updateDate = new Date()
    updateDate.setDate(updateDate.getDate() - daysPast)
    const updateTime = updateDate.toISOString().split('T')[0]

    chapters.push({
      id: `${comicId}-${i}`,
      comicId,
      title: `第${i}话`,
      order: i,
      updateTime,
      pageCount: Math.floor(Math.random() * 20) + 10 // 10-30页
    })
  }

  return chapters
}

// 生成随机页面数据
function generateMockPages(chapterId: number | string, pageCount: number): Page[] {
  const pages: Page[] = []
  
  for (let i = 1; i <= pageCount; i++) {
    pages.push({
      id: `${chapterId}-${i}`,
      chapterId,
      url: `https://picsum.photos/id/${(Math.floor(Math.random() * 100) + 200)}/800/1200`,
      order: i
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

// 获取章节页面
export function getChapterPages(chapterId: number | string): Page[] {
  // 从chapterId解析出comicId和chapterOrder
  const [comicId, chapterOrder] = chapterId.toString().split('-').map(Number)
  
  // 获取漫画章节信息
  const comic = getComicDetail(comicId)
  if (!comic || !comic.chapters) return []
  
  const chapter = comic.chapters.find(c => c.order === chapterOrder)
  if (!chapter) return []
  
  return generateMockPages(chapterId, chapter.pageCount)
}

// 搜索漫画
export function searchComics(params: SearchParams): PaginatedResult<Comic> {
  const { keyword, page = 1, pageSize = 20, sort, tags } = params
  const allComics = getAllComics()
  
  // 过滤匹配的漫画
  let filtered = allComics
  
  // 关键词过滤
  if (keyword) {
    // 判断是否是纯数字
    const isNumeric = /^\d+$/.test(keyword)
    
    if (isNumeric) {
      // 匹配ID
      filtered = filtered.filter(comic => comic.id.toString() === keyword)
    } else {
      // 匹配标题或作者
      const lowerKeyword = keyword.toLowerCase()
      filtered = filtered.filter(comic => 
        comic.title.toLowerCase().includes(lowerKeyword) || 
        comic.author.toLowerCase().includes(lowerKeyword)
      )
    }
  }
  
  // 标签过滤
  if (tags && tags.length > 0) {
    filtered = filtered.filter(comic => 
      tags.some(tag => comic.tags.includes(tag))
    )
  }
  
  // 排序
  if (sort) {
    if (sort === 'newest') {
      filtered.sort((a, b) => new Date(b.updateTime).getTime() - new Date(a.updateTime).getTime())
    } else if (sort === 'popular') {
      // 这里用ID的倒序模拟人气排序
      filtered.sort((a, b) => Number(b.id) - Number(a.id))
    }
  }
  
  // 分页
  const start = (page - 1) * pageSize
  const end = start + pageSize
  const items = filtered.slice(start, end)
  
  return {
    items,
    total: filtered.length,
    page,
    pageSize,
    hasMore: end < filtered.length
  }
} 
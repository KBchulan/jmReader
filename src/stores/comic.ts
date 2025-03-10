import { defineStore } from 'pinia'
import { ref, computed, onMounted, onUnmounted } from 'vue'
import type { Comic, Chapter, Page } from '@/types'
import * as comicApi from '@/api/comic'
import { onMessage } from '@/utils/websocket'

export const useComicStore = defineStore('comic', () => {
  // 状态
  const comics = ref<Comic[]>([])
  const latestComics = ref<Comic[]>([])
  const recommendedComics = ref<Comic[]>([])
  const filteredComics = ref<Comic[]>([])
  const currentComic = ref<Comic | null>(null)
  const currentChapter = ref<Chapter | null>(null)
  const currentPages = ref<Page[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // 计算属性
  const hasComics = computed(() => comics.value.length > 0)
  const hasCurrentComic = computed(() => currentComic.value !== null)
  const hasCurrentChapter = computed(() => currentChapter.value !== null)
  const hasCurrentPages = computed(() => currentPages.value.length > 0)

  // 获取漫画列表
  async function fetchComics(page = 1, pageSize = 20) {
    try {
      loading.value = true
      error.value = null
      const result = await comicApi.getComics(page, pageSize)
      comics.value = result.items
      return result
    } catch (err: any) {
      error.value = err.message || '获取漫画列表失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 获取最新漫画
  async function fetchLatestComics(limit = 10) {
    try {
      loading.value = true
      error.value = null
      latestComics.value = await comicApi.getLatestComics(limit)
    } catch (err: any) {
      error.value = err.message || '获取最新漫画失败'
    } finally {
      loading.value = false
    }
  }

  // 获取推荐漫画
  async function fetchRecommendedComics(limit = 6) {
    try {
      loading.value = true
      error.value = null
      recommendedComics.value = await comicApi.getRecommendedComics(limit)
    } catch (err: any) {
      error.value = err.message || '获取推荐漫画失败'
    } finally {
      loading.value = false
    }
  }

  // 获取漫画详情
  async function fetchComicDetail(id: number | string) {
    try {
      loading.value = true
      error.value = null
      const comic = await comicApi.getComicDetail(id)
      if (comic) {
        currentComic.value = comic
      } else {
        error.value = '漫画不存在'
      }
    } catch (err: any) {
      error.value = err.message || '获取漫画详情失败'
    } finally {
      loading.value = false
    }
  }

  // 获取章节页面
  async function fetchChapterPages(chapterId: number | string) {
    try {
      loading.value = true
      error.value = null

      // 如果当前漫画存在，查找章节
      if (currentComic.value && currentComic.value.chapters) {
        const [comicId, chapterOrder] = chapterId.toString().split('-').map(Number)

        if (currentComic.value.id.toString() === comicId.toString()) {
          currentChapter.value = currentComic.value.chapters.find(
            c => c.order === chapterOrder
          ) || null
        }
      }

      currentPages.value = await comicApi.getChapterPages(chapterId)
    } catch (err: any) {
      error.value = err.message || '获取章节页面失败'
    } finally {
      loading.value = false
    }
  }

  // 搜索漫画
  async function searchComics(keyword: string, page = 1, pageSize = 20) {
    try {
      loading.value = true
      error.value = null
      return await comicApi.searchComics({ keyword, page, pageSize })
    } catch (err: any) {
      error.value = err.message || '搜索漫画失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 根据标签获取漫画
  async function fetchComicsByTag(tag: string, page = 1, pageSize = 20) {
    try {
      loading.value = true
      error.value = null

      // 先获取所有漫画
      await fetchComics(page, pageSize)

      // 然后根据标签筛选
      filteredComics.value = comics.value.filter(comic =>
        comic.tags && comic.tags.includes(tag)
      )

      return {
        items: filteredComics.value,
        total: filteredComics.value.length,
        page,
        pageSize,
        hasMore: false
      }
    } catch (err: any) {
      error.value = err.message || '获取分类漫画失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 重置状态
  function resetState() {
    comics.value = []
    latestComics.value = []
    recommendedComics.value = []
    filteredComics.value = []
    currentComic.value = null
    currentChapter.value = null
    currentPages.value = []
    error.value = null
  }

  // 处理WebSocket消息
  function handleComicAdded(data: any) {
    console.log('收到漫画添加通知:', data)
    // 刷新漫画列表
    fetchComics()
    fetchLatestComics()
    fetchRecommendedComics()
  }

  function handleComicDeleted(data: any) {
    console.log('收到漫画删除通知:', data)
    // 刷新漫画列表
    fetchComics()
    fetchLatestComics()
    fetchRecommendedComics()
    
    // 如果当前正在查看的漫画被删除，重置状态
    if (currentComic.value && currentComic.value.id.toString() === data.comic_id) {
      currentComic.value = null
      currentChapter.value = null
      currentPages.value = []
    }
  }

  // 注册WebSocket消息处理
  onMessage('comic_added', handleComicAdded)
  onMessage('comic_deleted', handleComicDeleted)

  return {
    // 状态
    comics,
    latestComics,
    recommendedComics,
    filteredComics,
    currentComic,
    currentChapter,
    currentPages,
    loading,
    error,

    // 计算属性
    hasComics,
    hasCurrentComic,
    hasCurrentChapter,
    hasCurrentPages,

    // 动作
    fetchComics,
    fetchLatestComics,
    fetchRecommendedComics,
    fetchComicDetail,
    fetchChapterPages,
    searchComics,
    fetchComicsByTag,
    resetState
  }
}) 
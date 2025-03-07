<template>
  <div class="reader-view" :class="{ 'fullscreen': isFullscreen }">
    <!-- 顶部控制栏 -->
    <div class="reader-header" v-show="showControls">
      <div class="container">
        <div class="header-content">
          <div class="left-controls">
            <el-button @click="goBack" icon="Back" plain>返回</el-button>
            <h2 class="chapter-title" v-if="currentChapter">{{ currentChapter.title }}</h2>
          </div>
          
          <div class="right-controls">
            <el-button-group>
              <el-button @click="toggleFullscreen" :icon="isFullscreen ? 'FullScreen' : 'FullScreen'" plain>
                {{ isFullscreen ? '退出全屏' : '全屏' }}
              </el-button>
              <el-button @click="toggleSettings" icon="Setting" plain>设置</el-button>
            </el-button-group>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 阅读设置抽屉 -->
    <el-drawer
      v-model="showSettings"
      title="阅读设置"
      direction="rtl"
      size="300px"
    >
      <div class="settings-content">
        <div class="setting-item">
          <span class="setting-label">阅读模式</span>
          <el-radio-group v-model="readingMode" size="small">
            <el-radio-button label="vertical">垂直滚动</el-radio-button>
            <el-radio-button label="horizontal">水平翻页</el-radio-button>
          </el-radio-group>
        </div>
        
        <div class="setting-item">
          <span class="setting-label">背景颜色</span>
          <el-radio-group v-model="backgroundColor" size="small">
            <el-radio-button label="white">白色</el-radio-button>
            <el-radio-button label="black">黑色</el-radio-button>
            <el-radio-button label="sepia">护眼</el-radio-button>
          </el-radio-group>
        </div>
        
        <div class="setting-item">
          <span class="setting-label">图片宽度</span>
          <el-slider v-model="imageWidth" :min="50" :max="100" :step="5" :format-tooltip="formatTooltip" />
        </div>
      </div>
    </el-drawer>
    
    <!-- 加载中 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="5" animated />
    </div>
    
    <!-- 阅读内容 -->
    <div v-else-if="pages.length > 0" class="reader-content" :class="[readingMode, backgroundColor]">
      <div class="pages-container" :style="{ maxWidth: `${imageWidth}%` }">
        <!-- 垂直滚动模式 -->
        <template v-if="readingMode === 'vertical'">
          <div v-for="page in pages" :key="page.id" class="page-item">
            <img :src="page.url" :alt="`Page ${page.order}`" loading="lazy" />
          </div>
        </template>
        
        <!-- 水平翻页模式 -->
        <template v-else>
          <el-carousel
            ref="carousel"
            :autoplay="false"
            :initial-index="currentPageIndex"
            indicator-position="none"
            height="calc(100vh - 120px)"
            @change="handlePageChange"
          >
            <el-carousel-item v-for="page in pages" :key="page.id">
              <div class="page-item horizontal">
                <img :src="page.url" :alt="`Page ${page.order}`" />
              </div>
            </el-carousel-item>
          </el-carousel>
          
          <div class="page-navigation">
            <el-button @click="prevPage" :disabled="currentPageIndex === 0" icon="ArrowLeft" circle />
            <span class="page-indicator">{{ currentPageIndex + 1 }} / {{ pages.length }}</span>
            <el-button @click="nextPage" :disabled="currentPageIndex === pages.length - 1" icon="ArrowRight" circle />
          </div>
        </template>
      </div>
    </div>
    
    <!-- 错误提示 -->
    <div v-else class="error-container">
      <el-empty description="无法加载漫画内容" />
      <el-button type="primary" @click="goBack">返回</el-button>
    </div>
    
    <!-- 章节导航 -->
    <div class="chapter-navigation" v-if="currentChapter && comic">
      <div class="container">
        <div class="navigation-content">
          <el-button
            v-if="prevChapter"
            @click="navigateToChapter(prevChapter)"
            icon="ArrowLeft"
          >
            上一章: {{ prevChapter.title }}
          </el-button>
          <span v-else></span>
          
          <el-dropdown @command="handleChapterSelect">
            <el-button>
              章节列表
              <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item
                  v-for="chapter in comic.chapters"
                  :key="chapter.id"
                  :command="chapter.id"
                  :class="{ 'is-active': currentChapter.id === chapter.id }"
                >
                  {{ chapter.title }}
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          
          <el-button
            v-if="nextChapter"
            @click="navigateToChapter(nextChapter)"
            icon-position="right"
          >
            下一章: {{ nextChapter.title }}
            <el-icon class="el-icon--right"><arrow-right /></el-icon>
          </el-button>
          <span v-else></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useComicStore } from '@/stores/comic'
import { useFullscreen } from '@vueuse/core'
import { ArrowLeft, ArrowRight, ArrowDown, Back, FullScreen, Setting } from '@element-plus/icons-vue'
import type { Chapter } from '@/types'

const route = useRoute()
const router = useRouter()
const comicStore = useComicStore()

// 状态
const readingMode = ref<'vertical' | 'horizontal'>('vertical')
const backgroundColor = ref<'white' | 'black' | 'sepia'>('white')
const imageWidth = ref(80)
const showControls = ref(true)
const showSettings = ref(false)
const currentPageIndex = ref(0)
const controlsTimeout = ref<number | null>(null)
const carousel = ref<any>(null)

// 全屏控制
const { isFullscreen, toggle: toggleFullscreen } = useFullscreen()

// 计算属性
const loading = computed(() => comicStore.loading)
const pages = computed(() => comicStore.currentPages)
const currentChapter = computed(() => comicStore.currentChapter)
const comic = computed(() => comicStore.currentComic)

// 获取章节ID
const chapterId = computed(() => route.params.id)

// 上一章和下一章
const prevChapter = computed(() => {
  if (!comic.value || !comic.value.chapters || !currentChapter.value) return null
  
  const currentIndex = comic.value.chapters.findIndex(c => c.id === currentChapter.value?.id)
  if (currentIndex > 0) {
    return comic.value.chapters[currentIndex - 1]
  }
  return null
})

const nextChapter = computed(() => {
  if (!comic.value || !comic.value.chapters || !currentChapter.value) return null
  
  const currentIndex = comic.value.chapters.findIndex(c => c.id === currentChapter.value?.id)
  if (currentIndex < comic.value.chapters.length - 1) {
    return comic.value.chapters[currentIndex + 1]
  }
  return null
})

// 监听路由变化，重新加载数据
watch(() => route.params.id, (newId) => {
  if (newId) {
    const id = Array.isArray(newId) ? newId[0] : newId
    loadChapterPages(id)
    currentPageIndex.value = 0
  }
})

// 加载章节页面
async function loadChapterPages(id: string | number) {
  try {
    await comicStore.fetchChapterPages(id)
  } catch (err) {
    console.error('加载章节页面失败', err)
  }
}

// 返回上一页
function goBack() {
  if (comic.value) {
    router.push(`/comic/${comic.value.id}`)
  } else {
    router.push('/')
  }
}

// 切换设置抽屉
function toggleSettings() {
  showSettings.value = !showSettings.value
}

// 格式化提示
function formatTooltip(val: number) {
  return `${val}%`
}

// 上一页
function prevPage() {
  if (carousel.value) {
    carousel.value.prev()
  }
}

// 下一页
function nextPage() {
  if (carousel.value) {
    carousel.value.next()
  }
}

// 处理页面变化
function handlePageChange(index: number) {
  currentPageIndex.value = index
}

// 导航到章节
function navigateToChapter(chapter: Chapter) {
  router.push(`/reader/${chapter.id}`)
}

// 处理章节选择
function handleChapterSelect(chapterId: string | number) {
  router.push(`/reader/${chapterId}`)
}

// 自动隐藏控制栏
function resetControlsTimeout() {
  if (controlsTimeout.value) {
    clearTimeout(controlsTimeout.value)
  }
  
  showControls.value = true
  controlsTimeout.value = window.setTimeout(() => {
    if (!showSettings.value) {
      showControls.value = false
    }
  }, 3000)
}

// 监听鼠标移动
function handleMouseMove() {
  resetControlsTimeout()
}

// 初始化
onMounted(() => {
  if (chapterId.value) {
    const id = Array.isArray(chapterId.value) ? chapterId.value[0] : chapterId.value
    loadChapterPages(id)
  }
  
  // 添加鼠标移动监听
  document.addEventListener('mousemove', handleMouseMove)
  
  // 初始化控制栏超时
  resetControlsTimeout()
  
  // 从本地存储加载阅读设置
  const savedReadingMode = localStorage.getItem('comic-reading-mode')
  if (savedReadingMode === 'vertical' || savedReadingMode === 'horizontal') {
    readingMode.value = savedReadingMode
  }
  
  const savedBackgroundColor = localStorage.getItem('comic-background-color')
  if (savedBackgroundColor === 'white' || savedBackgroundColor === 'black' || savedBackgroundColor === 'sepia') {
    backgroundColor.value = savedBackgroundColor
  }
  
  const savedImageWidth = localStorage.getItem('comic-image-width')
  if (savedImageWidth) {
    imageWidth.value = parseInt(savedImageWidth, 10)
  }
})

// 保存阅读设置
watch(readingMode, (newValue) => {
  localStorage.setItem('comic-reading-mode', newValue)
})

watch(backgroundColor, (newValue) => {
  localStorage.setItem('comic-background-color', newValue)
})

watch(imageWidth, (newValue) => {
  localStorage.setItem('comic-image-width', newValue.toString())
})

// 监听设置抽屉状态
watch(showSettings, (newValue) => {
  if (newValue) {
    showControls.value = true
    if (controlsTimeout.value) {
      clearTimeout(controlsTimeout.value)
      controlsTimeout.value = null
    }
  } else {
    resetControlsTimeout()
  }
})
</script>

<style scoped lang="scss">
.reader-view {
  position: relative;
  min-height: calc(100vh - 60px);
  
  &.fullscreen {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 9999;
    background-color: var(--bg-color, white);
    
    .reader-header {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      z-index: 10;
    }
    
    .chapter-navigation {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      z-index: 10;
    }
    
    .reader-content {
      height: 100vh;
      padding: 60px 0;
    }
  }
}

.reader-header {
  background-color: var(--header-bg-color, white);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 10px 0;
  transition: transform 0.3s;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left-controls,
.right-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.chapter-title {
  margin: 0;
  font-size: 18px;
  color: var(--text-color-primary, #303133);
}

.loading-container,
.error-container {
  padding: 40px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.reader-content {
  display: flex;
  justify-content: center;
  padding: 20px 0;
  transition: background-color 0.3s;
  
  &.white {
    background-color: #ffffff;
    color: #333333;
  }
  
  &.black {
    background-color: #121212;
    color: #ffffff;
  }
  
  &.sepia {
    background-color: #f8f1e3;
    color: #5f4b32;
  }
  
  &.vertical {
    .pages-container {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin: 0 auto;
    }
    
    .page-item {
      text-align: center;
      
      img {
        max-width: 100%;
        height: auto;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      }
    }
  }
  
  &.horizontal {
    .page-item {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100%;
      
      img {
        max-height: 100%;
        max-width: 100%;
        object-fit: contain;
      }
    }
    
    .page-navigation {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 20px;
      margin-top: 20px;
    }
    
    .page-indicator {
      font-size: 14px;
      color: var(--text-color-regular, #606266);
    }
  }
}

.chapter-navigation {
  background-color: var(--header-bg-color, white);
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
  padding: 15px 0;
}

.navigation-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.settings-content {
  padding: 20px;
}

.setting-item {
  margin-bottom: 24px;
  
  .setting-label {
    display: block;
    margin-bottom: 10px;
    font-weight: 500;
    color: var(--text-color-primary, #303133);
  }
}

:deep(.el-dropdown-menu__item.is-active) {
  color: var(--primary-color, #fb7299);
}
</style> 
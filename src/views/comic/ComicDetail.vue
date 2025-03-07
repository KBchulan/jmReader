<template>
  <div class="comic-detail">
    <div v-if="loading" class="loading-container">
      <el-skeleton style="width: 100%" animated>
        <template #template>
          <div style="display: flex; gap: 20px;">
            <div style="width: 240px;">
              <el-skeleton-item variant="image" style="width: 240px; height: 320px;" />
            </div>
            <div style="flex: 1;">
              <el-skeleton-item variant="h1" style="width: 50%;" />
              <div style="display: flex; gap: 20px; margin: 15px 0;">
                <el-skeleton-item variant="text" style="width: 30%;" />
                <el-skeleton-item variant="text" style="width: 30%;" />
              </div>
              <el-skeleton-item variant="text" style="width: 80%;" />
              <el-skeleton-item variant="text" style="width: 80%;" />
              <el-skeleton-item variant="text" style="width: 80%;" />
            </div>
          </div>
        </template>
      </el-skeleton>
      
      <el-skeleton style="margin-top: 40px;" :rows="10" animated />
    </div>
    
    <template v-else-if="comic">
      <!-- 漫画信息 -->
      <div class="comic-info">
        <div class="comic-cover">
          <img :src="comic.cover" :alt="comic.title" />
          <div class="comic-status" :class="comic.status">
            {{ comic.status === 'ongoing' ? '连载中' : '已完结' }}
          </div>
        </div>
        
        <div class="comic-meta">
          <h1 class="comic-title">{{ comic.title }}</h1>
          
          <div class="comic-tags">
            <span v-for="tag in comic.tags" :key="tag" class="tag">{{ tag }}</span>
          </div>
          
          <div class="comic-data">
            <div class="data-item">
              <span class="label">作者</span>
              <span class="value">{{ comic.author }}</span>
            </div>
            <div class="data-item">
              <span class="label">更新</span>
              <span class="value">{{ comic.updateTime }}</span>
            </div>
          </div>
          
          <div class="comic-description">
            <p>{{ comic.description }}</p>
          </div>
          
          <div class="comic-actions">
            <el-button type="primary" @click="startReading">开始阅读</el-button>
            <el-button type="info" plain>收藏</el-button>
          </div>
        </div>
      </div>
      
      <!-- 章节列表 -->
      <div class="chapter-list">
        <section-title title="章节列表">
          <template #right>
            <el-radio-group v-model="chapterOrder" size="small">
              <el-radio-button label="asc">正序</el-radio-button>
              <el-radio-button label="desc">倒序</el-radio-button>
            </el-radio-group>
          </template>
        </section-title>
        
        <div class="chapters">
          <div
            v-for="chapter in displayChapters"
            :key="chapter.id"
            class="chapter-item"
            @click="navigateToChapter(chapter)"
          >
            <span class="chapter-title">{{ chapter.title }}</span>
            <span class="chapter-date">{{ chapter.updateTime }}</span>
          </div>
        </div>
      </div>
    </template>
    
    <div v-else class="error-container">
      <el-empty description="漫画不存在或已被删除" />
      <el-button type="primary" @click="goBack">返回首页</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useComicStore } from '@/stores/comic'
import SectionTitle from '@/components/SectionTitle.vue'
import type { Chapter } from '@/types'

const route = useRoute()
const router = useRouter()
const comicStore = useComicStore()

// 状态
const chapterOrder = ref<'asc' | 'desc'>('desc')
const loading = computed(() => comicStore.loading)
const comic = computed(() => comicStore.currentComic)
const error = computed(() => comicStore.error)

// 计算章节顺序
const displayChapters = computed(() => {
  if (!comic.value || !comic.value.chapters) return []
  
  const chapters = [...comic.value.chapters]
  return chapterOrder.value === 'asc'
    ? chapters.sort((a, b) => a.order - b.order)
    : chapters.sort((a, b) => b.order - a.order)
})

// 获取漫画ID
const comicId = computed(() => route.params.id)

// 监听路由变化，重新加载数据
watch(() => route.params.id, (newId) => {
  if (newId) {
    loadComicDetail(newId.toString())
  }
})

// 加载漫画详情
async function loadComicDetail(id: string | number) {
  try {
    await comicStore.fetchComicDetail(id)
  } catch (err) {
    console.error('加载漫画详情失败', err)
  }
}

// 开始阅读（从第一章开始）
function startReading() {
  if (comic.value && comic.value.chapters && comic.value.chapters.length > 0) {
    const firstChapter = displayChapters.value[0]
    navigateToChapter(firstChapter)
  }
}

// 导航到章节
function navigateToChapter(chapter: Chapter) {
  router.push(`/reader/${chapter.id}`)
}

// 返回首页
function goBack() {
  router.push('/')
}

// 初始化
onMounted(() => {
  if (comicId.value) {
    loadComicDetail(comicId.value)
  }
})
</script>

<style scoped lang="scss">
.comic-detail {
  padding-bottom: 40px;
}

.loading-container,
.error-container {
  padding: 40px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.comic-info {
  display: flex;
  gap: 30px;
  margin-bottom: 40px;
  
  @media (max-width: 768px) {
    flex-direction: column;
  }
}

.comic-cover {
  position: relative;
  width: 240px;
  flex-shrink: 0;
  
  img {
    width: 100%;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  
  .comic-status {
    position: absolute;
    top: 10px;
    right: 0;
    padding: 2px 8px;
    font-size: 12px;
    color: white;
    border-radius: 4px 0 0 4px;
    
    &.ongoing {
      background-color: var(--primary-color, #fb7299);
    }
    
    &.completed {
      background-color: var(--success-color, #67c23a);
    }
  }
  
  @media (max-width: 768px) {
    width: 180px;
    margin: 0 auto;
  }
}

.comic-meta {
  flex: 1;
}

.comic-title {
  font-size: 24px;
  margin: 0 0 16px;
  color: var(--text-color-primary, #303133);
}

.comic-tags {
  margin-bottom: 16px;
}

.comic-data {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 16px;
  
  .data-item {
    display: flex;
    align-items: center;
    
    .label {
      color: var(--text-color-secondary, #909399);
      margin-right: 8px;
    }
    
    .value {
      color: var(--text-color-primary, #303133);
    }
  }
}

.comic-description {
  margin-bottom: 24px;
  color: var(--text-color-regular, #606266);
  line-height: 1.6;
}

.comic-actions {
  display: flex;
  gap: 12px;
}

.chapter-list {
  margin-top: 40px;
}

.chapters {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
  
  .chapter-item {
    padding: 12px 16px;
    border-radius: 4px;
    background-color: var(--bg-color, white);
    border: 1px solid var(--border-color-light, #e4e7ed);
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    transition: all 0.3s;
    
    .chapter-title {
      color: var(--text-color-primary, #303133);
      font-weight: 500;
    }
    
    .chapter-date {
      color: var(--text-color-secondary, #909399);
      font-size: 12px;
    }
    
    &:hover {
      border-color: var(--primary-color, #fb7299);
      transform: translateY(-2px);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
  }
}
</style> 
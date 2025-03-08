<template>
  <div class="ranking-view">
    <h1 class="page-title">漫画排行榜</h1>
    
    <!-- 排行榜类型 -->
    <div class="ranking-tabs">
      <el-tabs v-model="activeTab" @tab-change="handleTabChange">
        <el-tab-pane label="热门排行" name="popular"></el-tab-pane>
        <el-tab-pane label="评分排行" name="rating"></el-tab-pane>
        <el-tab-pane label="收藏排行" name="favorites"></el-tab-pane>
        <el-tab-pane label="更新排行" name="updates"></el-tab-pane>
      </el-tabs>
    </div>
    
    <!-- 漫画列表 -->
    <div class="ranking-list">
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="3" animated v-for="i in 10" :key="i" />
      </div>
      <div v-else>
        <div class="ranking-item" v-for="(comic, index) in rankingComics" :key="comic.id">
          <div class="ranking-number" :class="{ 'top-three': index < 3 }">{{ index + 1 }}</div>
          <div class="ranking-comic" @click="navigateToComic(comic.id)">
            <div class="comic-cover">
              <img :src="comic.cover" :alt="comic.title" />
            </div>
            <div class="comic-info">
              <h3 class="comic-title">{{ comic.title }}</h3>
              <div class="comic-tags">
                <span v-for="tag in comic.tags.slice(0, 3)" :key="tag" class="tag">{{ tag }}</span>
              </div>
              <div class="comic-meta">
                <span class="comic-author">{{ comic.author }}</span>
                <span class="comic-rating">
                  <el-rate :model-value="Number(comic.rating || 0)" disabled text-color="#ff9900" />
                  <span class="rating-value">{{ Number(comic.rating || 0).toFixed(1) }}</span>
                </span>
              </div>
              <p class="comic-description">{{ comic.description?.substring(0, 100) }}{{ comic.description?.length > 100 ? '...' : '' }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useComicStore } from '@/stores/comic'
import { ElMessage } from 'element-plus'

const router = useRouter()
const comicStore = useComicStore()

// 状态
const activeTab = ref('popular')
const loading = computed(() => comicStore.loading)
const comics = computed(() => comicStore.comics)

// 排行榜漫画
const rankingComics = computed(() => {
  const list = [...comics.value]
  
  // 为每个漫画添加随机属性（仅用于演示）
  list.forEach(comic => {
    if (!comic.views) comic.views = Math.floor(Math.random() * 10000)
    if (!comic.rating) comic.rating = (Math.random() * 4 + 1).toFixed(1)
    if (!comic.favorites) comic.favorites = Math.floor(Math.random() * 5000)
  })
  
  // 根据不同的排行类型排序
  switch (activeTab.value) {
    case 'popular':
      return list.sort((a, b) => (b.views || 0) - (a.views || 0)).slice(0, 20)
    case 'rating':
      return list.sort((a, b) => (parseFloat(b.rating as string) || 0) - (parseFloat(a.rating as string) || 0)).slice(0, 20)
    case 'favorites':
      return list.sort((a, b) => (b.favorites || 0) - (a.favorites || 0)).slice(0, 20)
    case 'updates':
      return list.sort((a, b) => new Date(b.updateTime).getTime() - new Date(a.updateTime).getTime()).slice(0, 20)
    default:
      return list.slice(0, 20)
  }
})

// 处理标签切换
const handleTabChange = (tab: string) => {
  activeTab.value = tab
}

// 获取排行榜漫画
const fetchRankingComics = async () => {
  try {
    await comicStore.fetchComics(1, 50)
  } catch (error) {
    console.error('加载排行榜失败', error)
    ElMessage.error('加载排行榜失败')
  }
}

// 导航到漫画详情
const navigateToComic = (id: number | string) => {
  router.push(`/comic/${id}`)
}

// 初始化数据
onMounted(() => {
  fetchRankingComics()
})
</script>

<style scoped lang="scss">
.ranking-view {
  padding: 20px 0 40px;
  margin-top: 0;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 20px;
  color: white;
}

.ranking-tabs {
  margin-bottom: 30px;
  
  :deep(.el-tabs__item) {
    color: #aaa;
    font-size: 16px;
    
    &.is-active {
      color: #fb7299;
    }
    
    &:hover {
      color: #fb7299;
    }
  }
  
  :deep(.el-tabs__active-bar) {
    background-color: #fb7299;
  }
}

.loading-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.ranking-item {
  display: flex;
  margin-bottom: 20px;
  background-color: #2a2a2a;
  border-radius: 4px;
  overflow: hidden;
  transition: all 0.3s;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }
}

.ranking-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  font-size: 24px;
  font-weight: bold;
  color: white;
  background-color: #333;
  
  &.top-three {
    background-color: #fb7299;
  }
}

.ranking-comic {
  display: flex;
  flex: 1;
  cursor: pointer;
}

.comic-cover {
  width: 120px;
  height: 160px;
  overflow: hidden;
  
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s;
    
    &:hover {
      transform: scale(1.05);
    }
  }
}

.comic-info {
  flex: 1;
  padding: 15px;
}

.comic-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 10px;
  color: white;
}

.comic-tags {
  display: flex;
  gap: 5px;
  margin-bottom: 10px;
  
  .tag {
    display: inline-block;
    padding: 2px 6px;
    font-size: 12px;
    border-radius: 2px;
    background-color: rgba(251, 114, 153, 0.2);
    color: #fb7299;
  }
}

.comic-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  
  .comic-author {
    font-size: 14px;
    color: #aaa;
  }
  
  .comic-rating {
    display: flex;
    align-items: center;
    
    .rating-value {
      margin-left: 5px;
      color: #ff9900;
      font-weight: bold;
    }
  }
}

.comic-description {
  font-size: 14px;
  color: #bbb;
  margin: 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 
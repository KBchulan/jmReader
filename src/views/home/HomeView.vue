<template>
  <div class="home-view">
    <!-- 轮播图 -->
    <div class="banner-section">
      <div class="carousel-container">
        <div class="carousel-wrapper">
          <div v-for="(item, index) in bannerItems" :key="index" class="carousel-item" 
            :class="{ 'active': index === currentBannerIndex }"
            @click="navigateToComic(item.id)">
            <img :src="item.cover" :alt="item.title" />
            <div class="banner-content">
              <h3>{{ item.title }}</h3>
              <p class="comic-author">{{ item.author || '百合小漫' }}</p>
              <p class="comic-description" v-if="item.description">{{ item.description }}</p>
              <el-button type="primary" size="small" class="banner-button" @click.stop="navigateToComic(item.id)">
                立即阅读
              </el-button>
            </div>
          </div>
        </div>

        <!-- 控制按钮 -->
        <div class="carousel-controls">
          <button class="carousel-arrow prev-arrow" @click="prevBanner">
            <el-icon><ArrowLeft /></el-icon>
          </button>
          <div class="carousel-indicators">
            <span v-for="(_, index) in bannerItems" :key="index" class="indicator-dot"
              :class="{ active: currentBannerIndex === index }" @click="setCurrentBanner(index)"></span>
          </div>
          <button class="carousel-arrow next-arrow" @click="nextBanner">
            <el-icon><ArrowRight /></el-icon>
          </button>
        </div>
      </div>
    </div>

    <!-- 推荐漫画 -->
    <div class="recommended-section">
      <section-title title="推荐漫画" more-link="/ranking" />
      <div class="recommended-grid">
        <div v-if="loading" class="loading-container">
          <el-skeleton :rows="2" animated />
          <el-skeleton :rows="2" animated />
          <el-skeleton :rows="2" animated />
        </div>
        <div v-else class="grid-container">
          <div v-for="comic in recommendedComics" :key="comic.id" class="grid-item">
            <comic-card :comic="comic" />
          </div>
        </div>
      </div>
    </div>

    <!-- 最新更新 -->
    <div class="latest-section">
      <section-title title="最新更新" more-link="/latest" />
      <div class="latest-grid">
        <div v-if="loading" class="loading-container">
          <el-skeleton :rows="2" animated />
          <el-skeleton :rows="2" animated />
          <el-skeleton :rows="2" animated />
        </div>
        <div v-else class="grid-container">
          <div v-for="comic in latestComics" :key="comic.id" class="grid-item">
            <comic-card :comic="comic" />
          </div>
        </div>
      </div>
    </div>

    <!-- 漫画列表 -->
    <div class="comics-section">
      <section-title title="全部漫画" more-link="/category" />
      <comic-grid :comics="comics" :loading="loading" :pagination="true" :total="total" :default-page="currentPage"
        :default-page-size="pageSize" @page-change="handlePageChange" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useComicStore } from '@/stores/comic'
import SectionTitle from '@/components/SectionTitle.vue'
import ComicCard from '@/components/ComicCard.vue'
import ComicGrid from '@/components/ComicGrid.vue'
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'

const router = useRouter()
const comicStore = useComicStore()

// 状态
const currentPage = ref(1)
const pageSize = ref(Number(import.meta.env.VITE_COMICS_PER_PAGE) || 24)
const total = ref(0)
const loading = computed(() => comicStore.loading)
const comics = computed(() => comicStore.comics)
const recommendedComics = computed(() => {
  // 随机选择3个推荐漫画
  if (comicStore.recommendedComics.length > 3) {
    const shuffled = [...comicStore.recommendedComics].sort(() => 0.5 - Math.random())
    return shuffled.slice(0, 3)
  }
  return comicStore.recommendedComics
})
const latestComics = computed(() => {
  // 随机选择4个最新漫画
  if (comicStore.latestComics.length > 4) {
    const shuffled = [...comicStore.latestComics].sort(() => 0.5 - Math.random())
    return shuffled.slice(0, 4)
  }
  return comicStore.latestComics
})

// 轮播图数据
const bannerItems = ref<any[]>([])
const currentBannerIndex = ref(0)

// 设置当前轮播图索引
const setCurrentBanner = (index: number) => {
  currentBannerIndex.value = index
}

// 自动轮播
let autoplayInterval: number | null = null

const startAutoplay = () => {
  if (autoplayInterval) clearInterval(autoplayInterval)
  autoplayInterval = window.setInterval(() => {
    nextBanner()
  }, 5000)
}

const stopAutoplay = () => {
  if (autoplayInterval) {
    clearInterval(autoplayInterval)
    autoplayInterval = null
  }
}

// 下一张轮播图
const nextBanner = () => {
  currentBannerIndex.value = (currentBannerIndex.value + 1) % bannerItems.value.length
}

// 上一张轮播图
const prevBanner = () => {
  currentBannerIndex.value = (currentBannerIndex.value - 1 + bannerItems.value.length) % bannerItems.value.length
}

// 更新轮播图数据
const updateBannerItems = () => {
  // 从所有漫画中选择作为轮播图
  const allComics = [...comics.value, ...recommendedComics.value, ...latestComics.value]
  
  // 去重
  const uniqueComics = allComics.filter((comic, index, self) => 
    index === self.findIndex(c => c.id === comic.id)
  )
  
  if (uniqueComics.length > 0) {
    // 随机打乱
    const shuffled = [...uniqueComics].sort(() => 0.5 - Math.random())
    // 固定选择3个漫画作为轮播图
    const selected = shuffled.slice(0, 3)
    
    bannerItems.value = selected.map(comic => ({
      id: comic.id,
      title: comic.title,
      description: comic.description?.substring(0, 80) + (comic.description?.length > 80 ? '...' : '') || '',
      author: comic.author || '百合小漫',
      cover: comic.cover
    }))
  }
}

// 初始化数据
onMounted(async () => {
  try {
    // 获取推荐漫画
    await comicStore.fetchRecommendedComics(3)

    // 获取最新漫画
    await comicStore.fetchLatestComics(4)

    // 获取漫画列表
    const result = await comicStore.fetchComics(currentPage.value, pageSize.value)
    total.value = result.total

    // 更新轮播图
    updateBannerItems()

    // 启动自动轮播
    startAutoplay()
  } catch (error) {
    console.error('加载首页数据失败', error)
  }
})

// 组件卸载时清除定时器
onUnmounted(() => {
  stopAutoplay()
})

// 处理页码变化
const handlePageChange = async (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size

  try {
    const result = await comicStore.fetchComics(page, size)
    total.value = result.total
  } catch (error) {
    console.error('加载漫画列表失败', error)
  }
}

// 导航到漫画详情
const navigateToComic = (id: number | string) => {
  router.push(`/comic/${id}`)
}

// 监听漫画数据变化，更新轮播图
watch([() => comics.value, () => recommendedComics.value, () => latestComics.value], () => {
  updateBannerItems()
})
</script>

<style scoped lang="scss">
@use "sass:color";

.home-view {
  padding-bottom: 40px;
  background-color: #222;
  color: white;
  margin-top: 0;
  
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }
}

.banner-section {
  position: relative;
  height: 600px;
  overflow: hidden;
  background-color: #1a1a1a;  
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);

  .carousel-container {
    position: relative;
    width: 100%;
    height: 100%;
  }

  .carousel-wrapper {
    position: relative;
    width: 100%;
    height: 100%;
  }

  .carousel-item {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.5s ease;
    overflow: hidden;
    cursor: pointer;
    border-radius: 8px;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #1a1a1a;

    img {
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      transition: transform 0.5s ease;
    }

    &.active {
      opacity: 1;
      visibility: visible;
      z-index: 1;
    }
  }

  .banner-content {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 20px 30px;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0));
    color: white;
    text-align: left;
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
    
    h3 {
      margin: 0 0 8px;
      font-size: 22px;
      font-weight: 600;
      text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
    }

    .comic-author {
      margin: 0 0 10px;
      font-size: 15px;
      opacity: 0.95;
      color: rgba(255, 255, 255, 0.9);
      font-weight: 500;
    }
    
    .comic-description {
      margin: 0 0 15px;
      font-size: 14px;
      line-height: 1.5;
      opacity: 0.9;
      color: rgba(255, 255, 255, 0.9);
      max-width: 600px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .banner-button {
      background-color: #fb7299;
      border-color: #fb7299;
      border-radius: 4px;
      padding: 8px 16px;
      font-size: 14px;
      font-weight: 500;
      box-shadow: 0 2px 6px rgba(251, 114, 153, 0.3);
      transition: all 0.3s ease;

      &:hover {
        background-color: color.adjust(#fb7299, $lightness: -5%);
        border-color: color.adjust(#fb7299, $lightness: -5%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(251, 114, 153, 0.4);
      }
      
      &:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(251, 114, 153, 0.3);
      }
    }
  }

  .carousel-controls {
    position: absolute;
    bottom: 15px;
    left: 0;
    right: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 2;

    .carousel-indicators {
      display: flex;
      gap: 8px;
      background-color: rgba(0, 0, 0, 0.3);
      padding: 6px 12px;
      border-radius: 20px;

      .indicator-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: rgba(255, 255, 255, 0.5);
        cursor: pointer;
        transition: all 0.3s ease;

        &.active {
          width: 20px;
          border-radius: 4px;
          background-color: #fb7299;
        }

        &:hover {
          background-color: rgba(255, 255, 255, 0.8);
        }
      }
    }
    
    .carousel-arrow {
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background-color: rgba(0, 0, 0, 0.5);
      color: white;
      border: none;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.3s ease;
      opacity: 0;
      
      &:hover {
        background-color: rgba(0, 0, 0, 0.7);
      }
      
      .el-icon {
        font-size: 20px;
      }
      
      &.prev-arrow {
        left: 20px;
      }
      
      &.next-arrow {
        right: 20px;
      }
    }
  }
}

.banner-section:hover {
  .carousel-arrow {
    opacity: 1;
  }
}

.recommended-section,
.latest-section,
.comics-section {
  margin-bottom: 40px;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;

  @media (max-width: 768px) {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 15px;
  }
}

.loading-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;

  :deep(.el-skeleton) {
    --el-skeleton-color: #3a3a3a;
    --el-skeleton-to-color: #4a4a4a;
  }
}

.grid-item {
  transition: transform 0.3s;

  &:hover {
    transform: translateY(-5px);
  }
}
</style>
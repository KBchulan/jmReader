<template>
  <div class="home-view">
    <!-- 轮播图 -->
    <div class="banner-section">
      <el-carousel height="300px" :interval="5000" arrow="always" indicator-position="outside">
        <el-carousel-item v-for="(item, index) in bannerItems" :key="index">
          <div class="banner-item" @click="navigateToComic(item.id)">
            <img :src="item.image" :alt="item.title" />
            <div class="banner-content">
              <h3>{{ item.title }}</h3>
              <p>{{ item.description }}</p>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>

    <!-- 推荐漫画 -->
    <div class="recommended-section">
      <section-title title="推荐漫画" more-link="/category" />
      <div class="recommended-grid">
        <div v-if="loading" class="loading-container">
          <el-skeleton :rows="2" animated />
          <el-skeleton :rows="2" animated />
          <el-skeleton :rows="2" animated />
        </div>
        <div v-else class="grid-container">
          <div
            v-for="comic in recommendedComics"
            :key="comic.id"
            class="grid-item"
          >
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
          <div
            v-for="comic in latestComics"
            :key="comic.id"
            class="grid-item"
          >
            <comic-card :comic="comic" />
          </div>
        </div>
      </div>
    </div>

    <!-- 漫画列表 -->
    <div class="comics-section">
      <section-title title="全部漫画" more-link="/category" />
      <comic-grid
        :comics="comics"
        :loading="loading"
        :pagination="true"
        :total="total"
        :default-page="currentPage"
        :default-page-size="pageSize"
        @page-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useComicStore } from '@/stores/comic'
import SectionTitle from '@/components/SectionTitle.vue'
import ComicCard from '@/components/ComicCard.vue'
import ComicGrid from '@/components/ComicGrid.vue'

const router = useRouter()
const comicStore = useComicStore()

// 状态
const currentPage = ref(1)
const pageSize = ref(Number(import.meta.env.VITE_COMICS_PER_PAGE) || 24)
const total = ref(0)
const loading = computed(() => comicStore.loading)
const comics = computed(() => comicStore.comics)
const recommendedComics = computed(() => comicStore.recommendedComics)
const latestComics = computed(() => comicStore.latestComics)

// 轮播图数据
const bannerItems = ref([
  {
    id: 1,
    title: '热门推荐',
    description: '精选热门漫画，不容错过',
    image: 'https://picsum.photos/id/237/1200/300'
  },
  {
    id: 2,
    title: '新番上线',
    description: '最新上线的精彩漫画',
    image: 'https://picsum.photos/id/238/1200/300'
  },
  {
    id: 3,
    title: '经典回顾',
    description: '经典漫画系列，重温童年',
    image: 'https://picsum.photos/id/239/1200/300'
  }
])

// 初始化数据
onMounted(async () => {
  try {
    // 获取推荐漫画
    await comicStore.fetchRecommendedComics(6)
    
    // 获取最新漫画
    await comicStore.fetchLatestComics(6)
    
    // 获取漫画列表
    const result = await comicStore.fetchComics(currentPage.value, pageSize.value)
    total.value = result.total
  } catch (error) {
    console.error('加载首页数据失败', error)
  }
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
</script>

<style scoped lang="scss">
.home-view {
  padding-bottom: 40px;
}

.banner-section {
  margin-bottom: 30px;
  
  .banner-item {
    position: relative;
    height: 100%;
    cursor: pointer;
    
    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
    
    .banner-content {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      padding: 20px;
      background: linear-gradient(to top, rgba(0, 0, 0, 0.7), transparent);
      color: white;
      
      h3 {
        margin: 0 0 8px;
        font-size: 24px;
      }
      
      p {
        margin: 0;
        font-size: 14px;
        opacity: 0.9;
      }
    }
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
}

.grid-item {
  transition: transform 0.3s;
}
</style> 
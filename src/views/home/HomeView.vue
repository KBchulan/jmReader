<template>
  <div class="home-view">
    <!-- 下载漫画 -->
    <div class="download-section">
      <div class="download-card">
        <div class="download-header">
          <h2>下载漫画</h2>
          <span class="download-tip">输入6位漫画ID，一键下载您喜欢的漫画</span>
        </div>
        <div class="download-form">
          <el-input
            v-model="comicId"
            placeholder="请输入6位漫画ID"
            maxlength="6"
            show-word-limit
            clearable
            class="download-input"
          >
            <template #prefix>
              <el-icon><Download /></el-icon>
            </template>
          </el-input>
          <el-button 
            type="primary" 
            :loading="downloading" 
            @click="downloadComic"
            class="download-button"
            :disabled="!comicId || comicId.length !== 6"
          >
            下载
          </el-button>
        </div>
        <div v-if="downloadMessage" class="download-message" :class="{ 'success': downloadSuccess, 'error': !downloadSuccess }">
          <el-icon v-if="downloadSuccess"><Check /></el-icon>
          <el-icon v-else><Warning /></el-icon>
          {{ downloadMessage }}
        </div>
      </div>
    </div>

    <!-- 轮播图 -->
    <div class="banner-section">
      <el-carousel 
        height="300px" 
        :interval="5000" 
        arrow="always" 
        indicator-position="none" 
        class="banner-carousel"
        @change="handleCarouselChange"
      >
        <el-carousel-item v-for="(item, index) in bannerItems" :key="index">
          <div class="banner-item" @click="navigateToComic(item.id)">
            <img :src="item.cover" :alt="item.title" />
            <div class="banner-content">
              <h3>{{ item.title }}</h3>
              <p>{{ item.description }}</p>
              <el-button type="primary" size="small" class="banner-button" @click.stop="navigateToComic(item.id)">
                立即阅读
              </el-button>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
      <div class="banner-indicators">
        <span 
          v-for="(_, index) in bannerItems" 
          :key="index" 
          class="indicator-dot"
          :class="{ active: currentBannerIndex === index }"
          @click="setCurrentBanner(index)"
        ></span>
      </div>
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
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useComicStore } from '@/stores/comic'
import SectionTitle from '@/components/SectionTitle.vue'
import ComicCard from '@/components/ComicCard.vue'
import ComicGrid from '@/components/ComicGrid.vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { Download, Check, Warning } from '@element-plus/icons-vue'

const router = useRouter()
const comicStore = useComicStore()

// 状态
const currentPage = ref(1)
const pageSize = ref(Number(import.meta.env.VITE_COMICS_PER_PAGE) || 24)
const total = ref(0)
const loading = computed(() => comicStore.loading)
const comics = computed(() => comicStore.comics)
const recommendedComics = computed(() => {
  // 随机选择6个推荐漫画
  if (comicStore.recommendedComics.length > 6) {
    const shuffled = [...comicStore.recommendedComics].sort(() => 0.5 - Math.random())
    return shuffled.slice(0, 6)
  }
  return comicStore.recommendedComics
})
const latestComics = computed(() => {
  // 随机选择6个最新漫画
  if (comicStore.latestComics.length > 6) {
    const shuffled = [...comicStore.latestComics].sort(() => 0.5 - Math.random())
    return shuffled.slice(0, 6)
  }
  return comicStore.latestComics
})

// 下载漫画相关
const comicId = ref('')
const downloading = ref(false)
const downloadMessage = ref('')
const downloadSuccess = ref(false)

// 下载漫画
const downloadComic = async () => {
  if (!comicId.value) {
    ElMessage.warning('请输入漫画ID')
    return
  }
  
  if (!/^\d{6}$/.test(comicId.value)) {
    ElMessage.warning('漫画ID必须是6位数字')
    downloadSuccess.value = false
    downloadMessage.value = '漫画ID必须是6位数字'
    return
  }
  
  downloading.value = true
  downloadMessage.value = '正在下载，请稍候...'
  downloadSuccess.value = true
  
  try {
    const response = await axios.get(`http://localhost:3000/download/${comicId.value}`)
    downloadMessage.value = response.data.message
    downloadSuccess.value = true
    ElMessage.success(response.data.message)
    
    // 下载完成后刷新漫画列表
    setTimeout(async () => {
      await comicStore.fetchComics(currentPage.value, pageSize.value)
      await comicStore.fetchRecommendedComics(6)
      await comicStore.fetchLatestComics(6)
      updateBannerItems() // 更新轮播图
    }, 3000)
  } catch (error: any) {
    console.error('下载漫画失败', error)
    downloadMessage.value = `下载失败: ${error.response?.data?.detail || error.message}`
    downloadSuccess.value = false
    ElMessage.error(downloadMessage.value)
  } finally {
    downloading.value = false
  }
}

// 轮播图数据
const bannerItems = ref<any[]>([])
const currentBannerIndex = ref(0)

// 设置当前轮播图索引
const setCurrentBanner = (index: number) => {
  currentBannerIndex.value = index
}

// 监听轮播图变化
const handleCarouselChange = (index: number) => {
  currentBannerIndex.value = index
}

// 更新轮播图数据
const updateBannerItems = () => {
  // 从所有漫画中随机选择3-5个作为轮播图
  const allComics = [...comics.value, ...recommendedComics.value, ...latestComics.value]
  
  // 去重
  const uniqueComics = allComics.filter((comic, index, self) => 
    index === self.findIndex(c => c.id === comic.id)
  )
  
  if (uniqueComics.length > 0) {
    // 随机打乱并选择前3-5个
    const shuffled = [...uniqueComics].sort(() => 0.5 - Math.random())
    const selected = shuffled.slice(0, Math.min(5, shuffled.length))
    
    bannerItems.value = selected.map(comic => ({
      id: comic.id,
      title: comic.title,
      description: comic.description.substring(0, 50) + (comic.description.length > 50 ? '...' : ''),
      cover: comic.cover
    }))
  }
}

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
    
    // 更新轮播图
    updateBannerItems()
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

// 监听漫画数据变化，更新轮播图
watch([() => comics.value, () => recommendedComics.value, () => latestComics.value], () => {
  updateBannerItems()
})
</script>

<style scoped lang="scss">
@use "sass:color";

.home-view {
  padding-bottom: 40px;
}

.download-section {
  margin-bottom: 30px;
  
  .download-card {
    border-radius: 8px;
    transition: all 0.3s ease;
    background-color: white;
    border: 1px solid #ebeef5;
    padding: 20px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
    
    .download-header {
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 12px;
      
      h2 {
        margin: 0;
        font-size: 18px;
        color: #303133;
        font-weight: 600;
      }
      
      .download-tip {
        font-size: 14px;
        color: #909399;
      }
    }
    
    .download-form {
      display: flex;
      gap: 10px;
      margin-bottom: 10px;
      
      .download-input {
        :deep(.el-input__inner) {
          border-radius: 4px;
          height: 36px;
          font-size: 14px;
        }
        
        :deep(.el-input__prefix) {
          color: #909399;
        }
      }
      
      .download-button {
        border-radius: 4px;
        height: 36px;
        font-size: 14px;
        background-color: #fb7299;
        border-color: #fb7299;
      }
    }
    
    .download-message {
      margin-top: 10px;
      padding: 10px;
      border-radius: 4px;
      font-size: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
      
      &.success {
        background-color: rgba(103, 194, 58, 0.1);
        color: #67c23a;
      }
      
      &.error {
        background-color: rgba(245, 108, 108, 0.1);
        color: #f56c6c;
      }
    }
  }
}

.banner-section {
  margin-bottom: 30px;
  position: relative;
  
  .banner-carousel {
    border-radius: 0;
    overflow: hidden;
    box-shadow: none;
    
    :deep(.el-carousel__arrow) {
      background-color: rgba(0, 0, 0, 0.3);
      border-radius: 50%;
      width: 36px;
      height: 36px;
      
      &:hover {
        background-color: rgba(0, 0, 0, 0.5);
      }
    }
  }
  
  .banner-item {
    position: relative;
    height: 100%;
    cursor: pointer;
    
    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      background-color: #f5f7fa;
    }
    
    .banner-content {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      padding: 20px;
      background: linear-gradient(to top, rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.4), transparent);
      color: white;
      
      h3 {
        margin: 0 0 8px;
        font-size: 24px;
        font-weight: 600;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
      }
      
      p {
        margin: 0 0 12px;
        font-size: 14px;
        opacity: 0.9;
        max-width: 80%;
      }
      
      .banner-button {
        background-color: #fb7299;
        border-color: #fb7299;
        
        &:hover {
          background-color: color.adjust(#fb7299, $lightness: -10%);
          border-color: color.adjust(#fb7299, $lightness: -10%);
        }
      }
    }
  }
  
  .banner-indicators {
    position: absolute;
    bottom: 15px;
    left: 0;
    right: 0;
    display: flex;
    justify-content: center;
    gap: 8px;
    z-index: 10;
    
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
  
  &:hover {
    transform: translateY(-5px);
  }
}
</style> 
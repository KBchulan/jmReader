<template>
  <div class="latest-view">
    <h1 class="page-title">最新更新</h1>

    <!-- 时间筛选 -->
    <div class="time-filter">
      <el-radio-group v-model="timeFilter" @change="handleTimeFilterChange">
        <el-radio-button label="all">全部</el-radio-button>
        <el-radio-button label="today">今天</el-radio-button>
        <el-radio-button label="week">本周</el-radio-button>
        <el-radio-button label="month">本月</el-radio-button>
      </el-radio-group>
    </div>

    <!-- 漫画列表 -->
    <comic-grid :comics="filteredComics" :loading="loading" :pagination="true" :total="total"
      :default-page="currentPage" :default-page-size="pageSize" @page-change="handlePageChange" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useComicStore } from '@/stores/comic'
import ComicGrid from '@/components/ComicGrid.vue'
import { ElMessage } from 'element-plus'

const comicStore = useComicStore()

// 状态
const currentPage = ref(1)
const pageSize = ref(Number(import.meta.env.VITE_COMICS_PER_PAGE) || 24)
const total = ref(0)
const loading = computed(() => comicStore.loading)
const comics = computed(() => comicStore.latestComics)
const timeFilter = ref('all')

// 根据时间筛选漫画
const filteredComics = computed(() => {
  if (timeFilter.value === 'all') {
    return comics.value
  }

  const now = new Date()
  let startDate: Date

  switch (timeFilter.value) {
    case 'today':
      startDate = new Date(now.setHours(0, 0, 0, 0))
      break
    case 'week':
      startDate = new Date(now.setDate(now.getDate() - now.getDay()))
      startDate.setHours(0, 0, 0, 0)
      break
    case 'month':
      startDate = new Date(now.getFullYear(), now.getMonth(), 1)
      break
    default:
      return comics.value
  }

  return comics.value.filter(comic => {
    const updateDate = new Date(comic.updateTime)
    return updateDate >= startDate
  })
})

// 处理时间筛选变化
const handleTimeFilterChange = (value: string) => {
  timeFilter.value = value
  currentPage.value = 1
}

// 处理页码变化
const handlePageChange = async (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  fetchLatestComics()
}

// 获取最新漫画
const fetchLatestComics = async () => {
  try {
    // 获取更多的最新漫画，以便筛选
    await comicStore.fetchLatestComics(50)

    // 根据时间筛选后的总数
    total.value = filteredComics.value.length
  } catch (error) {
    console.error('加载最新漫画失败', error)
    ElMessage.error('加载最新漫画失败')
  }
}

// 初始化数据
onMounted(() => {
  fetchLatestComics()
})
</script>

<style scoped lang="scss">
.latest-view {
  padding: 20px 0 40px;
  margin-top: 0;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 20px;
  color: white;
}

.time-filter {
  margin-bottom: 30px;

  :deep(.el-radio-button__inner) {
    background-color: #2a2a2a;
    border-color: #3a3a3a;
    color: white;

    &:hover {
      color: #fb7299;
    }
  }

  :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
    background-color: #fb7299;
    border-color: #fb7299;
    box-shadow: -1px 0 0 0 #fb7299;
  }
}
</style>
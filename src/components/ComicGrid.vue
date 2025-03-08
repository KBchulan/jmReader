<template>
  <div class="comic-grid">
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="2" animated />
      <el-skeleton :rows="2" animated />
      <el-skeleton :rows="2" animated />
      <el-skeleton :rows="2" animated />
    </div>

    <div v-else-if="comics.length === 0" class="empty-container">
      <el-empty description="暂无漫画" />
    </div>

    <div v-else class="grid-container">
      <div v-for="comic in comics" :key="comic.id" class="grid-item">
        <comic-card :comic="comic" />
      </div>
    </div>

    <div v-if="pagination && !loading" class="pagination-container">
      <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :page-sizes="[12, 24, 36, 48]"
        :background="true" layout="total, sizes, prev, pager, next, jumper" :total="total"
        @size-change="handleSizeChange" @current-change="handleCurrentChange" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Comic } from '@/types'
import ComicCard from './ComicCard.vue'

const props = defineProps<{
  comics: Comic[]
  loading?: boolean
  pagination?: boolean
  total?: number
  defaultPage?: number
  defaultPageSize?: number
}>()

const emit = defineEmits<{
  (e: 'page-change', page: number, pageSize: number): void
}>()

const currentPage = ref(props.defaultPage || 1)
const pageSize = ref(props.defaultPageSize || 24)

// 监听页码和每页数量变化
watch(() => props.defaultPage, (newVal) => {
  if (newVal) {
    currentPage.value = newVal
  }
})

watch(() => props.defaultPageSize, (newVal) => {
  if (newVal) {
    pageSize.value = newVal
  }
})

// 处理页码变化
const handleCurrentChange = (page: number) => {
  currentPage.value = page
  emit('page-change', page, pageSize.value)
}

// 处理每页数量变化
const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  emit('page-change', 1, size)
}
</script>

<style scoped lang="scss">
.comic-grid {
  width: 100%;
}

.loading-container,
.empty-container {
  padding: 40px 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
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

.grid-item {
  transition: transform 0.3s;
}

.pagination-container {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}
</style>
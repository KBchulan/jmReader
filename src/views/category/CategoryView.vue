<template>
  <div class="category-view">
    <h1 class="page-title">漫画分类</h1>
    
    <!-- 分类标签 -->
    <div class="category-tags">
      <el-tag 
        v-for="tag in categoryTags" 
        :key="tag.id" 
        :class="{ active: activeTag === tag.id }"
        @click="setActiveTag(tag.id)"
      >
        {{ tag.name }}
      </el-tag>
    </div>
    
    <!-- 漫画列表 -->
    <comic-grid
      :comics="filteredComics"
      :loading="loading"
      :pagination="true"
      :total="total"
      :default-page="currentPage"
      :default-page-size="pageSize"
      @page-change="handlePageChange"
    />
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
const comics = computed(() => comicStore.comics)
const activeTag = ref('all')

// 分类标签
const categoryTags = [
  { id: 'all', name: '全部' },
  { id: '百合', name: '百合' },
  { id: '校园', name: '校园' },
  { id: '恋爱', name: '恋爱' },
  { id: '治愈', name: '治愈' },
  { id: '奇幻', name: '奇幻' },
  { id: '冒险', name: '冒险' },
  { id: '搞笑', name: '搞笑' },
  { id: '日常', name: '日常' }
]

// 设置当前标签
const setActiveTag = (tagId: string) => {
  activeTag.value = tagId
  currentPage.value = 1
  fetchComics()
}

// 获取漫画列表
const fetchComics = async () => {
  try {
    // 根据选中的标签获取漫画
    if (activeTag.value !== 'all') {
      // 如果选择了特定标签，则获取该标签下的漫画
      await comicStore.fetchComicsByTag(activeTag.value, currentPage.value, pageSize.value)
    } else {
      // 如果选择了全部，则获取所有漫画
      await comicStore.fetchComics(currentPage.value, pageSize.value)
    }
    total.value = activeTag.value === 'all' ? comicStore.comics.length : comicStore.filteredComics.length
  } catch (error) {
    console.error('加载漫画列表失败', error)
    ElMessage.error('加载漫画列表失败')
  }
}

// 过滤后的漫画列表
const filteredComics = computed(() => {
  if (activeTag.value === 'all') {
    return comics.value
  }
  return comicStore.filteredComics
})

// 处理页码变化
const handlePageChange = async (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  fetchComics()
}

// 初始化数据
onMounted(() => {
  fetchComics()
})
</script>

<style scoped lang="scss">
.category-view {
  padding: 20px 0 40px;
  margin-top: 0;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 20px;
  color: white;
}

.category-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 30px;
  
  .el-tag {
    cursor: pointer;
    padding: 8px 16px;
    font-size: 14px;
    background-color: #2a2a2a;
    border-color: #2a2a2a;
    color: white;
    transition: all 0.3s;
    
    &:hover {
      background-color: #3a3a3a;
      border-color: #3a3a3a;
    }
    
    &.active {
      background-color: #fb7299;
      border-color: #fb7299;
      color: white;
    }
  }
}
</style> 
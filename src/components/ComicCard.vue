<template>
  <div class="comic-card card" @click="navigateToDetail">
    <div class="comic-cover">
      <lazy-image :src="comic.cover" :alt="comic.title" />
      <div class="comic-status" :class="comic.status">
        {{ comic.status === 'ongoing' ? '连载中' : '已完结' }}
      </div>
    </div>
    <div class="comic-info">
      <h3 class="comic-title truncate">{{ comic.title }}</h3>
      <div class="comic-tags">
        <span v-for="tag in comic.tags.slice(0, 3)" :key="tag" class="tag">{{ tag }}</span>
      </div>
      <div class="comic-meta">
        <span class="comic-author truncate">{{ comic.author }}</span>
        <span class="comic-update">{{ comic.updateTime }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Comic } from '@/types'
import LazyImage from './LazyImage.vue'

const props = defineProps<{
  comic: Comic
}>()

const router = useRouter()

const navigateToDetail = () => {
  router.push(`/comic/${props.comic.id}`)
}
</script>

<style scoped lang="scss">
.comic-card {
  cursor: pointer;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.comic-cover {
  position: relative;
  padding-top: 133%; // 3:4 比例
  overflow: hidden;
  
  .lazy-image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    transition: transform 0.3s ease;
  }
  
  .comic-status {
    position: absolute;
    top: 10px;
    right: 0;
    padding: 2px 8px;
    font-size: 12px;
    color: white;
    border-radius: 4px 0 0 4px;
    z-index: 1;
    
    &.ongoing {
      background-color: var(--primary-color, #fb7299);
    }
    
    &.completed {
      background-color: var(--success-color, #67c23a);
    }
  }
}

.comic-info {
  padding: 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.comic-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px;
  color: var(--text-color-primary, #303133);
}

.comic-tags {
  margin-bottom: 8px;
  min-height: 24px;
}

.comic-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-color-secondary, #909399);
  margin-top: auto;
}

.comic-author {
  max-width: 60%;
}

.comic-card:hover {
  .comic-cover .lazy-image {
    transform: scale(1.05);
  }
}
</style> 
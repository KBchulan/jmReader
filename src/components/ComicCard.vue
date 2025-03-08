<template>
  <div class="comic-card" @click="navigateToDetail">
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
        <span class="comic-update">{{ formatDate(comic.updateTime) }}</span>
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

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24))

  if (diffDays === 0) {
    return '今天'
  } else if (diffDays === 1) {
    return '昨天'
  } else if (diffDays < 7) {
    return `${diffDays}天前`
  } else if (diffDays < 30) {
    return `${Math.floor(diffDays / 7)}周前`
  } else {
    return `${date.getMonth() + 1}月${date.getDate()}日`
  }
}
</script>

<style scoped lang="scss">
@use "sass:color";

.comic-card {
  cursor: pointer;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  border-radius: 4px;
  background-color: #2a2a2a;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }
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
    transition: transform 0.4s ease;
    object-fit: cover;
  }

  .comic-status {
    position: absolute;
    top: 8px;
    right: 0;
    padding: 2px 6px;
    font-size: 12px;
    color: white;
    border-radius: 4px 0 0 4px;
    z-index: 2;
    font-weight: 500;

    &.ongoing {
      background-color: #fb7299;
    }

    &.completed {
      background-color: #67c23a;
    }
  }
}

.comic-info {
  padding: 10px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.comic-title {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 6px;
  color: white;
  line-height: 1.4;
}

.comic-tags {
  margin-bottom: 6px;
  min-height: 22px;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;

  .tag {
    display: inline-block;
    padding: 1px 4px;
    font-size: 12px;
    border-radius: 2px;
    background-color: rgba(251, 114, 153, 0.2);
    color: #fb7299;
  }
}

.comic-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #aaa;
  margin-top: auto;
}

.comic-author {
  max-width: 60%;
  font-weight: 500;
}

.comic-update {
  color: #aaa;
}

.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
<template>
  <div class="section-title">
    <h2 class="title">{{ title }}</h2>
    <div v-if="$slots.right" class="right-content">
      <slot name="right"></slot>
    </div>
    <router-link v-else-if="moreLink" :to="moreLink" class="more-link">
      更多 <el-icon><ArrowRight /></el-icon>
    </router-link>
  </div>
</template>

<script setup lang="ts">
import { ArrowRight } from '@element-plus/icons-vue'

defineProps<{
  title: string
  moreLink?: string
}>()
</script>

<style scoped lang="scss">
.section-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  
  .title {
    font-size: 20px;
    font-weight: 600;
    color: var(--text-color-primary, #303133);
    margin: 0;
    position: relative;
    padding-left: 12px;
    
    &::before {
      content: '';
      position: absolute;
      left: 0;
      top: 50%;
      transform: translateY(-50%);
      width: 4px;
      height: 18px;
      background-color: var(--primary-color, #fb7299);
      border-radius: 2px;
    }
  }
  
  .more-link {
    font-size: 14px;
    display: flex;
    align-items: center;
    
    .el-icon {
      margin-left: 4px;
      transition: transform 0.3s;
    }
    
    &:hover .el-icon {
      transform: translateX(3px);
    }
  }
}
</style> 
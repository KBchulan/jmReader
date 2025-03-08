<template>
  <div class="section-title">
    <div class="title-wrapper">
      <div class="title-indicator"></div>
      <h2 class="title">{{ title }}</h2>
    </div>
    <div v-if="$slots.right" class="right-content">
      <slot name="right"></slot>
    </div>
    <router-link v-else-if="moreLink" :to="moreLink" class="more-link">
      更多 <el-icon>
        <ArrowRight />
      </el-icon>
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
  
  .title-wrapper {
    display: flex;
    align-items: center;
  }

  .title-indicator {
    width: 4px;
    height: 16px;
    background-color: #fb7299;
    border-radius: 2px;
    margin-right: 8px;
  }

  .title {
    font-size: 18px;
    font-weight: 600;
    color: #303133;
    margin: 0;
  }

  .more-link {
    font-size: 14px;
    display: flex;
    align-items: center;
    color: #909399;
    text-decoration: none;

    &:hover {
      color: #fb7299;
    }

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
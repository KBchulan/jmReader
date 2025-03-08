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
@use "sass:color";

.section-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 25px;
  padding-bottom: 10px;
  border-bottom: 1px solid #3a3a3a;
  
  .title-wrapper {
    display: flex;
    align-items: center;
  }

  .title-indicator {
    width: 5px;
    height: 20px;
    background-color: #fb7299;
    border-radius: 2px;
    margin-right: 10px;
  }

  .title {
    font-size: 20px;
    font-weight: 600;
    color: white;
    margin: 0;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  }

  .more-link {
    font-size: 14px;
    display: flex;
    align-items: center;
    color: #fb7299;
    text-decoration: none;
    font-weight: 500;

    &:hover {
      color: color.adjust(#fb7299, $lightness: -10%);
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
<template>
  <router-view />
</template>

<script setup lang="ts">
import { useTheme } from '@/composables/useTheme'

// 初始化主题
useTheme()
</script>

<style>
/* 全局样式可以在这里添加 */
</style>

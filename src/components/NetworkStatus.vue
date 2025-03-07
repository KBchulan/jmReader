<template>
  <div v-if="!isOnline || showConnectionStatus" class="network-status" :class="{ 'is-offline': !isOnline }">
    <el-alert :title="isOnline ? '网络已连接' : '网络连接已断开'" :type="isOnline ? 'success' : 'error'" :closable="isOnline" @close="hideConnectionStatus">
      <template #default>
        <div class="alert-content">
          <el-icon class="status-icon">
            <component :is="isOnline ? 'Check' : 'Warning'" />
          </el-icon>
          <span>{{ isOnline ? '您的网络已恢复连接' : '请检查您的网络连接' }}</span>
        </div>
      </template>
    </el-alert>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useTimeoutFn } from '@vueuse/core'
import { Check, Warning } from '@element-plus/icons-vue'

// 状态
const isOnline = ref(navigator.onLine)
const showConnectionStatus = ref(false)

// 超时函数，用于自动隐藏恢复连接提示
const { start: startHideTimer, stop: stopHideTimer } = useTimeoutFn(() => {
  hideConnectionStatus()
}, 3000)

// 处理连接状态变化
function handleOnline() {
  isOnline.value = true
  showConnectionStatus.value = true
  startHideTimer()
}

function handleOffline() {
  isOnline.value = false
  showConnectionStatus.value = true
  stopHideTimer()
}

// 隐藏连接状态提示
function hideConnectionStatus() {
  showConnectionStatus.value = false
}

// 注册和移除事件监听
onMounted(() => {
  window.addEventListener('online', handleOnline)
  window.addEventListener('offline', handleOffline)
})

onUnmounted(() => {
  window.removeEventListener('online', handleOnline)
  window.removeEventListener('offline', handleOffline)
})
</script>

<style scoped lang="scss">
.network-status {
  position: fixed;
  top: 60px;
  left: 0;
  right: 0;
  z-index: 1000;
  
  &.is-offline {
    .el-alert {
      margin: 0;
    }
  }
  
  .alert-content {
    display: flex;
    align-items: center;
    gap: 5px;
  }
  
  .status-icon {
    font-size: 18px;
    margin-right: 5px;
  }
}
</style> 
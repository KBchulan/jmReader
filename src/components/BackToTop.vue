<template>
  <transition name="fade">
    <div v-if="show" class="back-to-top" @click="scrollToTop">
      <el-icon>
        <ArrowUp />
      </el-icon>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useThrottleFn } from '@vueuse/core'
import { ArrowUp } from '@element-plus/icons-vue'

// 配置
const props = withDefaults(defineProps<{
  visibilityHeight?: number; // 滚动高度达到此参数才出现
  right?: number; // 距离右侧距离
  bottom?: number; // 距离底部距离
  duration?: number; // 滚动动画持续时间
}>(), {
  visibilityHeight: 400,
  right: 30,
  bottom: 30,
  duration: 300
})

// 是否显示
const show = ref(false)

// 处理滚动事件
const handleScroll = useThrottleFn(() => {
  show.value = window.pageYOffset > props.visibilityHeight
}, 200)

// 滚动到顶部
function scrollToTop() {
  const startTime = Date.now()
  const startScrollY = window.pageYOffset

  function scrollStep() {
    const elapsed = Date.now() - startTime
    const progress = Math.min(elapsed / props.duration, 1)
    const easeProgress = 1 - Math.pow(1 - progress, 4) // easeOutQuart
    window.scrollTo(0, startScrollY * (1 - easeProgress))

    if (progress < 1) {
      window.requestAnimationFrame(scrollStep)
    }
  }

  window.requestAnimationFrame(scrollStep)
}

// 添加和移除滚动事件监听
onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  handleScroll() // 初始检查
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped lang="scss">
.back-to-top {
  position: fixed;
  right: v-bind('`${props.right}px`');
  bottom: v-bind('`${props.bottom}px`');
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--primary-color, #fb7299);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 99;
  transition: background-color 0.3s, transform 0.3s;
  
  &:hover {
    background-color: var(--primary-color-light, #ffa5c2);
    transform: translateY(-3px);
  }
  
  &:active {
    background-color: var(--primary-color-dark, #d65f87);
    transform: translateY(0);
  }
  
  .el-icon {
    font-size: 20px;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style> 
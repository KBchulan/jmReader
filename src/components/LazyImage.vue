<template>
  <div class="lazy-image" :class="{ 'is-loaded': loaded, 'is-error': error }">
    <div v-if="!loaded && !error" class="lazy-image-placeholder">
      <div class="lazy-image-skeleton"></div>
    </div>
    <img ref="imgRef" :src="src" :alt="alt" v-show="loaded" @load="handleLoad" @error="handleError" />
    <div v-if="error" class="lazy-image-error">
      <el-icon>
        <PictureFilled />
      </el-icon>
      <span>加载失败</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { PictureFilled } from '@element-plus/icons-vue'
import { useIntersectionObserver } from '@vueuse/core'

// 属性
const props = defineProps<{
  src: string
  alt?: string
  threshold?: number // 元素可见性阈值，默认为0.1
}>()

// 状态
const imgRef = ref<HTMLImageElement | null>(null)
const loaded = ref(false)
const error = ref(false)
const isIntersecting = ref(false)
const actualSrc = ref('')

// 当图片在视口中时才加载图片
const { stop } = useIntersectionObserver(
  imgRef,
  ([{ isIntersecting: newIsIntersecting }]) => {
    isIntersecting.value = newIsIntersecting
    if (isIntersecting.value && imgRef.value && !loaded.value && !error.value) {
      // 开始加载图片
      actualSrc.value = props.src
      imgRef.value.src = actualSrc.value
    }
  },
  {
    threshold: props.threshold || 0.1
  }
)

// 处理图片加载成功
function handleLoad() {
  loaded.value = true
}

// 处理图片加载错误
function handleError() {
  error.value = true
}

// 卸载时停止观察
onUnmounted(() => {
  stop()
})
</script>

<style scoped lang="scss">
.lazy-image {
  position: relative;
  overflow: hidden;
  width: 100%;
  height: 100%;
  background-color: var(--bg-color-secondary, #f5f7fa);
  border-radius: 4px;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: opacity 0.3s;
  }

  &.is-loaded img {
    opacity: 1;
  }
}

.lazy-image-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lazy-image-skeleton {
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.lazy-image-error {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-color-secondary, #f5f7fa);
  color: var(--text-color-secondary, #909399);

  .el-icon {
    font-size: 24px;
    margin-bottom: 8px;
  }

  span {
    font-size: 12px;
  }
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }

  100% {
    background-position: -200% 0;
  }
}
</style>
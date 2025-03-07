import { ref, onMounted, onUnmounted } from 'vue'
import { useThrottleFn } from '@vueuse/core'

/**
 * 滚动位置跟踪组合式函数
 * @param options 配置选项
 */
export function useScrollPosition(options: {
  throttle?: number; // 节流时间，默认100ms
  target?: HTMLElement | null; // 目标元素，默认为window
} = {}) {
  const { throttle = 100, target = null } = options

  // 滚动位置
  const scrollX = ref(0)
  const scrollY = ref(0)

  // 滚动方向
  const isScrollingUp = ref(false)
  const isScrollingDown = ref(false)
  const isScrollingLeft = ref(false)
  const isScrollingRight = ref(false)

  // 上一次滚动位置
  let lastScrollX = 0
  let lastScrollY = 0

  // 处理滚动事件
  const handleScroll = useThrottleFn(() => {
    const currentScrollX = target
      ? target.scrollLeft
      : window.scrollX || window.pageXOffset || document.documentElement.scrollLeft
    const currentScrollY = target
      ? target.scrollTop
      : window.scrollY || window.pageYOffset || document.documentElement.scrollTop

    // 更新方向状态
    isScrollingUp.value = currentScrollY < lastScrollY
    isScrollingDown.value = currentScrollY > lastScrollY
    isScrollingLeft.value = currentScrollX < lastScrollX
    isScrollingRight.value = currentScrollX > lastScrollX

    // 保存当前位置
    scrollX.value = currentScrollX
    scrollY.value = currentScrollY
    lastScrollX = currentScrollX
    lastScrollY = currentScrollY
  }, throttle)

  // 添加和移除事件监听
  onMounted(() => {
    const scrollTarget = target || window
    scrollTarget.addEventListener('scroll', handleScroll, { passive: true })
    handleScroll() // 初始化位置
  })

  onUnmounted(() => {
    const scrollTarget = target || window
    scrollTarget.removeEventListener('scroll', handleScroll)
  })

  return {
    scrollX,
    scrollY,
    isScrollingUp,
    isScrollingDown,
    isScrollingLeft,
    isScrollingRight
  }
} 
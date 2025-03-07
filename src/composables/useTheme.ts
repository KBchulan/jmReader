import { ref, watch, onMounted } from 'vue'
import type { ThemeMode } from '@/types'
import { usePreferredDark } from '@vueuse/core'

const THEME_KEY = 'comic-theme-mode'
const COLOR_KEY = 'comic-theme-color'

// 主题模式列表
export const themeModes: { label: string; value: ThemeMode }[] = [
  { label: '亮色', value: 'light' },
  { label: '暗色', value: 'dark' },
  { label: '自动', value: 'auto' }
]

// 颜色主题列表
export const colorThemes = [
  { label: '粉色', value: 'pink-theme' },
  { label: '蓝色', value: 'blue-theme' },
  { label: '绿色', value: 'green-theme' },
  { label: '紫色', value: 'purple-theme' }
]

export function useTheme() {
  // 主题模式和颜色主题
  const themeMode = ref<ThemeMode>('auto')
  const colorTheme = ref(colorThemes[0].value)
  
  // 系统暗色模式偏好
  const prefersDark = usePreferredDark()
  
  // 初始化主题
  onMounted(() => {
    // 从本地存储加载主题设置
    const savedThemeMode = localStorage.getItem(THEME_KEY) as ThemeMode
    if (savedThemeMode && themeModes.some(t => t.value === savedThemeMode)) {
      themeMode.value = savedThemeMode
    }
    
    const savedColorTheme = localStorage.getItem(COLOR_KEY)
    if (savedColorTheme && colorThemes.some(t => t.value === savedColorTheme)) {
      colorTheme.value = savedColorTheme
    }
    
    // 初始应用主题
    applyTheme()
  })
  
  // 当主题模式改变时保存并应用
  watch(themeMode, () => {
    localStorage.setItem(THEME_KEY, themeMode.value)
    applyTheme()
  })
  
  // 当颜色主题改变时保存并应用
  watch(colorTheme, () => {
    localStorage.setItem(COLOR_KEY, colorTheme.value)
    applyTheme()
  })
  
  // 当系统暗色偏好改变时，如果当前是自动模式，则应用主题
  watch(prefersDark, () => {
    if (themeMode.value === 'auto') {
      applyTheme()
    }
  })
  
  // 应用主题到文档
  function applyTheme() {
    // 移除所有主题相关的类
    document.documentElement.classList.remove('dark-theme')
    colorThemes.forEach(theme => {
      document.documentElement.classList.remove(theme.value)
    })
    
    // 添加颜色主题类
    document.documentElement.classList.add(colorTheme.value)
    
    // 根据主题模式设置暗色主题
    let isDark = false
    
    if (themeMode.value === 'dark') {
      isDark = true
    } else if (themeMode.value === 'auto') {
      isDark = prefersDark.value
    }
    
    if (isDark) {
      document.documentElement.classList.add('dark-theme')
    }
  }
  
  // 切换主题模式
  function setThemeMode(mode: ThemeMode) {
    themeMode.value = mode
  }
  
  // 切换颜色主题
  function setColorTheme(theme: string) {
    colorTheme.value = theme
  }
  
  return {
    themeMode,
    colorTheme,
    themeModes,
    colorThemes,
    setThemeMode,
    setColorTheme,
    isDarkMode: () => {
      return themeMode.value === 'dark' || 
        (themeMode.value === 'auto' && prefersDark.value)
    }
  }
} 
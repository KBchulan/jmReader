<template>
  <div class="theme-switcher">
    <el-popover
      placement="top"
      :width="240"
      trigger="click"
      popper-class="theme-popover"
    >
      <template #reference>
        <div class="theme-button">
          <el-icon v-if="isDarkMode"><Moon /></el-icon>
          <el-icon v-else><Sunny /></el-icon>
        </div>
      </template>
      
      <div class="theme-panel">
        <h3>主题设置</h3>
        
        <div class="theme-section">
          <div class="section-title">主题模式</div>
          <div class="theme-mode-options">
            <div
              v-for="mode in themeModes"
              :key="mode.value"
              class="theme-mode-option"
              :class="{ active: themeMode === mode.value }"
              @click="setThemeMode(mode.value)"
            >
              <el-icon v-if="mode.value === 'light'"><Sunny /></el-icon>
              <el-icon v-else-if="mode.value === 'dark'"><Moon /></el-icon>
              <el-icon v-else><Monitor /></el-icon>
              <span>{{ mode.label }}</span>
            </div>
          </div>
        </div>
        
        <div class="theme-section">
          <div class="section-title">颜色主题</div>
          <div class="color-theme-options">
            <div
              v-for="theme in colorThemes"
              :key="theme.value"
              class="color-theme-option"
              :class="[theme.value, { active: colorTheme === theme.value }]"
              @click="setColorTheme(theme.value)"
            ></div>
          </div>
        </div>
      </div>
    </el-popover>
  </div>
</template>

<script setup lang="ts">
import { useTheme, themeModes, colorThemes } from '@/composables/useTheme'
import { Sunny, Moon, Monitor } from '@element-plus/icons-vue'
import { computed } from 'vue'

const { themeMode, colorTheme, setThemeMode, setColorTheme } = useTheme()
const isDarkMode = computed(() => {
  return themeMode.value === 'dark' || 
    (themeMode.value === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches)
})
</script>

<style scoped lang="scss">
.theme-switcher {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 99;
}

.theme-button {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--primary-color, #fb7299);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  }
  
  .el-icon {
    font-size: 20px;
  }
}

.theme-panel {
  padding: 10px;
  
  h3 {
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 16px;
    font-weight: 600;
    text-align: center;
    color: var(--text-color-primary, #303133);
  }
  
  .theme-section {
    margin-bottom: 15px;
    
    .section-title {
      font-size: 14px;
      margin-bottom: 8px;
      color: var(--text-color-secondary, #909399);
    }
  }
  
  .theme-mode-options {
    display: flex;
    justify-content: space-between;
    
    .theme-mode-option {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 8px;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.2s;
      
      .el-icon {
        font-size: 20px;
        margin-bottom: 4px;
      }
      
      span {
        font-size: 12px;
      }
      
      &:hover {
        background-color: rgba(0, 0, 0, 0.05);
      }
      
      &.active {
        background-color: var(--primary-color, #fb7299);
        color: white;
      }
    }
  }
  
  .color-theme-options {
    display: flex;
    justify-content: space-between;
    
    .color-theme-option {
      width: 30px;
      height: 30px;
      border-radius: 50%;
      cursor: pointer;
      transition: all 0.2s;
      position: relative;
      
      &:hover {
        transform: scale(1.1);
      }
      
      &.active::after {
        content: '';
        position: absolute;
        top: -4px;
        right: -4px;
        bottom: -4px;
        left: -4px;
        border: 2px solid var(--primary-color, #fb7299);
        border-radius: 50%;
      }
      
      &.pink-theme {
        background-color: #fb7299;
      }
      
      &.blue-theme {
        background-color: #1976d2;
      }
      
      &.green-theme {
        background-color: #388e3c;
      }
      
      &.purple-theme {
        background-color: #7b1fa2;
      }
    }
  }
}

:deep(.theme-popover) {
  padding: 0;
  
  .el-popper__arrow {
    display: none;
  }
}
</style> 
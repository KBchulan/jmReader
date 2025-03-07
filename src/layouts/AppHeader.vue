<template>
  <header class="app-header">
    <div class="container">
      <div class="header-content">
        <!-- Logo -->
        <div class="logo">
          <router-link to="/">
            <div class="logo-content">
              <svg class="logo-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
              </svg>
              <h1>漫画阅读</h1>
            </div>
          </router-link>
        </div>

        <!-- 导航 -->
        <nav class="nav-menu">
          <router-link to="/" active-class="active">首页</router-link>
          <router-link to="/category" active-class="active">分类</router-link>
          <router-link to="/ranking" active-class="active">排行榜</router-link>
          <router-link to="/latest" active-class="active">最新更新</router-link>
        </nav>

        <!-- 搜索框 -->
        <div class="search-box">
          <el-input v-model="searchKeyword" placeholder="搜索漫画名称或ID" class="search-input" @keyup.enter="handleSearch">
            <template #suffix>
              <el-icon class="search-icon" @click="handleSearch">
                <Search />
              </el-icon>
            </template>
          </el-input>
        </div>

        <!-- 主题切换 -->
        <div class="theme-switcher">
          <el-dropdown trigger="click" @command="handleThemeChange">
            <el-button type="primary" plain size="small">
              主题设置
              <el-icon class="el-icon--right">
                <ArrowDown />
              </el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item-group title="主题模式">
                  <el-dropdown-item v-for="mode in themeModes" :key="mode.value"
                    :command="{ type: 'mode', value: mode.value }" :class="{ 'is-active': themeMode === mode.value }">
                    {{ mode.label }}
                  </el-dropdown-item>
                </el-dropdown-item-group>
                <el-dropdown-item-group title="颜色主题">
                  <el-dropdown-item v-for="theme in colorThemes" :key="theme.value"
                    :command="{ type: 'color', value: theme.value }"
                    :class="{ 'is-active': colorTheme === theme.value }">
                    {{ theme.label }}
                  </el-dropdown-item>
                </el-dropdown-item-group>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Search, ArrowDown } from '@element-plus/icons-vue'
import { useTheme, themeModes, colorThemes } from '@/composables/useTheme'

const router = useRouter()
const searchKeyword = ref('')

// 使用主题组合式函数
const { themeMode, colorTheme, setThemeMode, setColorTheme } = useTheme()

// 处理搜索
const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    router.push({
      path: '/search',
      query: { keyword: searchKeyword.value.trim() }
    })
  }
}

// 处理主题变更
const handleThemeChange = (command: { type: 'mode' | 'color'; value: string }) => {
  if (command.type === 'mode') {
    setThemeMode(command.value as any)
  } else if (command.type === 'color') {
    setColorTheme(command.value)
  }
}
</script>

<style scoped lang="scss">
.app-header {
  background-color: var(--header-bg-color, white);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
  height: 60px;
  display: flex;
  align-items: center;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.logo {
  h1 {
    font-size: 1.5rem;
    color: var(--primary-color, #fb7299);
    margin: 0;
    font-weight: bold;
  }
  
  .logo-content {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .logo-icon {
    width: 24px;
    height: 24px;
    stroke: var(--primary-color, #fb7299);
  }
}

.nav-menu {
  display: flex;
  gap: 20px;

  a {
    padding: 5px 0;
    position: relative;
    color: var(--text-color-regular, #606266);

    &:hover,
    &.active {
      color: var(--primary-color, #fb7299);
    }

    &.active::after {
      content: '';
      position: absolute;
      bottom: -2px;
      left: 0;
      width: 100%;
      height: 2px;
      background-color: var(--primary-color, #fb7299);
    }
  }
}

.search-box {
  width: 240px;

  .search-input {
    :deep(.el-input__inner) {
      border-radius: 20px;
    }
  }

  .search-icon {
    cursor: pointer;

    &:hover {
      color: var(--primary-color, #fb7299);
    }
  }
}

.theme-switcher {
  :deep(.el-dropdown-menu__item.is-active) {
    color: var(--primary-color, #fb7299);
  }
}

@media (max-width: 768px) {
  .nav-menu {
    display: none;
  }

  .search-box {
    width: 160px;
  }
}
</style>
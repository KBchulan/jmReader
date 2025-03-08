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

        <!-- 登录按钮 -->
        <div class="login-button">
          <el-button type="primary" size="small">登录</el-button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Search } from '@element-plus/icons-vue'
import { useTheme } from '@/composables/useTheme'

const router = useRouter()
const searchKeyword = ref('')

// 使用主题组合式函数
const { themeMode, colorTheme } = useTheme()

// 处理搜索
const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    router.push({
      path: '/search',
      query: { keyword: searchKeyword.value.trim() }
    })
  }
}
</script>

<style scoped lang="scss">
@use "sass:color";

.app-header {
  background-color: #fb7299;
  position: sticky;
  top: 0;
  z-index: 100;
  height: 56px;
  display: flex;
  align-items: center;
  transition: background-color 0.3s;
  color: white;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 15px;
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
    color: white;
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
    stroke: white;
  }
}

.nav-menu {
  display: flex;
  gap: 30px;

  a {
    padding: 5px 0;
    position: relative;
    color: rgba(255, 255, 255, 0.85);
    font-size: 16px;
    font-weight: 500;
    text-decoration: none;

    &:hover,
    &.active {
      color: white;
    }

    &.active::after {
      content: '';
      position: absolute;
      bottom: -2px;
      left: 0;
      width: 100%;
      height: 2px;
      background-color: white;
    }
  }
}

.search-box {
  width: 240px;

  .search-input {
    :deep(.el-input__inner) {
      border-radius: 4px;
      background-color: rgba(255, 255, 255, 0.2);
      border: none;
      color: white;
      
      &::placeholder {
        color: rgba(255, 255, 255, 0.7);
      }
    }
    
    :deep(.el-input__suffix) {
      color: white;
    }
  }

  .search-icon {
    cursor: pointer;
    color: white;
  }
}

.login-button {
  :deep(.el-button) {
    background-color: white;
    color: #fb7299;
    border: none;
    font-weight: 500;
    
    &:hover {
      background-color: rgba(255, 255, 255, 0.9);
    }
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
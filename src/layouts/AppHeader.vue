<template>
  <header class="app-header">
    <div class="container">
      <div class="header-content">
        <!-- Logo -->
        <div class="logo">
          <router-link to="/">
            <div class="logo-content">
              <svg class="logo-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
              </svg>
              <h1>漫画阅读</h1>
            </div>
          </router-link>
        </div>

        <!-- 导航 -->
        <nav class="nav-menu">
          <router-link to="/" exact-active-class="active">首页</router-link>
          <router-link to="/category" exact-active-class="active">分类</router-link>
          <router-link to="/ranking" exact-active-class="active">排行榜</router-link>
          <router-link to="/latest" exact-active-class="active">最新更新</router-link>
        </nav>

        <!-- 右侧功能区 -->
        <div class="header-actions">
          <!-- 搜索框 -->
          <div class="search-box">
            <el-input 
              v-model="searchKeyword" 
              placeholder="搜索漫画名称或ID" 
              class="search-input" 
              @keyup.enter="handleSearch"
              clearable
            >
              <template #prefix>
                <el-icon class="search-icon" @click="handleSearch">
                  <Search />
                </el-icon>
              </template>
            </el-input>
          </div>

          <!-- 下载按钮 -->
          <div class="action-btn download-btn">
            <el-button type="primary" size="small" @click="showDownloadDialog = true">
              下载
            </el-button>
          </div>

          <!-- 登录按钮 -->
          <div class="action-btn login-button">
            <el-button type="primary" size="small">
              登录
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 下载弹窗 -->
    <el-dialog v-model="showDownloadDialog" title="下载漫画" width="360px" center :show-close="true"
      :close-on-click-modal="false" :close-on-press-escape="true">
      <div class="download-dialog-content">
        <p class="download-tip">输入6位漫画ID，一键下载您喜欢的漫画</p>
        <el-input v-model="comicId" placeholder="请输入6位漫画ID" maxlength="6" show-word-limit clearable
          class="download-input">
          <template #prefix>
            <el-icon>
              <Download />
            </el-icon>
          </template>
        </el-input>
        <div v-if="downloadMessage" class="download-message"
          :class="{ 'success': downloadSuccess, 'error': !downloadSuccess }">
          <el-icon v-if="downloadSuccess">
            <Check />
          </el-icon>
          <el-icon v-else>
            <Warning />
          </el-icon>
          {{ downloadMessage }}
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showDownloadDialog = false">取消</el-button>
          <el-button type="primary" :loading="downloading" @click="downloadComic"
            :disabled="!comicId || comicId.length !== 6">
            下载
          </el-button>
        </span>
      </template>
    </el-dialog>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Search, Download, Check, Warning } from '@element-plus/icons-vue'
import { useTheme } from '@/composables/useTheme'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const router = useRouter()
const searchKeyword = ref('')

// 使用主题组合式函数
const { themeMode, colorTheme } = useTheme()

// 下载漫画相关
const showDownloadDialog = ref(false)
const comicId = ref('')
const downloading = ref(false)
const downloadMessage = ref('')
const downloadSuccess = ref(false)

// 处理搜索
const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    router.push({
      path: '/search',
      query: { keyword: searchKeyword.value.trim() }
    })

    // 搜索后清空搜索框
    setTimeout(() => {
      searchKeyword.value = ''
    }, 300)

    // 记录到控制台，方便调试
    console.log('搜索关键词:', searchKeyword.value.trim())
  } else {
    ElMessage.warning('请输入搜索关键词')
  }
}

// 下载漫画
const downloadComic = async () => {
  if (!comicId.value) {
    ElMessage.warning('请输入漫画ID')
    return
  }

  if (!/^\d{6}$/.test(comicId.value)) {
    ElMessage.warning('漫画ID必须是6位数字')
    downloadSuccess.value = false
    downloadMessage.value = '漫画ID必须是6位数字'
    return
  }

  downloading.value = true
  downloadMessage.value = '正在下载，请稍候...'
  downloadSuccess.value = true

  try {
    const response = await axios.get(`http://localhost:3000/download/${comicId.value}`)
    downloadMessage.value = response.data.message
    downloadSuccess.value = true
    ElMessage.success(response.data.message)

    // 下载完成后关闭弹窗
    setTimeout(() => {
      showDownloadDialog.value = false
      comicId.value = ''
      downloadMessage.value = ''
    }, 3000)
  } catch (error: any) {
    console.error('下载漫画失败', error)
    downloadMessage.value = `下载失败: ${error.response?.data?.detail || error.message}`
    downloadSuccess.value = false
    ElMessage.error(downloadMessage.value)
  } finally {
    downloading.value = false
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
  height: 70px;
  min-height: 70px;
  display: flex;
  align-items: center;
  transition: background-color 0.3s;
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
  height: 100%;
}

.logo {
  margin-right: 40px;

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
  flex: 1;
  height: 100%;
  align-items: center;

  a {
    padding: 8px 0;
    position: relative;
    color: rgba(255, 255, 255, 0.85);
    font-size: 16px;
    font-weight: 500;
    text-decoration: none;
    transition: color 0.2s;
    height: 100%;
    display: flex;
    align-items: center;

    &:hover,
    &.active {
      color: white;
    }

    &.active::after {
      content: '';
      position: absolute;
      bottom: -20px;
      left: 0;
      width: 100%;
      height: 3px;
      background-color: white;
    }
  }
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.search-box {
  width: 240px;

  .search-input {
    :deep(.el-input__wrapper) {
      background-color: white;
      box-shadow: none !important;
      border-radius: 4px;
    }
    
    :deep(.el-input__inner) {
      color: #333 !important;
      background-color: white;
      border: none;
      caret-color: #333;
      -webkit-text-fill-color: #333;
    }

    :deep(.el-input__prefix), 
    :deep(.el-input__prefix-inner),
    :deep(.el-input__suffix), 
    :deep(.el-input__suffix-inner) {
      color: #666;
    }
    
    :deep(.el-input__placeholder) {
      color: #999;
    }
    
    .search-icon {
      cursor: pointer;
      
      &:hover {
        color: #409EFF;
      }
    }
  }
}

.action-btn {
  :deep(.el-button) {
    background-color: white;
    color: #fb7299;
    border: none;
    font-weight: 500;
    border-radius: 4px;
    padding: 0 15px;
    height: 36px;
    transition: all 0.2s;

    &:hover {
      background-color: rgba(255, 255, 255, 0.9);
    }
  }
}

.download-dialog-content {
  padding: 10px 0;

  .download-tip {
    margin-top: 0;
    margin-bottom: 15px;
    color: #606266;
    font-size: 14px;
    text-align: center;
  }

  .download-input {
    margin-bottom: 15px;
  }

  .download-message {
    padding: 10px;
    border-radius: 4px;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 8px;

    &.success {
      background-color: rgba(103, 194, 58, 0.1);
      color: #67c23a;
    }

    &.error {
      background-color: rgba(245, 108, 108, 0.1);
      color: #f56c6c;
    }
  }
}

:deep(.el-dialog) {
  border-radius: 8px;
  overflow: hidden;

  .el-dialog__header {
    margin: 0;
    padding: 15px 20px;
    background-color: #fb7299;
    color: white;
    text-align: center;

    .el-dialog__title {
      color: white;
      font-weight: 600;
      font-size: 18px;
    }

    .el-dialog__close {
      color: white;

      &:hover {
        color: rgba(255, 255, 255, 0.8);
      }
    }
  }

  .el-dialog__body {
    padding: 20px;
  }

  .el-dialog__footer {
    padding: 10px 20px 20px;
    border-top: 1px solid #f0f0f0;
    display: flex;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .nav-menu {
    display: none;
  }

  .search-box {
    width: 160px;

    .search-input {
      :deep(.el-input__inner) {
        height: 32px;
        font-size: 14px;
      }
    }
  }

  .action-btn {
    :deep(.el-button) {
      padding: 0 10px;
      height: 32px;
      font-size: 14px;
    }
  }
}
</style>
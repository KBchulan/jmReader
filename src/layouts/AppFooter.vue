<template>
  <footer class="app-footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-left">
          <div class="footer-logo">
            <svg class="logo-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
              <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
            </svg>
            <h3>漫画阅读</h3>
          </div>
          <p class="footer-desc">您的在线漫画阅读平台，随时随地畅享精彩漫画</p>
          <p class="footer-copyright">© {{ currentYear }} 漫画阅读网站 保留所有权利</p>
        </div>
        <div class="footer-right">
          <div class="footer-section">
            <h4>关于我们</h4>
            <div class="footer-links">
              <router-link to="/about">关于我们</router-link>
              <router-link to="/contact">联系我们</router-link>
              <router-link to="/join">加入我们</router-link>
            </div>
          </div>
          <div class="footer-section">
            <h4>帮助中心</h4>
            <div class="footer-links">
              <router-link to="/faq">常见问题</router-link>
              <router-link to="/terms">使用条款</router-link>
              <router-link to="/privacy">隐私政策</router-link>
            </div>
          </div>
          <div class="footer-section">
            <h4>关注我们</h4>
            <div class="social-links">
              <a href="#" @click.prevent="showSocialModal('weibo')" class="social-link">
                <i class="social-icon weibo"></i>
                微博
              </a>
              <a href="#" @click.prevent="showSocialModal('wechat')" class="social-link">
                <i class="social-icon wechat"></i>
                微信
              </a>
              <a href="#" @click.prevent="showSocialModal('qq')" class="social-link">
                <i class="social-icon qq"></i>
                QQ
              </a>
            </div>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>本站漫画均来自互联网，如有侵权请联系我们删除</p>
      </div>
    </div>
    
    <!-- 社交媒体弹窗 -->
    <el-dialog
      v-model="socialModalVisible"
      :title="socialModalTitle"
      width="300px"
      align-center
    >
      <div class="social-modal-content">
        <div class="qrcode-placeholder">
          <svg xmlns="http://www.w3.org/2000/svg" width="150" height="150" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <path d="M8 7v10"></path>
            <path d="M12 7v10"></path>
            <path d="M16 7v10"></path>
            <path d="M7 8h10"></path>
            <path d="M7 12h10"></path>
            <path d="M7 16h10"></path>
          </svg>
        </div>
        <p>扫描二维码关注我们</p>
      </div>
    </el-dialog>
  </footer>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

// 获取当前年份
const currentYear = computed(() => new Date().getFullYear())

// 社交媒体弹窗
const socialModalVisible = ref(false)
const socialModalTitle = ref('')

// 显示社交媒体弹窗
const showSocialModal = (type: 'weibo' | 'wechat' | 'qq') => {
  socialModalVisible.value = true
  
  switch (type) {
    case 'weibo':
      socialModalTitle.value = '关注我们的微博'
      break
    case 'wechat':
      socialModalTitle.value = '关注我们的微信公众号'
      break
    case 'qq':
      socialModalTitle.value = '加入我们的QQ群'
      break
  }
}
</script>

<style scoped lang="scss">
.app-footer {
  background-color: var(--header-bg-color, white);
  padding: 40px 0 20px;
  margin-top: auto;
  border-top: 1px solid var(--border-color-base, #dcdfe6);
}

.footer-content {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
  
  @media (max-width: 768px) {
    flex-direction: column;
    gap: 30px;
  }
}

.footer-left {
  max-width: 300px;
  
  .footer-logo {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
    
    .logo-icon {
      width: 24px;
      height: 24px;
      stroke: var(--primary-color, #fb7299);
    }
    
    h3 {
      font-size: 1.2rem;
      color: var(--primary-color, #fb7299);
      margin: 0;
      font-weight: 600;
    }
  }
  
  .footer-desc {
    margin: 0 0 12px;
    color: var(--text-color-regular, #606266);
    font-size: 0.9rem;
    line-height: 1.5;
  }
  
  .footer-copyright {
    margin: 0;
    color: var(--text-color-secondary, #909399);
    font-size: 0.85rem;
  }
  
  @media (max-width: 768px) {
    max-width: 100%;
    text-align: center;
    
    .footer-logo {
      justify-content: center;
    }
  }
}

.footer-right {
  display: flex;
  gap: 40px;
  
  @media (max-width: 768px) {
    justify-content: space-around;
    flex-wrap: wrap;
    gap: 20px;
  }
  
  @media (max-width: 576px) {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
}

.footer-section {
  h4 {
    font-size: 1rem;
    color: var(--text-color-primary, #303133);
    margin: 0 0 15px;
    font-weight: 600;
  }
}

.footer-links {
  display: flex;
  flex-direction: column;
  gap: 10px;
  
  a {
    color: var(--text-color-regular, #606266);
    font-size: 0.9rem;
    transition: color 0.2s;
    
    &:hover {
      color: var(--primary-color, #fb7299);
    }
  }
}

.social-links {
  display: flex;
  flex-direction: column;
  gap: 10px;
  
  .social-link {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-color-regular, #606266);
    font-size: 0.9rem;
    transition: color 0.2s;
    
    &:hover {
      color: var(--primary-color, #fb7299);
    }
    
    .social-icon {
      width: 16px;
      height: 16px;
      background-size: contain;
      background-repeat: no-repeat;
      background-position: center;
      
      &.weibo {
        background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cGF0aCBkPSJNMjAgOWMtMS4xIDAtMiAuOS0yIDJhMiAyIDAgMCAwIDIgMmMyLjIgMCA0LTEuOCA0LTRzLTEuOC00LTQtNGMtMy4zIDAtNiAyLjctNiA2djJjMCA0LjQtMy42IDgtOCA4cy04LTMuNi04LTggMy42LTggOC04YzEuMSAwIDIuMi4yIDMuMi42Ii8+PC9zdmc+');
      }
      
      &.wechat {
        background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cGF0aCBkPSJNMTcgMTFhOCA4IDAgMSAwLTkuNjQgNy44MUw1IDIybDMuMzMtMi4zQTggOCAwIDAgMCAxNyAxMXoiLz48L3N2Zz4=');
      }
      
      &.qq {
        background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cGF0aCBkPSJNMTggMTBhOCA4IDAgMSAwLTE2IDBjMCAzLjEgMS43NiA1LjggNC4zMyA3LjE2QzUuNTYgMTguNDUgNSAyMCA1IDIyaDJjMC0xLjM4IDEuMzQtMi41IDMtMi41czMgMS4xMiAzIDIuNWgyYzAtMi0uNTYtMy41NS0xLjMzLTQuODRBNy45OCA3Ljk4IDAgMCAwIDE4IDEweiIvPjwvc3ZnPg==');
      }
    }
  }
}

.footer-bottom {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid var(--border-color-light, #ebeef5);
  
  p {
    margin: 0;
    color: var(--text-color-secondary, #909399);
    font-size: 0.85rem;
  }
}

.social-modal-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  
  .qrcode-placeholder {
    width: 150px;
    height: 150px;
    margin-bottom: 15px;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f5f7fa;
    border-radius: 4px;
    
    svg {
      color: #dcdfe6;
    }
  }
  
  p {
    margin: 0;
    color: var(--text-color-regular, #606266);
    font-size: 14px;
  }
}
</style> 
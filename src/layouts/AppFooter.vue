<template>
  <footer class="app-footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-left">
          <h3>漫画阅读</h3>
          <p>© {{ currentYear }} 漫画阅读网站 保留所有权利</p>
        </div>
        <div class="footer-right">
          <div class="footer-links">
            <a href="#" @click.prevent>关于我们</a>
            <a href="#" @click.prevent>联系我们</a>
            <a href="#" @click.prevent>使用条款</a>
            <a href="#" @click.prevent>隐私政策</a>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { computed } from 'vue'

// 获取当前年份
const currentYear = computed(() => new Date().getFullYear())
</script>

<style scoped lang="scss">
.app-footer {
  background-color: var(--header-bg-color, white);
  padding: 20px 0;
  margin-top: auto;
  border-top: 1px solid var(--border-color-base, #dcdfe6);
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  @media (max-width: 768px) {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
}

.footer-left {
  h3 {
    font-size: 1.2rem;
    color: var(--primary-color, #fb7299);
    margin: 0 0 5px;
  }
  
  p {
    margin: 0;
    color: var(--text-color-secondary, #909399);
    font-size: 0.9rem;
  }
}

.footer-links {
  display: flex;
  gap: 20px;
  
  a {
    color: var(--text-color-regular, #606266);
    font-size: 0.9rem;
    
    &:hover {
      color: var(--primary-color, #fb7299);
    }
  }
  
  @media (max-width: 768px) {
    justify-content: center;
    flex-wrap: wrap;
    gap: 15px;
  }
}
</style> 
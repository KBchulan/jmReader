<template>
  <div class="contact-view">
    <div class="container">
      <div class="page-header">
        <h1>联系我们</h1>
      </div>
      
      <div class="contact-content">
        <div class="contact-info">
          <section class="contact-section">
            <h2>联系方式</h2>
            <div class="info-item">
              <el-icon><Message /></el-icon>
              <div class="info-content">
                <h3>电子邮箱</h3>
                <p>contact@mangareader.com</p>
              </div>
            </div>
            <div class="info-item">
              <el-icon><Location /></el-icon>
              <div class="info-content">
                <h3>办公地址</h3>
                <p>北京市海淀区中关村科技园区</p>
              </div>
            </div>
            <div class="info-item">
              <el-icon><Phone /></el-icon>
              <div class="info-content">
                <h3>联系电话</h3>
                <p>010-12345678</p>
              </div>
            </div>
          </section>
          
          <section class="contact-section">
            <h2>社交媒体</h2>
            <div class="social-links">
              <a href="#" @click.prevent="showSocialModal('weibo')" class="social-link">
                <i class="social-icon weibo"></i>
                <span>官方微博</span>
              </a>
              <a href="#" @click.prevent="showSocialModal('wechat')" class="social-link">
                <i class="social-icon wechat"></i>
                <span>微信公众号</span>
              </a>
              <a href="#" @click.prevent="showSocialModal('qq')" class="social-link">
                <i class="social-icon qq"></i>
                <span>QQ交流群</span>
              </a>
            </div>
          </section>
        </div>
        
        <div class="contact-form">
          <h2>留言反馈</h2>
          <el-form :model="form" label-position="top">
            <el-form-item label="您的姓名">
              <el-input v-model="form.name" placeholder="请输入您的姓名" />
            </el-form-item>
            <el-form-item label="电子邮箱">
              <el-input v-model="form.email" placeholder="请输入您的电子邮箱" />
            </el-form-item>
            <el-form-item label="留言类型">
              <el-select v-model="form.type" placeholder="请选择留言类型" style="width: 100%">
                <el-option label="问题反馈" value="feedback" />
                <el-option label="建议" value="suggestion" />
                <el-option label="合作咨询" value="cooperation" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>
            <el-form-item label="留言内容">
              <el-input
                v-model="form.content"
                type="textarea"
                placeholder="请输入您的留言内容"
                :rows="5"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitForm">提交留言</el-button>
            </el-form-item>
          </el-form>
        </div>
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
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Message, Location, Phone } from '@element-plus/icons-vue'

// 表单数据
const form = ref({
  name: '',
  email: '',
  type: '',
  content: ''
})

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

// 提交表单
const submitForm = () => {
  if (!form.value.name || !form.value.email || !form.value.type || !form.value.content) {
    ElMessage.warning('请填写完整的表单信息')
    return
  }
  
  ElMessage.success('留言提交成功，我们会尽快回复您')
  
  // 重置表单
  form.value = {
    name: '',
    email: '',
    type: '',
    content: ''
  }
}
</script>

<style scoped lang="scss">
.contact-view {
  padding: 40px 0;
}

.page-header {
  margin-bottom: 40px;
  text-align: center;
  
  h1 {
    font-size: 32px;
    color: var(--text-color-primary, #303133);
    margin: 0;
    font-weight: 600;
    position: relative;
    display: inline-block;
    
    &::after {
      content: '';
      position: absolute;
      bottom: -10px;
      left: 50%;
      transform: translateX(-50%);
      width: 60px;
      height: 3px;
      background-color: var(--primary-color, #fb7299);
    }
  }
}

.contact-content {
  max-width: 1000px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.contact-section {
  margin-bottom: 30px;
  
  h2 {
    font-size: 24px;
    color: var(--text-color-primary, #303133);
    margin: 0 0 20px;
    font-weight: 600;
  }
}

.info-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
  
  .el-icon {
    font-size: 24px;
    color: var(--primary-color, #fb7299);
    margin-right: 16px;
    margin-top: 4px;
  }
  
  .info-content {
    h3 {
      font-size: 18px;
      color: var(--text-color-primary, #303133);
      margin: 0 0 8px;
      font-weight: 600;
    }
    
    p {
      font-size: 16px;
      color: var(--text-color-regular, #606266);
      margin: 0;
      line-height: 1.5;
    }
  }
}

.social-links {
  display: flex;
  flex-direction: column;
  gap: 16px;
  
  .social-link {
    display: flex;
    align-items: center;
    gap: 12px;
    color: var(--text-color-regular, #606266);
    font-size: 16px;
    transition: color 0.2s;
    
    &:hover {
      color: var(--primary-color, #fb7299);
    }
    
    .social-icon {
      width: 24px;
      height: 24px;
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

.contact-form {
  background-color: var(--card-bg-color, white);
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  
  h2 {
    font-size: 24px;
    color: var(--text-color-primary, #303133);
    margin: 0 0 20px;
    font-weight: 600;
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
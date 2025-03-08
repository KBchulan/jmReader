<template>
  <div class="faq-view">
    <div class="container">
      <div class="page-header">
        <h1>常见问题</h1>
      </div>
      
      <div class="faq-content">
        <el-collapse accordion>
          <el-collapse-item v-for="(item, index) in faqItems" :key="index" :title="item.question">
            <div class="faq-answer">{{ item.answer }}</div>
          </el-collapse-item>
        </el-collapse>
        
        <div class="contact-section">
          <h2>还有其他问题？</h2>
          <p>如果您有其他问题，欢迎随时与我们联系。</p>
          <router-link to="/contact" class="contact-link">
            <el-button type="primary">联系我们</el-button>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// FAQ数据
const faqItems = ref([
  {
    question: '如何下载漫画？',
    answer: '您可以在首页输入6位漫画ID,点击下载按钮即可下载漫画。下载完成后,您可以在漫画列表中找到您下载的漫画。'
  },
  {
    question: '如何阅读漫画？',
    answer: '点击漫画卡片进入漫画详情页,然后选择您想要阅读的章节即可开始阅读。在阅读页面,您可以通过点击屏幕左右两侧或使用键盘方向键翻页。'
  },
  {
    question: '漫画更新频率是多久？',
    answer: '不同漫画的更新频率不同,一般连载中的漫画会每周或每月更新。您可以在漫画详情页查看最近更新时间。'
  },
  {
    question: '如何查找特定漫画？',
    answer: '您可以使用页面顶部的搜索框搜索漫画名称或ID。此外,您还可以通过分类页面按类型浏览漫画。'
  },
  {
    question: '网站是否支持移动设备？',
    answer: '是的,我们的网站采用响应式设计,可以在各种设备上提供良好的阅读体验,包括手机、平板和电脑。'
  },
  {
    question: '如何收藏喜欢的漫画？',
    answer: '在漫画详情页,点击"收藏"按钮即可将漫画添加到您的收藏列表。您可以在个人中心查看您收藏的漫画。'
  },
  {
    question: '如何调整阅读设置？',
    answer: '在阅读页面,点击屏幕中央弹出阅读设置菜单,您可以调整页面显示模式、背景颜色等设置。'
  },
  {
    question: '漫画内容来源于哪里？',
    answer: '我们的漫画内容来自互联网公开资源,我们尊重原创,如有侵权内容,请联系我们删除。'
  },
  {
    question: '如何报告问题或提出建议？',
    answer: '您可以通过"联系我们"页面填写反馈表单,或发送邮件至18737519552@163.com。我们会认真对待每一条反馈。'
  },
  {
    question: '网站是否收费？',
    answer: '目前我们的网站是完全免费的,您可以免费阅读所有漫画内容。未来可能会推出一些增值服务,但基础阅读功能将保持免费。'
  }
])
</script>

<style scoped lang="scss">
.faq-view {
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

.faq-content {
  max-width: 800px;
  margin: 0 auto;
  
  :deep(.el-collapse) {
    border: none;
    
    .el-collapse-item {
      margin-bottom: 16px;
      border: 1px solid var(--border-color-light, #ebeef5);
      border-radius: 8px;
      overflow: hidden;
      
      &:last-child {
        margin-bottom: 0;
      }
      
      .el-collapse-item__header {
        font-size: 18px;
        font-weight: 600;
        color: var(--text-color-primary, #303133);
        padding: 16px 20px;
        background-color: var(--card-bg-color, white);
        border-bottom: none;
        
        &.is-active {
          color: var(--primary-color, #fb7299);
        }
      }
      
      .el-collapse-item__content {
        padding: 0 20px 20px;
      }
    }
  }
  
  .faq-answer {
    font-size: 16px;
    line-height: 1.8;
    color: var(--text-color-regular, #606266);
  }
}

.contact-section {
  margin-top: 40px;
  text-align: center;
  padding: 30px;
  background-color: var(--card-bg-color, white);
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  
  h2 {
    font-size: 24px;
    color: var(--text-color-primary, #303133);
    margin: 0 0 16px;
    font-weight: 600;
  }
  
  p {
    font-size: 16px;
    color: var(--text-color-regular, #606266);
    margin: 0 0 20px;
  }
  
  .contact-link {
    text-decoration: none;
  }
}

@media (max-width: 768px) {
  .faq-view {
    padding: 30px 0;
  }
  
  .page-header {
    margin-bottom: 30px;
    
    h1 {
      font-size: 28px;
    }
  }
  
  .faq-content {
    :deep(.el-collapse) {
      .el-collapse-item {
        .el-collapse-item__header {
          font-size: 16px;
          padding: 14px 16px;
        }
        
        .el-collapse-item__content {
          padding: 0 16px 16px;
        }
      }
    }
    
    .faq-answer {
      font-size: 15px;
    }
  }
  
  .contact-section {
    margin-top: 30px;
    padding: 24px;
    
    h2 {
      font-size: 22px;
      margin-bottom: 12px;
    }
    
    p {
      font-size: 15px;
      margin-bottom: 16px;
    }
  }
}
</style> 
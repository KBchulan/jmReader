<template>
  <div class="terms-view">
    <div class="container">
      <div class="page-header">
        <h1>使用条款</h1>
      </div>
      
      <div class="terms-content">
        <section class="terms-section">
          <h2>1. 接受条款</h2>
          <p>欢迎使用漫画阅读网站（以下简称"本网站"）。本网站由漫画阅读团队（以下简称"我们"）提供。通过访问或使用本网站，您同意受本使用条款的约束。如果您不同意这些条款，请不要使用本网站。</p>
        </section>
        
        <section class="terms-section">
          <h2>2. 服务描述</h2>
          <p>本网站提供在线漫画阅读服务，允许用户浏览、阅读和下载漫画内容。我们保留随时修改、暂停或终止部分或全部服务的权利，恕不另行通知。</p>
        </section>
        
        <section class="terms-section">
          <h2>3. 用户账户</h2>
          <p>某些功能可能需要您注册账户。您负责维护您账户的保密性，并对发生在您账户下的所有活动负责。您同意立即通知我们任何未经授权使用您账户的情况。</p>
        </section>
        
        <section class="terms-section">
          <h2>4. 用户行为</h2>
          <p>您同意不会：</p>
          <ul>
            <li>违反任何适用的法律法规</li>
            <li>侵犯他人的知识产权或其他权利</li>
            <li>传播有害、威胁、滥用、骚扰、诽谤、淫秽或其他不适当的内容</li>
            <li>干扰或破坏本网站的正常运行</li>
            <li>未经授权访问本网站的系统或网络</li>
            <li>使用自动化程序大量下载内容</li>
          </ul>
        </section>
        
        <section class="terms-section">
          <h2>5. 知识产权</h2>
          <p>本网站上的所有内容，包括但不限于文本、图形、标志、图标、图像、音频剪辑、数字下载和软件，均为本网站或其内容提供商的财产，受国际版权法保护。</p>
          <p>本网站上的漫画内容版权归原作者或出版商所有。我们尊重知识产权，如有侵权内容，请联系我们删除。</p>
        </section>
        
        <section class="terms-section">
          <h2>6. 免责声明</h2>
          <p>本网站按"现状"提供，不提供任何明示或暗示的保证。我们不保证本网站将无错误运行，或者本网站及其服务器不含有病毒或其他有害成分。</p>
          <p>在任何情况下，我们对因使用或无法使用本网站而导致的任何损害（包括但不限于直接、间接、附带、惩罚性和后果性损害）不承担责任。</p>
        </section>
        
        <section class="terms-section">
          <h2>7. 条款修改</h2>
          <p>我们保留随时修改这些条款的权利。修改后的条款将在本网站上发布时立即生效。您继续使用本网站将视为接受修改后的条款。</p>
        </section>
        
        <section class="terms-section">
          <h2>8. 适用法律</h2>
          <p>这些条款受中华人民共和国法律管辖，并按其解释，不考虑法律冲突原则。</p>
        </section>
        
        <section class="terms-section">
          <h2>9. 联系我们</h2>
          <p>如果您对这些条款有任何疑问，请通过以下方式联系我们：</p>
          <p>邮箱: 18737519552@163.com</p>
        </section>

        <div class="terms-footer">
          <p>最后更新日期：{{ currentDate }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

// 获取当前日期
const currentDate = computed(() => {
  const date = new Date()
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
})
</script>

<style scoped lang="scss">
.terms-view {
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

.terms-content {
  max-width: 800px;
  margin: 0 auto;
  background-color: var(--card-bg-color, white);
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  padding: 40px;
}

.terms-section {
  margin-bottom: 30px;
  
  h2 {
    font-size: 22px;
    color: var(--text-color-primary, #303133);
    margin: 0 0 16px;
    font-weight: 600;
  }
  
  p {
    font-size: 16px;
    line-height: 1.8;
    color: var(--text-color-regular, #606266);
    margin: 0 0 16px;
    
    &:last-child {
      margin-bottom: 0;
    }
  }
  
  ul {
    margin: 0 0 16px;
    padding-left: 24px;
    
    li {
      font-size: 16px;
      line-height: 1.8;
      color: var(--text-color-regular, #606266);
      margin-bottom: 8px;
      
      &:last-child {
        margin-bottom: 0;
      }
    }
  }
}

.terms-footer {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid var(--border-color-light, #ebeef5);
  
  p {
    font-size: 14px;
    color: var(--text-color-secondary, #909399);
    margin: 0;
    text-align: right;
  }
}

@media (max-width: 768px) {
  .terms-view {
    padding: 30px 0;
  }
  
  .page-header {
    margin-bottom: 30px;
    
    h1 {
      font-size: 28px;
    }
  }
  
  .terms-content {
    padding: 30px 20px;
  }
  
  .terms-section {
    margin-bottom: 24px;
    
    h2 {
      font-size: 20px;
      margin-bottom: 12px;
    }
    
    p, ul li {
      font-size: 15px;
    }
  }
  
  .terms-footer {
    margin-top: 30px;
  }
}
</style> 
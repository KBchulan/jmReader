<template>
  <div class="privacy-view">
    <div class="container">
      <div class="page-header">
        <h1>隐私政策</h1>
      </div>

      <div class="privacy-content">
        <section class="privacy-section">
          <h2>1. 引言</h2>
          <p>漫画阅读网站（以下简称"我们"或"本网站"）重视您的隐私。本隐私政策说明我们如何收集、使用、披露、处理和保护您在使用我们的服务时提供给我们的信息。</p>
          <p>请在使用本网站前仔细阅读本隐私政策。如果您不同意本隐私政策的任何部分,请不要使用本网站。</p>
        </section>

        <section class="privacy-section">
          <h2>2. 我们收集的信息</h2>
          <p>我们可能会收集以下类型的信息:</p>
          <ul>
            <li><strong>个人信息</strong>:当您注册账户、联系我们或参与我们的活动时,我们可能会收集您的姓名、电子邮件地址、电话号码等个人信息。</li>
            <li><strong>使用数据</strong>:我们自动收集有关您如何使用本网站的信息,包括您访问的页面、点击的链接、阅读的漫画等。</li>
            <li><strong>设备信息</strong>: 我们可能会收集有关您使用的设备的信息,如IP地址、浏览器类型、操作系统等。</li>
            <li><strong>Cookie和类似技术</strong>:我们使用Cookie和类似技术来收集和存储有关您使用本网站的信息。</li>
          </ul>
        </section>

        <section class="privacy-section">
          <h2>3. 我们如何使用您的信息</h2>
          <p>我们可能会将收集到的信息用于以下目的:</p>
          <ul>
            <li>提供、维护和改进我们的服务</li>
            <li>处理和管理您的账户</li>
            <li>响应您的请求和提供客户支持</li>
            <li>向您发送技术通知、更新、安全警报和支持消息</li>
            <li>根据您的兴趣和偏好向您推荐内容</li>
            <li>监控和分析使用趋势和活动</li>
            <li>保护本网站和用户的安全</li>
          </ul>
        </section>

        <section class="privacy-section">
          <h2>4. 信息共享与披露</h2>
          <p>我们不会出售或出租您的个人信息给第三方。但在以下情况下,我们可能会共享您的信息:</p>
          <ul>
            <li><strong>服务提供商</strong>:我们可能会与帮助我们提供服务的第三方服务提供商共享信息,如云存储提供商、支付处理商等。</li>
            <li><strong>法律要求</strong>:如果法律要求或为了保护我们的权利,我们可能会披露您的信息。</li>
            <li><strong>业务转让</strong>:如果我们参与合并、收购或资产出售,您的信息可能会作为交易的一部分被转让。</li>
            <li><strong>征得您的同意</strong>:在征得您的同意的情况下,我们可能会与第三方共享您的信息。</li>
          </ul>
        </section>

        <section class="privacy-section">
          <h2>5. 数据安全</h2>
          <p>我们采取合理的安全措施来保护您的个人信息不被未经授权的访问、使用或披露。但请注意,互联网上的传输方法和电子存储不是100%安全的。</p>
        </section>

        <section class="privacy-section">
          <h2>6. 您的权利</h2>
          <p>根据适用的数据保护法律,您可能拥有以下权利:</p>
          <ul>
            <li>访问您的个人信息</li>
            <li>更正不准确的个人信息</li>
            <li>删除您的个人信息</li>
            <li>限制或反对处理您的个人信息</li>
            <li>数据可携带性</li>
            <li>撤回同意</li>
          </ul>
          <p>如果您想行使这些权利,请通过本政策末尾提供的联系方式与我们联系。</p>
        </section>

        <section class="privacy-section">
          <h2>7. 儿童隐私</h2>
          <p>本网站不面向13岁以下的儿童。我们不会故意收集13岁以下儿童的个人信息。如果您发现我们可能收集了13岁以下儿童的个人信息,请立即联系我们,我们将采取措施删除这些信息。</p>
        </section>

        <section class="privacy-section">
          <h2>8. 隐私政策的变更</h2>
          <p>我们可能会不时更新本隐私政策。更新后的政策将在本网站上发布,并在发布时生效。我们鼓励您定期查看本隐私政策,以了解我们如何保护您的信息。</p>
        </section>

        <section class="privacy-section">
          <h2>9. 联系我们</h2>
          <p>如果您对本隐私政策有任何疑问或意见,请通过以下方式联系我们:</p>
          <p>邮箱:privacy@mangareader.com</p>
        </section>

        <div class="privacy-footer">
          <p>最后更新日期:{{ currentDate }}</p>
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
.privacy-view {
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

.privacy-content {
  max-width: 800px;
  margin: 0 auto;
  background-color: var(--card-bg-color, white);
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  padding: 40px;
}

.privacy-section {
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

      strong {
        font-weight: 600;
        color: var(--text-color-primary, #303133);
      }

      &:last-child {
        margin-bottom: 0;
      }
    }
  }
}

.privacy-footer {
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
  .privacy-view {
    padding: 30px 0;
  }

  .page-header {
    margin-bottom: 30px;

    h1 {
      font-size: 28px;
    }
  }

  .privacy-content {
    padding: 30px 20px;
  }

  .privacy-section {
    margin-bottom: 24px;

    h2 {
      font-size: 20px;
      margin-bottom: 12px;
    }

    p,
    ul li {
      font-size: 15px;
    }
  }

  .privacy-footer {
    margin-top: 30px;
  }
}
</style>
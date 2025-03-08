<template>
  <div class="about-view">
    <div class="container">
      <div class="page-header">
        <h1>关于我们</h1>
      </div>

      <div class="about-content">
        <section class="about-section">
          <h2>我们的故事</h2>
          <p>刚学完vue,做的一个练手的小网站</p>
        </section>

        <section class="about-section">
          <h2>我们的使命</h2>
          <p>搞一个自己看黄漫的地方(大雾)</p>
        </section>

        <section class="about-section">
          <h2>我们的团队</h2>
          <p>好吧，只有一个人</p>
        </section>

        <section class="about-section">
          <h2>联系我们</h2>
          <p>如果您有任何问题、建议或合作意向，欢迎随时与我们联系。</p>
          <p>邮箱: 18737519552@163.com</p>
          <div class="contact-buttons">
            <router-link to="/contact" class="contact-button">
              <el-button type="primary">联系我们</el-button>
            </router-link>
            <router-link to="/join" class="contact-button">
              <el-button>加入我们</el-button>
            </router-link>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 无需额外逻辑
</script>

<style scoped lang="scss">
.about-view {
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

.about-content {
  max-width: 800px;
  margin: 0 auto;
}

.about-section {
  margin-bottom: 40px;

  h2 {
    font-size: 24px;
    color: var(--text-color-primary, #303133);
    margin: 0 0 20px;
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
}

.contact-buttons {
  margin-top: 24px;
  display: flex;
  gap: 16px;

  .contact-button {
    text-decoration: none;
  }
}

@media (max-width: 768px) {
  .about-view {
    padding: 30px 0;
  }

  .page-header {
    margin-bottom: 30px;

    h1 {
      font-size: 28px;
    }
  }

  .about-section {
    margin-bottom: 30px;

    h2 {
      font-size: 22px;
      margin-bottom: 16px;
    }

    p {
      font-size: 15px;
    }
  }
}
</style>
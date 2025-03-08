<template>
  <div class="join-view">
    <div class="container">
      <div class="page-header">
        <h1>加入我们</h1>
      </div>

      <div class="join-content">
        <section class="join-section">
          <h2>为什么选择我们</h2>
          <p>加入漫画阅读网站，您将成为一个充满活力、创新和激情的团队的一员。我们致力于为用户提供最优质的漫画阅读体验，同时也为团队成员提供广阔的发展空间和成长机会。</p>
          <div class="benefits">
            <div class="benefit-item">
              <el-icon>
                <Star />
              </el-icon>
              <div class="benefit-content">
                <h3>有竞争力的薪资</h3>
                <p>我们提供行业内有竞争力的薪资待遇，让您的付出得到应有的回报。</p>
              </div>
            </div>
            <div class="benefit-item">
              <el-icon>
                <Promotion />
              </el-icon>
              <div class="benefit-content">
                <h3>广阔的发展空间</h3>
                <p>扁平化的管理结构，让每个人都有机会展示自己的才华和能力。</p>
              </div>
            </div>
            <div class="benefit-item">
              <el-icon>
                <OfficeBuilding />
              </el-icon>
              <div class="benefit-content">
                <h3>舒适的工作环境</h3>
                <p>现代化的办公环境，免费的零食和饮料，让您在舒适的环境中工作。</p>
              </div>
            </div>
            <div class="benefit-item">
              <el-icon>
                <Opportunity />
              </el-icon>
              <div class="benefit-content">
                <h3>灵活的工作时间</h3>
                <p>我们注重工作与生活的平衡，提供灵活的工作时间和远程工作的机会。</p>
              </div>
            </div>
          </div>
        </section>

        <section class="join-section">
          <h2>当前招聘职位</h2>
          <div class="job-list">
            <div class="job-item">
              <div class="job-header">
                <h3>前端开发工程师</h3>
                <span class="job-location">北京</span>
              </div>
              <div class="job-desc">
                <p>负责公司产品的前端开发工作，包括但不限于PC端、移动端的页面开发和交互实现。</p>
                <div class="job-requirements">
                  <h4>岗位要求：</h4>
                  <ul>
                    <li>熟悉HTML、CSS、JavaScript等前端技术</li>
                    <li>熟悉Vue、React等前端框架</li>
                    <li>有良好的代码风格和编程习惯</li>
                    <li>有良好的团队协作能力和沟通能力</li>
                  </ul>
                </div>
              </div>
              <el-button type="primary" @click="applyJob('前端开发工程师')">申请职位</el-button>
            </div>

            <div class="job-item">
              <div class="job-header">
                <h3>后端开发工程师</h3>
                <span class="job-location">北京</span>
              </div>
              <div class="job-desc">
                <p>负责公司产品的后端开发工作,包括但不限于API设计、数据库设计、性能优化等。</p>
                <div class="job-requirements">
                  <h4>岗位要求：</h4>
                  <ul>
                    <li>熟悉Java、Python、Node.js等后端技术</li>
                    <li>熟悉MySQL、MongoDB等数据库</li>
                    <li>有良好的代码风格和编程习惯</li>
                    <li>有良好的团队协作能力和沟通能力</li>
                  </ul>
                </div>
              </div>
              <el-button type="primary" @click="applyJob('后端开发工程师')">申请职位</el-button>
            </div>

            <div class="job-item">
              <div class="job-header">
                <h3>UI设计师</h3>
                <span class="job-location">北京</span>
              </div>
              <div class="job-desc">
                <p>负责公司产品的UI设计工作，包括但不限于界面设计、交互设计、视觉设计等。</p>
                <div class="job-requirements">
                  <h4>岗位要求：</h4>
                  <ul>
                    <li>熟悉Photoshop、Sketch、Figma等设计工具</li>
                    <li>有良好的审美能力和创意思维</li>
                    <li>了解前端开发流程和技术</li>
                    <li>有良好的团队协作能力和沟通能力</li>
                  </ul>
                </div>
              </div>
              <el-button type="primary" @click="applyJob('UI设计师')">申请职位</el-button>
            </div>
          </div>
        </section>

        <section class="join-section">
          <h2>联系我们</h2>
          <p>如果您对我们的职位感兴趣，或者想了解更多关于我们的信息，欢迎随时与我们联系。</p>
          <p>邮箱：hr@mangareader.com</p>
          <p>电话：010-12345678</p>
        </section>
      </div>
    </div>

    <!-- 申请职位弹窗 -->
    <el-dialog v-model="jobDialogVisible" :title="`申请职位：${selectedJob}`" width="500px">
      <el-form :model="jobForm" label-position="top">
        <el-form-item label="姓名">
          <el-input v-model="jobForm.name" placeholder="请输入您的姓名" />
        </el-form-item>
        <el-form-item label="电子邮箱">
          <el-input v-model="jobForm.email" placeholder="请输入您的电子邮箱" />
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="jobForm.phone" placeholder="请输入您的联系电话" />
        </el-form-item>
        <el-form-item label="个人简介">
          <el-input v-model="jobForm.intro" type="textarea" placeholder="请简单介绍一下您自己" :rows="3" />
        </el-form-item>
        <el-form-item label="上传简历">
          <el-upload action="#" :auto-upload="false" :limit="1" accept=".pdf,.doc,.docx">
            <template #trigger>
              <el-button type="primary">选择文件</el-button>
            </template>
            <template #tip>
              <div class="el-upload__tip">
                请上传PDF或Word格式的简历文件
              </div>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="jobDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitJobApplication">提交申请</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Star, Promotion, OfficeBuilding, Opportunity } from '@element-plus/icons-vue'

// 职位申请相关
const jobDialogVisible = ref(false)
const selectedJob = ref('')
const jobForm = ref({
  name: '',
  email: '',
  phone: '',
  intro: ''
})

// 申请职位
const applyJob = (job: string) => {
  selectedJob.value = job
  jobDialogVisible.value = true
}

// 提交职位申请
const submitJobApplication = () => {
  if (!jobForm.value.name || !jobForm.value.email || !jobForm.value.phone) {
    ElMessage.warning('请填写完整的申请信息')
    return
  }

  ElMessage.success('申请提交成功，我们会尽快与您联系')
  jobDialogVisible.value = false

  // 重置表单
  jobForm.value = {
    name: '',
    email: '',
    phone: '',
    intro: ''
  }
}
</script>

<style scoped lang="scss">
.join-view {
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

.join-content {
  max-width: 800px;
  margin: 0 auto;
}

.join-section {
  margin-bottom: 50px;

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
  }
}

.benefits {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-top: 30px;
}

.benefit-item {
  display: flex;
  align-items: flex-start;
  padding: 20px;
  background-color: var(--card-bg-color, white);
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s, box-shadow 0.3s;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  }

  .el-icon {
    font-size: 24px;
    color: var(--primary-color, #fb7299);
    margin-right: 16px;
    margin-top: 4px;
  }

  .benefit-content {
    h3 {
      font-size: 18px;
      color: var(--text-color-primary, #303133);
      margin: 0 0 8px;
      font-weight: 600;
    }

    p {
      font-size: 14px;
      color: var(--text-color-regular, #606266);
      margin: 0;
      line-height: 1.5;
    }
  }
}

.job-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.job-item {
  padding: 24px;
  background-color: var(--card-bg-color, white);
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);

  .job-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;

    h3 {
      font-size: 20px;
      color: var(--text-color-primary, #303133);
      margin: 0;
      font-weight: 600;
    }

    .job-location {
      font-size: 14px;
      color: var(--text-color-secondary, #909399);
      background-color: #f5f7fa;
      padding: 4px 8px;
      border-radius: 4px;
    }
  }

  .job-desc {
    margin-bottom: 20px;

    p {
      font-size: 16px;
      line-height: 1.6;
      color: var(--text-color-regular, #606266);
      margin: 0 0 16px;
    }

    .job-requirements {
      h4 {
        font-size: 16px;
        color: var(--text-color-primary, #303133);
        margin: 0 0 12px;
        font-weight: 600;
      }

      ul {
        margin: 0;
        padding-left: 20px;

        li {
          font-size: 14px;
          color: var(--text-color-regular, #606266);
          margin-bottom: 8px;
          line-height: 1.5;

          &:last-child {
            margin-bottom: 0;
          }
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .join-view {
    padding: 30px 0;
  }

  .page-header {
    margin-bottom: 30px;

    h1 {
      font-size: 28px;
    }
  }

  .join-section {
    margin-bottom: 40px;

    h2 {
      font-size: 22px;
      margin-bottom: 16px;
    }

    p {
      font-size: 15px;
    }
  }

  .benefits {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .job-item {
    padding: 20px;

    .job-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 8px;
    }
  }
}
</style>
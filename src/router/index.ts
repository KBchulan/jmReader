import { createRouter, createWebHistory } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: DefaultLayout,
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/views/home/HomeView.vue'),
          meta: {
            title: '首页'
          }
        },
        {
          path: 'search',
          name: 'search',
          component: () => import('@/views/search/SearchView.vue'),
          meta: {
            title: '搜索'
          }
        },
        {
          path: 'comic/:id',
          name: 'comic-detail',
          component: () => import('@/views/comic/ComicDetail.vue'),
          meta: {
            title: '漫画详情'
          }
        },
        {
          path: 'reader/:id',
          name: 'reader',
          component: () => import('@/views/reader/ReaderView.vue'),
          meta: {
            title: '阅读'
          }
        },
        {
          path: 'category',
          name: 'category',
          component: () => import('@/views/category/CategoryView.vue'),
          meta: {
            title: '分类'
          }
        },
        {
          path: 'ranking',
          name: 'ranking',
          component: () => import('@/views/ranking/RankingView.vue'),
          meta: {
            title: '排行榜'
          }
        },
        {
          path: 'latest',
          name: 'latest',
          component: () => import('@/views/latest/LatestView.vue'),
          meta: {
            title: '最新更新'
          }
        },
        {
          path: 'about',
          name: 'about',
          component: () => import('@/views/about/AboutView.vue'),
          meta: {
            title: '关于我们'
          }
        },
        {
          path: 'contact',
          name: 'contact',
          component: () => import('@/views/about/ContactView.vue'),
          meta: {
            title: '联系我们'
          }
        },
        {
          path: 'join',
          name: 'join',
          component: () => import('@/views/about/JoinView.vue'),
          meta: {
            title: '加入我们'
          }
        },
        {
          path: 'faq',
          name: 'faq',
          component: () => import('@/views/about/FaqView.vue'),
          meta: {
            title: '常见问题'
          }
        },
        {
          path: 'terms',
          name: 'terms',
          component: () => import('@/views/about/TermsView.vue'),
          meta: {
            title: '使用条款'
          }
        },
        {
          path: 'privacy',
          name: 'privacy',
          component: () => import('@/views/about/PrivacyView.vue'),
          meta: {
            title: '隐私政策'
          }
        }
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFound.vue'),
      meta: {
        title: '页面不存在'
      }
    }
  ]
})

// 路由前置守卫，设置页面标题
router.beforeEach((to, from, next) => {
  // 设置页面标题
  const appTitle = import.meta.env.VITE_APP_TITLE || '漫画阅读'
  document.title = to.meta.title
    ? `${to.meta.title} - ${appTitle}`
    : appTitle

  next()
})

export default router

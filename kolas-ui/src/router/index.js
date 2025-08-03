import { createRouter, createWebHistory } from 'vue-router'

// 导入组件
import HelloWorld from '../components/HelloWorld.vue'
import ProjectManagement from '../components/ProjectManagement.vue'
import DeployToHost from '../components/DeployToHost.vue'
import SettingsPage from '../components/SettingsPage.vue'

// 定义路由规则
const routes = [
  {
    path: '/',
    name: 'Home',
    component: HelloWorld
  },
  {
    path: '/project-management',
    name: 'ProjectManagement',
    component: ProjectManagement
  },
  {
    path: '/deploy-to-host',
    name: 'DeployToHost',
    component: DeployToHost
  },
  {
    path: '/settings',
    name: 'Settings',
    component: SettingsPage
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
import { createRouter, createWebHistory } from 'vue-router'

// 导入组件
import HelloWorld from '../components/HelloWorld.vue'
import ProjectManagement from '../components/ProjectManagement.vue'
import SettingsPage from '../components/SettingsPage.vue'
import ProjectDetail from '../components/ProjectDetail.vue'
import DeployByJar from '../components/DeployByJar.vue'
import TaskDetail from '../components/TaskDetail.vue'
import ServerList from '../components/ServerList.vue'

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
    path: '/settings',
  name: 'Settings',
  component: SettingsPage
},
{
  path: '/deploy-by-jar',
  name: 'DeployByJar',
  component: DeployByJar
},
  { path: '/project-detail/:id/host', name: 'ProjectDetailHost', component: ProjectDetail },
  { path: '/project-detail/:id', name: 'ProjectDetail', component: ProjectDetail },
  { path: '/task-detail/:name', name: 'TaskDetail', component: TaskDetail },
  { path: '/servers', name: 'ServerList', component: ServerList }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
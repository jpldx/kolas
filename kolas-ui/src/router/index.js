import { createRouter, createWebHistory } from 'vue-router'

// 导入组件
import HelloWorld from '../components/HelloWorld.vue'
import ProjectList from '../components/ProjectList.vue'
import SettingsPage from '../components/SettingsPage.vue'
import ProjectDetail from '../components/ProjectDetail.vue'
import DeployByJar from '../components/DeployByJar.vue'
import TaskDetail from '../components/TaskDetail.vue'
import HostList from '../components/HostList.vue'
import HostDetail from '../components/HostDetail.vue'

// 定义路由规则
const routes = [
  {
    path: '/',
    name: 'Home',
    component: HelloWorld
  },
  {
    path: '/project',
    name: 'ProjectList',
    component: ProjectList
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
  { 
    path: '/project-detail/:id', 
    name: 'ProjectDetail', 
    component: ProjectDetail,
    children: [
        { 
          path: 'host', 
          name: 'HostList', 
          component: HostList 
        }
    ]
  },
  { 
    path: '/task-detail/:name', 
    name: 'TaskDetail', 
    component: TaskDetail 
  },
  { 
    path: '/host-detail/:id', 
    name: 'HostDetail', 
    component: HostDetail }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
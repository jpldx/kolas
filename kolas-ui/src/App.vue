<template>
  <div id="app">
    <div class="app-container">
      <!-- 侧边栏菜单 -->
      <aside class="sidebar">
        <div class="sidebar-header">
          <img src="./assets/logo.png" alt="Kolas Logo" class="logo">
          <h1 class="project-name">kolas</h1>
        </div>
        <Menu mode="vertical" theme="light" width="240px" :active-name="activeMenu" @on-select="handleMenuSelect">
          <MenuItem name="home" icon="ios-home">首页</MenuItem>
          <MenuItem name="projectManagement" icon="ios-bar-chart">项目管理</MenuItem>
          <MenuItem name="deployToHost" icon="ios-cloud-upload">Deploy to Host</MenuItem>
          <MenuItem name="settings" icon="ios-cog">系统设置</MenuItem>
        </Menu>
      </aside>

      <!-- 主内容区域 -->
      <main class="main-content">
        <AppBreadcrumb :activeMenu="activeMenu"/>
        <div class="content-wrapper">
          <router-view/>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import AppBreadcrumb from './components/Breadcrumb.vue'
import { Menu, MenuItem } from 'view-ui-plus'
import { onMounted, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

export default {
  name: 'App',
  components: {
    AppBreadcrumb,
    Menu,
    MenuItem
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const activeMenu = ref('home')

    // 处理菜单选择
    const handleMenuSelect = (name) => {
      activeMenu.value = name
      switch(name) {
        case 'home':
          router.push('/')
          break
        case 'projectManagement':
          router.push('/project-management')
          break
        case 'deployToHost':
          router.push('/deploy-to-host')
          break
        case 'settings':
          router.push('/settings')
          break
      }
    }

    // 监听路由变化，更新活动菜单
    watch(route, (newRoute) => {
      switch(newRoute.path) {
        case '/':
          activeMenu.value = 'home'
          break
        case '/project-management':
          activeMenu.value = 'projectManagement'
          break
        case '/deploy-to-host':
          activeMenu.value = 'deployToHost'
          break
        case '/settings':
          activeMenu.value = 'settings'
          break
      }
    })

    // 初始加载时设置活动菜单
    onMounted(() => {
      switch(route.path) {
        case '/':
          activeMenu.value = 'home'
          break
        case '/project-management':
          activeMenu.value = 'projectManagement'
          break
        case '/deploy-to-host':
          activeMenu.value = 'deployToHost'
          break
        case '/settings':
          activeMenu.value = 'settings'
          break
      }
    })

    return {
      activeMenu,
      handleMenuSelect
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100vh;
  overflow: hidden;
}

.app-container {
  display: flex;
  height: 100%;
}

.sidebar {
  background-color: #ffffff;
  height: 100%;
  border-right: 1px solid #e8e8e8;
}

.sidebar-header {
  display: flex;
  align-items: center;
  padding: 20px 15px;
  border-bottom: 1px solid #e8e8e8;
}

.logo {
  width: 40px;
  height: 40px;
  margin-right: 10px;
}

.project-name {
  font-size: 18px;
  font-weight: bold;
  color: #1890ff;
  margin: 0;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  text-align: center;
}

.content-wrapper {
  padding: 20px;
  margin-top: 40px;
}
</style>

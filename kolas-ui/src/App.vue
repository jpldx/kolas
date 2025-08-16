<template>
  <div id="app">
    <div class="app-container">
      <!-- 侧边栏菜单 -->
      <aside class="sidebar">
        <div class="sidebar-header">
          <img src="/img/logo.png" alt="Kolas Logo" class="logo">
          <h1 class="project-name">Kolas</h1>
        </div>
        <Menu mode="vertical" theme="light" width="240px" :active-name="activeMenu" @on-select="handleMenuSelect" :open-names="['operation2']">
          <template v-if="$route.path.includes('/project-detail/')">
            <MenuItem name="backToHome" icon="ios-arrow-back">返回主页面</MenuItem>
            <MenuItem name="operation1" icon="ios-list">项目操作1</MenuItem>
            <Submenu name="operation2" icon="ios-rocket">
              <template #title>
                Deploy
              </template>
              <MenuItem name="deployToA">
                <Icon type="ios-archive"/>Deploy by JAR
              </MenuItem>
              <MenuItem name="deployToB" icon="ios-server">Deploy to B</MenuItem>
              <MenuItem name="deployToC" icon="ios-globe">Deploy to C</MenuItem>
            </Submenu>
            <MenuItem name="host" icon="ios-desktop">主机管理
            </MenuItem>
          </template>
          <template v-else>
            <MenuItem name="home">
              <Icon type="ios-home" size="16px"/>
              首页
            </MenuItem>
            <MenuItem name="project">
               <Icon type="md-apps" size="16px"/>
              项目管理
            </MenuItem>
            <MenuItem name="settings">
               <Icon type="md-settings" size="16px"/>
              系统设置
            </MenuItem>
          </template>
        </Menu>
      </aside>

      <!-- 主内容区域 -->
      <main class="main-content">
        <AppBreadcrumb :activeMenu="activeMenu"/>
        <div class="content-wrapper">
          <router-view>
          </router-view>/>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import AppBreadcrumb from './components/Breadcrumb.vue'
import { Menu, MenuItem, Submenu, Icon } from 'view-ui-plus'
import { onMounted, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

export default {
  name: 'App',
  components: {
    AppBreadcrumb,
    Menu,
    MenuItem,
    Submenu,
    Icon
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
          case 'project':
            router.push('/project')
            break
          case 'settings':
            router.push('/settings')
            break
          case 'backToHome':
            router.push('/')
            break
          case 'deployToA':
            router.push('/deploy-by-jar');
            break;
          case 'deployToB':
            router.push('/deploy-to-b');
            break;
          case 'deployToC':
            router.push('/deploy-to-c');
            break;
          case 'host': {
            // 获取当前项目ID并跳转到host页面
            const projectId = route.params.id;
            // const projectId = route.path.split('/')[2];
            if (projectId) {
              // router.push({ name: 'HostList', params: { id: projectId } });
              router.push(`/project-detail/${projectId}/host`);
            } else {
              // 如果没有项目ID，默认跳转到项目列表
              router.push('/project');
            }
            break;
          }
        }
    }

    // 监听路由变化，更新活动菜单
    watch(route, (newRoute) => {
      if (newRoute.path.includes('/project-detail/')) {
        if (newRoute.path.includes('/host')) {
          activeMenu.value = 'host'; // 高亮主机管理菜单
        } else {
          activeMenu.value = 'operation1';
        }
      } else {
        switch(newRoute.path) {
          case '/':
            activeMenu.value = 'home'
            break
          case '/project':
            activeMenu.value = 'project'
            break
          case '/settings':
            activeMenu.value = 'settings'
            break
        }
      }
    })

    // 初始加载时设置活动菜单
    onMounted(() => {
      switch(route.path) {
        case '/':
          activeMenu.value = 'home'
          break
        case '/project':
          activeMenu.value = 'project'
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

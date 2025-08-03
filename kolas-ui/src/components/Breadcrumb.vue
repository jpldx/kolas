<template>
  <div class="breadcrumb-container">
    <iBreadcrumb separator="/">
      <iBreadcrumbItem @click="handleBreadcrumbClick('home')">
        首页
      </iBreadcrumbItem>
      <iBreadcrumbItem v-if="activeMenu !== 'home'" @click="handleBreadcrumbClick(activeMenu)">
        {{ menuNames[activeMenu] || activeMenu }}
      </iBreadcrumbItem>
    </iBreadcrumb>
  </div>
</template>

<script>
import { Breadcrumb as iBreadcrumb, BreadcrumbItem as iBreadcrumbItem } from 'view-ui-plus'

export default {
  name: 'AppBreadcrumb',
  components: {
    iBreadcrumb,
    iBreadcrumbItem
  },
  props: {
    activeMenu: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      menuNames: {
        'projectManagement': '项目管理',
        'deployToHost': 'Deploy to Host',
        'settings': '系统设置'
      }
    }
  },
  methods: {
    handleBreadcrumbClick(menuName) {
      this.$emit('breadcrumb-click', menuName)
    }
  }
}
</script>

<style scoped>
.breadcrumb-container {
  padding: 30px 20px;
  background-color: #ffffff;
  border-bottom: 1px solid #e8e8e8;
  text-align: left;
  position: fixed;
  top: 0;
  left: 240px;
  right: 0;
  z-index: 100;
}
</style>
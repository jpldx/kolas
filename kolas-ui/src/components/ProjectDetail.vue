<template>
  <div class="project-detail-container">
    <div class="main-content">
      <h2 v-if="!isHostPage">{{ project.name }} 详情</h2>
      <!-- <h2 v-else>主机列表</h2> -->

      <!-- 项目详情内容 -->
      <div v-if="!isHostPage" class="project-info-card">
        <img :src="project.image" alt="Project Image" class="detail-image">
        <div class="info-content">
          <p><strong>项目名称:</strong> {{ project.name }}</p>
          <p><strong>项目描述:</strong> {{ project.description }}</p>
          <p><strong>项目状态:</strong> <span :class="'status-tag ' + project.status">{{ project.statusText }}</span></p>
        </div>
      </div>


    </div>
  </div>
</template>

<script>
  import { Modal } from 'view-ui-plus';
  
  export default {
    name: 'ProjectDetail',
    components: {
    // eslint-disable-next-line vue/no-unused-components
      Modal
      // FormItem: Form.Item,
      // Option: Select.Option,
  },
  data() {
    return {
      project: {},

    };
  },

  created() {
    const projectId = this.$route.params.id;
    this.loadProjectData(projectId);
  },
  methods: {
    loadProjectData(projectId) {
      // 实际应用中应该通过API获取
      // 这里使用从ProjectManagement组件传递的模拟数据
      const projects = [
        { id: 0, name: '项目 1', description: '这是项目 1 的描述', image: 'https://picsum.photos/300/200?random=1', status: 'success', statusText: '进行中' },
        { id: 1, name: '项目 2', description: '这是项目 2 的描述', image: 'https://picsum.photos/300/200?random=2', status: 'warning', statusText: '待审核' },
        { id: 2, name: '项目 3', description: '这是项目 3 的描述', image: 'https://picsum.photos/300/200?random=3', status: 'success', statusText: '进行中' },
        // 添加其他项目...
      ];
      this.project = projects[projectId] || { name: '未知项目', description: '项目数据不存在' };
    },

  }
};
</script>

<style scoped>
.project-detail-container {
  min-height: calc(100vh - 60px);
}

.main-content {
  padding: 20px;
  background-color: #f5f5f5;
}

.project-info-card {
  background: #fff;
  border-radius: 4px;
  padding: 20px;
  display: flex;
  gap: 20px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}

.detail-image {
  width: 200px;
  height: 150px;
  object-fit: cover;
  border-radius: 4px;
}

.info-content {
  flex: 1;
}

.status-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  color: white;
}

.success { background-color: #52c41a; }
.warning { background-color: #faad14; }
.error { background-color: #f5222d; }
.info { background-color: #1890ff; }

/* 主机列表样式 */
.server-list-container {
  background: #fff;
  border-radius: 4px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}

.ivu-table {
  width: 100%;
}

.ivu-table th {
  background-color: #f5f5f5;
}

.table-actions {
  margin-bottom: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.server-title {
  font-size: 18px;
  font-weight: 600;
  font-family: 'Helvetica Neue', Arial, sans-serif;
}

.ivu-modal-body {
  padding: 20px;
}

.ivu-form-item {
  margin-bottom: 15px;
}
</style>
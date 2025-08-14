<template>
  <div class="project">
    <div style="display: flex; margin-bottom: 16px; margin-top: 16px; margin-right: 10px;">
      <Input placeholder="搜索项目..." style="width: 300px;" />
      <Button type="default" icon="ios-search"></Button>
      <Button type="primary" @click="handleAddProject" icon="md-add"></Button>
    </div>
    <Row :gutter="16">
      <!-- 调整后的卡片布局 -->
      <Col span="6" v-for="(project, index) in projects" :key="index">
        <div class="spd-card" @click="handleProjectClick(index)">
          <!-- 顶部状态条 -->
          <div class="spd-card-header">
            <span class="spd-card-title">
              <img :src="project.image" alt="Project Logo" class="project-logo">
              {{ project.name }}
            </span>
            <!-- <span class="spd-card-status" :class="project.status">
              
            </span> -->
            <Tag color="success">
              {{ project.statusText }}
            </Tag>
          </div>
          
          <!-- 项目图片区域 -->
          <div class="spd-card-image-container">
            <span class="spd-card-description">{{ project.description }}</span>
            <!-- <img :src="project.image" alt="Project Image" class="spd-card-image"> -->
          </div>
          
          <!-- 描述与辅助信息 -->
          <div class="spd-card-body">
            <div class="spd-card-meta">
              <span class="spd-tag">SPD</span>
              <span class="spd-time">2024-09-09 11:49:11</span>
            </div>
          </div>
        </div>
      </Col>
    </Row>
  </div>
  
  <!-- 新增项目弹窗保持不变 -->
  <Modal
    v-model="showAddProjectModal"
    title="新增项目"
    ok-text="保存"
    cancel-text="取消"
    @on-ok="handleSaveProject"
    @on-cancel="handleCancelAdd"
  >
    <Form ref="projectForm" :model="newProject" :rules="formRules">
      <FormItem label="项目图标">
        <div class="project-icon-preview">
          <img :src="newProject.image" alt="项目图标预览" class="preview-image">
          <Button type="primary" size="small" @click="handleChangeImage">更换图标</Button>
        </div>
      </FormItem>
      <FormItem label="项目名称" prop="name">
        <Input v-model="newProject.name" placeholder="请输入项目名称" />
      </FormItem>
    </Form>
  </Modal>
</template>

<script>
// JavaScript 部分保持不变
import axios from 'axios';
import { Row, Col, Button, Modal, Form, Input, Message, Tag} from 'view-ui-plus'
export default {
  name: 'ProjectList',
  components: {
    Row,
    Col,
    // Card,
    Tag,
    Button,
    Modal,
    Form,
    Input
  },
  methods: {
    handleAddProject() {
      this.showAddProjectModal = true;
    },
    handleSaveProject() {
      this.$refs.projectForm.validate(valid => {
        if (valid) {
          axios.post('/api/projects', this.newProject)
            .then(response => {
              Message.success('项目保存成功');
              this.projects.push({
                ...response.data,
                description: '这是新项目的描述',
                status: 'success',
                statusText: '进行中'
              });
              this.showAddProjectModal = false;
              this.newProject = {
                name: '',
                image: 'https://picsum.photos/300/200?random=100'
              };
              this.$refs.projectForm.resetFields();
            })
            .catch(error => {
              Message.error('保存失败: ' + (error.response?.data?.message || error.message));
            });
        }
      });
    },
    handleCancelAdd() {
      this.showAddProjectModal = false;
      this.$refs.projectForm.resetFields();
    },
    handleChangeImage() {
      const randomNum = Math.floor(Math.random() * 1000);
      this.newProject.image = `https://picsum.photos/300/200?random=${randomNum}`;
    },
    handleProjectClick(index) {
      this.$router.push({ name: 'ProjectDetail', params: { id: index } });
    }
  },
  data() {
    return {
      projects: [
        {
          name: '项目 1',
          description: '这是项目 1 的描述',
          image: 'https://picsum.photos/300/200?random=1',
          status: 'success',
          statusText: '进行中'
        },
        // 其他项目数据保持不变...
        {
          name: '项目 16',
          description: '这是项目 16 的描述',
          image: 'https://picsum.photos/300/200?random=16',
          status: 'error',
          statusText: '已暂停'
        }
      ],
      showAddProjectModal: false,
      newProject: {
        name: '',
        image: 'https://picsum.photos/300/200?random=100',
      },
      formRules: {
        name: [
          { required: true, message: '请输入项目名称', trigger: 'blur' }
        ]
      }
    }
  }
}
</script>

<style scoped>
/* 移除原有 Card 样式，替换为新样式 */
.spd-card {
  border: 1px solid #e8e8e8;
  border-radius: 6px;
  overflow: hidden;
  transition: all 0.3s ease;
  background-color: #fff;
}

.spd-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 头部标题与状态 */
.spd-card-header {
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.spd-card-title {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  display: flex;
  align-items: center;
}

.project-logo {
  width: 32px;
  height: 32px;
  border-radius: 4px;
  margin-right: 8px;
  object-fit: cover;
}

/* 状态标签样式 */
.spd-card-status {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  color: white;
}

.success {
  background-color: #52c41a;
}

.warning {
  background-color: #faad14;
}

.error {
  background-color: #f5222d;
}

.info {
  background-color: #1890ff;
}

/* 图片区域 */
.spd-card-image-container {
  width: 100%;
  height: 65px;
  overflow: hidden;
  padding: 16px;
}

.spd-card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.spd-card:hover .spd-card-image {
  transform: scale(1.05);
}

/* 内容区域 */
.spd-card-body {
  padding: 16px;
}

.spd-card-description {
  font-size: 14px;
  color: #666;
  /* margin-bottom: 12px; */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  /* -webkit-box-orient: vertical; */
  overflow: hidden;
}

/* 底部元信息 */
.spd-card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #999;
}

.spd-tag {
  padding: 2px 6px;
  background-color: #f5f5f5;
  border-radius: 4px;
  color: #1890ff;
}

.spd-time {
  color: #999;
}

/* 原有弹窗样式保持不变 */
.project-icon-preview {
  display: flex;
  align-items: center;
  gap: 16px;
}

.preview-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 4px;
}

.project {
  padding: 20px;
}
</style>
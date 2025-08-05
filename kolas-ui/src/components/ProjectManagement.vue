<template>
  <div class="project-management">
    <!-- <h2>项目管理</h2> -->
    <div style="display: flex; justify-content: flex-end; margin-bottom: 16px;">
      <Button type="primary" @click="handleAddProject">新增</Button>
    </div>
    <Row :gutter="16">
      <Col span="6" v-for="(project, index) in projects" :key="index">
        <Card :bordered="true" class="project-card">
          <img :src="project.image" alt="Project Image" class="project-image">
          <div class="project-info">
            <h3>{{ project.name }}</h3>
            <p>{{ project.description }}</p>
            <div class="project-status" :class="project.status">
              {{ project.statusText }}
            </div>
          </div>
        </Card>
      </Col>
    </Row>
  </div>

  <!-- 新增项目弹窗 -->
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
import axios from 'axios';
import { Row, Col, Card, Button, Modal, Form, Input, Message } from 'view-ui-plus'

export default {
  name: 'ProjectManagement',
  components: {
    Row,
    Col,
    Card,
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
      // 这里只是简单地生成一个随机图标
      // 实际应用中可能需要调用文件上传API
      const randomNum = Math.floor(Math.random() * 1000);
      this.newProject.image = `https://picsum.photos/300/200?random=${randomNum}`;
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
          {
            name: '项目 2',
            description: '这是项目 2 的描述',
            image: 'https://picsum.photos/300/200?random=2',
            status: 'warning',
            statusText: '待审核'
          },
          {
            name: '项目 3',
            description: '这是项目 3 的描述',
            image: 'https://picsum.photos/300/200?random=3',
            status: 'success',
            statusText: '进行中'
          },
          {
            name: '项目 4',
            description: '这是项目 4 的描述',
            image: 'https://picsum.photos/300/200?random=4',
            status: 'error',
            statusText: '已暂停'
          },
          {
            name: '项目 5',
            description: '这是项目 5 的描述',
            image: 'https://picsum.photos/300/200?random=5',
            status: 'success',
            statusText: '进行中'
          },
          {
            name: '项目 6',
            description: '这是项目 6 的描述',
            image: 'https://picsum.photos/300/200?random=6',
            status: 'success',
            statusText: '进行中'
          },
          {
            name: '项目 7',
            description: '这是项目 7 的描述',
            image: 'https://picsum.photos/300/200?random=7',
            status: 'info',
            statusText: '已完成'
          },
          {
            name: '项目 8',
            description: '这是项目 8 的描述',
            image: 'https://picsum.photos/300/200?random=8',
            status: 'warning',
            statusText: '待审核'
          },
          {
            name: '项目 9',
            description: '这是项目 9 的描述',
            image: 'https://picsum.photos/300/200?random=9',
            status: 'success',
            statusText: '进行中'
          },
          {
            name: '项目 10',
            description: '这是项目 10 的描述',
            image: 'https://picsum.photos/300/200?random=10',
            status: 'error',
            statusText: '已暂停'
          },
          {
            name: '项目 11',
            description: '这是项目 11 的描述',
            image: 'https://picsum.photos/300/200?random=11',
            status: 'info',
            statusText: '已完成'
          },
          {
            name: '项目 12',
            description: '这是项目 12 的描述',
            image: 'https://picsum.photos/300/200?random=12',
            status: 'success',
            statusText: '进行中'
          },
          {
            name: '项目 13',
            description: '这是项目 13 的描述',
            image: 'https://picsum.photos/300/200?random=13',
            status: 'warning',
            statusText: '待审核'
          },
          {
            name: '项目 14',
            description: '这是项目 14 的描述',
            image: 'https://picsum.photos/300/200?random=14',
            status: 'info',
            statusText: '已完成'
          },
          {
            name: '项目 15',
            description: '这是项目 15 的描述',
            image: 'https://picsum.photos/300/200?random=15',
            status: 'success',
            statusText: '进行中'
          },
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
        image: 'https://picsum.photos/300/200?random=100', // 默认图标
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

/* 其他现有样式 */
.project-management {
  padding: 20px;
}

.project-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.project-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 4px;
}

.project-info {
  padding: 16px 0;
}

.project-info h3 {
  margin-top: 10px;
  margin-bottom: 8px;
  font-size: 16px;
}

.project-info p {
  color: #666;
  font-size: 14px;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-status {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
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
</style>
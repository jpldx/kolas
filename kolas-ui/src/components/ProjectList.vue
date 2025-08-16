<template>
  <div class="project">
    <div style="display: flex; margin-bottom: 16px; margin-top: 16px; margin-right: 10px;">
      <Input placeholder="搜索项目..." style="width: 300px;" />
      <Button type="default" icon="ios-search"></Button>
      <Button type="primary" @click="handleAddProject" icon="md-add"></Button>
    </div>
    <Row :gutter="16">
      <!-- 调整后的卡片布局 -->
      <Col span="6" v-for="(project, index) in projects" :key="project.id || index">
        <div class="spd-card" @click="handleProjectClick(project.id)">
          <!-- 顶部状态条 -->
          <div class="spd-card-header">
            <span class="spd-card-title">
              <img :src="previewImageUrl(project.icon_name)" alt="Project Logo" class="project-logo">
              {{ project.name }}
            </span>
            <!-- <span class="spd-card-status" :class="project.status">
              
            </span> -->
            <Tag :color="project.status === 1 ? 'success' : '#BDBDBD'">
              {{ project.status === 1 ? '使用中' : '已下线' }}
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
              <span class="spd-tag">admin</span>
              <span class="spd-time">{{ project.create_time }}</span>
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
      <FormItem label="图标">
        <Upload
            :before-upload="handleBeforeUpload"
            :show-upload-list="false"
            action=""
          >
            <div class="project-icon-preview">
              <template v-if="imageUploaded">
                <img :src="newProject.image" alt="项目图标预览" class="preview-image">
              </template>
              <template v-else>
                <div class="upload-icon-container">
                  <Icon type="ios-cloud-upload" size="48" class="upload-icon" />
                  <span class="upload-text">点击上传图标</span>
                </div>
              </template>
            </div>
        </Upload>
      </FormItem>
      <FormItem label="名称" prop="name">
        <Input v-model="newProject.name" placeholder="请输入名称" />
      </FormItem>
       <FormItem label="描述" prop="description">
        <Input v-model="newProject.description" placeholder="请输入描述" />
      </FormItem>
    </Form>
  </Modal>
</template>

<script>
/* eslint-disable */
// JavaScript 部分保持不变
import axios from 'axios';
import { Row, Col, Button, Modal, Form, Input, Message, Tag, Upload, Icon } from 'view-ui-plus'
import { list as getProjectList, save as saveProject } from '@/api/project'
import { uploadIcon } from '@/api/file'
import service from '@/utils/axios'
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
    Input,
    Upload
  },
  methods: {
    handleAddProject() {
      this.showAddProjectModal = true;
    },
    handleSaveProject() {
      this.$refs.projectForm.validate(valid => {
        if (valid) {
          saveProject(this.newProject)
            .then(response => {
              Message.success('项目保存成功');
              this.fetchProjects(); // 保存成功后重新获取项目列表
              this.showAddProjectModal = false;
              this.newProject = {
                name: '',
                description: '',
                icon_name: '',
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
      this.imageUploaded = false
      this.$refs.projectForm.resetFields();
    },
    handleChangeImage() {
      const randomNum = Math.floor(Math.random() * 1000);
      this.newProject.image = `https://picsum.photos/300/200?random=${randomNum}`;
    },
    handleProjectClick(id) {
      this.$router.push({ name: 'ProjectDetail', params: { id } });
    },
    // handleBeforeUpload(file) {
    //   const reader = new FileReader();
    //   reader.onload = (e) => {
    //     this.newProject.image = e.target.result;
    //   };
    //   reader.readAsDataURL(file);
    //   return false; // 阻止默认上传行为
    // },
    handleBeforeUpload(file) {
      // 调用文件上传接口
      uploadIcon(file)
        .then(res => {
          Message.success('图片上传成功');
          // 将图片转换为base64直接渲染
          const reader = new FileReader();
          reader.onload = (e) => {
            this.newProject.image = e.target.result;
            this.imageUploaded = true;
          };
          reader.readAsDataURL(file);
          // this.newProject.image = res.data.url; // 假设服务器返回图片URL
          this.newProject.icon_name = res.data.filename;
        })
        .catch(error => {
          Message.error('图片上传失败: ' + (error.response?.data?.msg || error.msg));
        });
      return false; // 阻止默认上传行为
    },
    handleUploadSuccess(response, file) {
      // 此函数可能不再需要，但保留以防止错误
    },
    previewImageUrl(iconName) {
      if (!iconName) {
        return 'https://picsum.photos/300/200?random=100';
      }
      // 直接返回接口地址，让img标签的src属性直接请求该地址
      return `${service.defaults.baseURL}/file/image/preview/${iconName}`;
    },
    fetchProjects() {
      getProjectList()
        .then(response => {
          this.projects = response.data || [];
        })
        .catch(error => {
          Message.error('获取项目列表失败: ' + (error.response?.data?.message || error.message));
        });
    }
  },
  mounted() {
    this.fetchProjects();
  },
  data() {
    return {
      projects: [],
      showAddProjectModal: false,
      imageUploaded: false,
      newProject: {
        name: '',
        description: '',
        image: 'https://picsum.photos/300/200?random=100',
        icon_name: ''
      },
      formRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '请输入描述', trigger: 'blur' }
        ]
      }
    };
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
  margin-bottom: 10px;
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
  min-height: 100px;
}

.upload-icon-container {
  width: 100px;
  height: 100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2px dashed #e8e8e8;
  border-radius: 4px;
  background-color: #f9f9f9;
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-icon-container:hover {
  border-color: #1890ff;
  background-color: #e6f7ff;
}

.upload-icon {
  color: #3399ff;
  margin-bottom: 8px;
}

.upload-text {
  font-size: 12px;
  color: #999;
}

.preview-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 4px;
  border: 2px solid #e8e8e8;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.preview-image:hover {
  border-color: #1890ff;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.project {
  padding: 20px;
}
</style>
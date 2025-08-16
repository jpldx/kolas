<template>
  <div class="server-list-container">
    <div class="table-actions">
      <div style="margin-top: 10px;">
        <Input v-model="searchKeyword" placeholder="请输入主机名称/IP" style="width: 300px;"></Input>
        <Button type="default" @click="handleSearch" icon="ios-search"></Button>
        <Button @click="handleReset" icon="md-refresh"></Button>
        <!-- <span class="server-title">主机列表</span> -->
        <Button type="primary" @click="showAddModal" icon="md-add"></Button>
      </div>
    </div>
    <Table :data="filteredResults" :columns="columns" :scroll-x="true"></Table>

    <!-- 添加/编辑主机模态框 -->
    <Modal v-model="modalVisible" :title="modalType === 'add' ? '新增主机' : '编辑主机'">
      <Form :model="formData" :rules="formRules" ref="serverForm">
        <FormItem label="名称" prop="name">
          <Input v-model="formData.name" placeholder="请输入名称"></Input>
        </FormItem>
        <FormItem label="IP" prop="ip">
          <Input v-model="formData.ip" placeholder="请输入IP"></Input>
        </FormItem>
        <FormItem label="端口" prop="port">
          <InputNumber v-model="formData.port" placeholder="请输入端口" style="width: 100%"></InputNumber>
        </FormItem>
        <FormItem label="账号" prop="username">
          <Input v-model="formData.username" placeholder="请输入账号"></Input>
        </FormItem>
        <FormItem label="密码" prop="password">
          <Input type="password" password v-model="formData.password" placeholder="请输入密码"></Input>
        </FormItem>
        <FormItem label="状态" prop="status">
          <Select v-model="formData.status">
            <Option value="online">在线</Option>
            <Option value="offline">下线</Option>
          </Select>
        </FormItem>
         <FormItem label="描述" prop="description">
          <Input type='textarea' v-model="formData.description" placeholder="请输入描述"></Input>
        </FormItem>
      </Form>
      <template #footer>
        <Button @click="handleTestConnection" :loading="testLoading" icon="md-sync">测试连接</Button>
        <Button type="primary" @click="handleSave">保存</Button>
      </template>
    </Modal>
  </div>
</template>

<script>
import { RouterLink } from 'vue-router';
import { Table, Tag, Button, Modal, Form, Input, InputNumber, Select, Option } from 'view-ui-plus';
import { save, list, testConnection, del } from '@/api/host';
import { resolveComponent } from 'vue';
/* eslint-disable */ 
export default {
  name: 'HostList',
  components: {
    Table,
    Tag,
    Button,
    Modal,
    Form,
    FormItem: Form.Item,
    Input,
    InputNumber,
    Select,
    Option,
    RouterLink
  },
  data() {
    return {
      searchKeyword: '',
      filteredResults: [],
      hosts: [],
      modalVisible: false,
      modalType: 'add',
      formData: {
          id: '',
          ip: '',
          name: '',
          username: '',
          password: '',
          port: 1,
          description: '',
          status: 'online'
        },
      testLoading: false,
      formRules: {
        ip: [
          { required: true, message: '请输入主机IP', trigger: 'blur' },
          { pattern: /^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$/, message: '请输入有效的IP地址', trigger: 'blur' }
        ],
        name: [
          { required: true, message: '请输入主机名称', trigger: 'blur' }
        ],
        username: [
          { required: true, message: '请输入账号', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ],
        port: [
          { required: true, message: '请输入主机端口', trigger: ['blur'] }
        ],
        status: [
          { required: true, message: '请选择状态', trigger: 'change' }
        ]
      },
      columns: [
        {
          title: '#',
          key: 'index',
          width: 80,
          render: (h, params) => params.index + 1
        },
        {
          title: 'IP',
          key: 'ip',
          render: (h, params) => {
            return h(RouterLink, {
              to: `/host-detail/${params.row.id}`,
              attrs: {
                style: 'color: #2d8cf0; text-decoration: underline;'
              }
            }, params.row.ip);
          }
        },
        {
          title: '账号',
          key: 'username'
        },
         {
          title: '端口',
          key: 'port'
        },
        {
          title: '主机名称',
          key: 'name'
        },
        { 
          title: '状态', 
          key: 'status', 
          render: (h, params) => {
          return h(resolveComponent('Tag'), {
            color: params.row.status === 'online' ? 'success' : 'error'
          }, params.row.status === 'online' ? '在线' : '下线');
        }},
        {
          title: '操作',
          key: 'action',
          width: 150,
          render: (h, params) => {
            return h('div', [
              h(resolveComponent('Button'), {
                type: 'primary',
                size: 'small',
                style: { marginRight: '5px' },
                onClick: () => {
                    this.showEditModal(params.row )
                }
              }, '修改'),
              h(resolveComponent('Button'), {
                type: 'error',
                size: 'small',
                onClick: () => {
                    this.handleDelete(params.row.id, params.row.ip)
                }
              }, '删除')
            ]);
          }
        }
      ]
    };
  },
  computed: {
    filteredServers() {
      const keyword = this.searchKeyword.toLowerCase();
      return this.hosts.filter(server => 
        server.name.toLowerCase().includes(keyword) || 
        server.ip.toLowerCase().includes(keyword)
      );
    }
  },
  created() {
    this.loadServerData();
  },
  methods: {
    loadServerData() {
      list(1).then(response => {
        this.hosts = response.data;
        this.handleSearch();
      }).catch(error => {
        this.$Message.error('加载主机数据失败: ' + (error.response?.data?.message || '网络错误'));
      });
    },
    handleSearch() {
      const keyword = this.searchKeyword.toLowerCase();
      this.filteredResults = this.hosts.filter(server => 
        server.name.toLowerCase().includes(keyword) || 
        server.ip.toLowerCase().includes(keyword)
      );
    },
    handleReset() {
      this.searchKeyword = '';
      this.handleSearch();
    },
    showAddModal() {
      this.modalType = 'add';
      this.formData = {
        project_id: 1,
        ip: '',
        name: '',
        port: 22,
        description: '',
        status: 'online'
        };
      this.modalVisible = true;
    },
    showEditModal(row) {
      this.modalType = 'edit';
      this.formData = { ...row, port: Number(row.port), status: row.status };
      this.modalVisible = true;
    },
    handleTestConnection() {
      // 验证必要的连接信息
      if (!this.formData.ip || !this.formData.port || !this.formData.username || !this.formData.password) {
        this.$Message.warning('请填写IP、端口、账号和密码');
        return;
      }
      
      // this.$Message.loading('正在测试连接...', 0);
      this.testLoading = true;
      testConnection({
        ip: this.formData.ip,
        port: this.formData.port,
        username: this.formData.username,
        password: this.formData.password
      })
        .then(response => {
          this.testLoading = false;
          if (response.data) {
            this.$Message.success('连接测试成功');
          } else {
            this.$Message.error('连接测试失败');
          }
        })
        .catch(error => {
          this.testLoading = false;
          this.$Message.error('连接测试失败: ' + (error.response?.data?.message || '网络错误'));
        });
    },
    handleSave() {
      this.$refs.serverForm.validate(valid => {
        if (valid) {
          save(this.formData).then(response => {
            this.$Message.success('保存成功');
            this.loadServerData();
            this.modalVisible = false;
          }).catch(error => {
            this.$Message.error('保存失败: ' + (error.response?.data?.message || '网络错误'));
          });
        }
      });
    },
    handleDelete(id, ip) {
      this.$Modal.confirm({
        title: '确认删除',
        content: '确定要删除此主机（' + ip + '）吗？',
        onOk: () => {
          // this.servers = this.servers.filter(item => item.id !== id);
            del(id).then(response => {
            this.$Message.success('删除成功');
            this.loadServerData();
          }).catch(error => {
            this.$Message.error('删除失败: ' + (error.response?.data?.message || '网络错误'));
          });
        }
      });
    }
  }
};
</script>

<style scoped>
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
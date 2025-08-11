<template>
  <div class="server-list-container">
    <div class="table-actions">
      <div style="margin-top: 10px;">
        <Input v-model="searchKeyword" placeholder="请输入服务器名称/IP" style="width: 300px; margin-right: 10px;"></Input>
        <Button type="default" @click="handleSearch" style="margin-right: 10px;" icon="ios-search"></Button>
        <!-- <span class="server-title">服务器列表</span> -->
        <Button type="primary" @click="showAddModal" icon="md-add"></Button>
      </div>
    </div>
    <Table :data="filteredResults" :columns="columns" border :scroll-x="true"></Table>

    <!-- 添加/编辑服务器模态框 -->
    <Modal v-model="modalVisible" :title="modalType === 'add' ? '新增服务器' : '编辑服务器'">
      <Form :model="formData" :rules="formRules" ref="serverForm">
        <FormItem label="服务器IP" prop="ip">
          <Input v-model="formData.ip" placeholder="请输入服务器IP"></Input>
        </FormItem>
        <FormItem label="服务器名称" prop="name">
          <Input v-model="formData.name" placeholder="请输入服务器名称"></Input>
        </FormItem>
        <FormItem label="服务器状态" prop="statusText">
          <Select v-model="formData.statusText">
            <Option value="在线">在线</Option>
            <Option value="离线">离线</Option>
          </Select>
        </FormItem>
      </Form>
      <template #footer>
        <Button @click="modalVisible = false">取消</Button>
        <Button type="primary" @click="handleSave">保存</Button>
      </template>
    </Modal>
  </div>
</template>

<script>
import { Table, Tag, Button, Modal, Form, Input, Select, Option } from 'view-ui-plus';
/* eslint-disable */ 
export default {
  name: 'ServerList',
  components: {
    Table,
    Tag,
    Button,
    Modal,
    Form,
    FormItem: Form.Item,
    Input,
    Select,
    Option
  },
  data() {
    return {
      searchKeyword: '',
      filteredResults: [],
      servers: [],
      modalVisible: false,
      modalType: 'add',
      formData: {
        id: '',
        ip: '',
        name: '',
        port: '',
        statusText: '在线'
      },
      formRules: {
        ip: [
          { required: true, message: '请输入服务器IP', trigger: 'blur' },
          { pattern: /^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$/, message: '请输入有效的IP地址', trigger: 'blur' }
        ],
        name: [
          { required: true, message: '请输入服务器名称', trigger: 'blur' }
        ],
        port: [
          { required: true, message: '请输入服务器端口', trigger: 'blur' },
          { type: 'number', min: 1, max: 65535, message: '端口范围应在1-65535之间', trigger: 'blur' }
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
          key: 'ip'
        },
         {
          title: '端口',
          key: 'port'
        },
        {
          title: '服务器名称',
          key: 'name'
        },
        {
          title: '状态',
          key: 'status',
          render: (h, params) => {
            return h(Tag, {
              props: {
                type: params.row.statusText.trim() === '在线' ? 'success' : (params.row.statusText.trim() === '离线' ? 'error' : 'default')
              }
            }, params.row.statusText);
          }
        },
        {
          title: '操作',
          key: 'action',
          width: 150,
          render(h, params) {
            return h('div', [
              h(Button, {
                type: 'primary',
                size: 'small',
                style: { marginRight: '5px' },
                on: { click: () => this.showEditModal(params.row) }
              }, '修改'),
              h(Button, {
                type: 'error',
                size: 'small',
                on: { click: () => this.handleDelete(params.row.id) }
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
      return this.servers.filter(server => 
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
      // 模拟服务器数据
      this.servers = [
        { id: 1, ip: '192.168.1.101', port: 8080, status: 'success', statusText: '在线', name: '主服务器' },
        { id: 2, ip: '192.168.1.102', port: 8080, status: 'warning', statusText: '在线', name: '备份服务器' },
        { id: 3, ip: '192.168.1.103', port: 8080, status: 'error', statusText: '在线', name: '测试服务器' },
        { id: 4, ip: '192.168.1.104', port: 8080, status: 'success', statusText: '离线', name: '开发服务器' }
      ];
      this.filteredResults = [...this.servers];
    },
    handleSearch() {
      const keyword = this.searchKeyword.toLowerCase();
      this.filteredResults = this.servers.filter(server => 
        server.name.toLowerCase().includes(keyword) || 
        server.ip.toLowerCase().includes(keyword)
      );
    },
    showAddModal() {
      this.modalType = 'add';
      this.formData = {
        id: Date.now(),
        ip: '',
        name: '',
        port: '',
        statusText: '在线'
      };
      this.modalVisible = true;
    },
    showEditModal(row) {
      this.modalType = 'edit';
      this.formData = { ...row };
      this.modalVisible = true;
    },
    handleSave() {
      this.$refs.serverForm.validate(valid => {
        if (valid) {
          if (this.modalType === 'add') {
            this.servers.push(this.formData);
          } else {
            const index = this.servers.findIndex(item => item.id === this.formData.id);
            if (index !== -1) {
              this.servers.splice(index, 1, this.formData);
            }
          }
          this.modalVisible = false;
        }
      });
    },
    handleDelete(id) {
      this.$Modal.confirm({
        title: '确认删除',
        content: '确定要删除此服务器吗？',
        onOk: () => {
          this.servers = this.servers.filter(item => item.id !== id);
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
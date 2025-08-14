<template>
  <div class="task-detail-container">
    <div class="layout-row">
      <div class="left-column">
        <!-- <h2>任务基本信息</h2> -->
        <Divider orientation="center">任务基本信息</Divider>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        <Form :model="task" :label-width="100" >
          <FormItem label="JAR包上传">
            <Upload type="drag" action="/upload" :on-success="handleUploadSuccess">
              <div style="padding: 20px 0;">
                <Icon type="ios-cloud-upload" size="50"></Icon>
                <p>点击或拖拽文件到此处上传</p>
              </div>
            </Upload>
          </FormItem>
          <FormItem label="目标主机" prop="host">
            <!-- <Select v-model="task.host" placeholder="请选择目标主机">
              <Option v-for="item in hostOptions" :value="item.value" :key="item.value" >{{ item.label }}
                <Tag color="success" style="float:right" v-if="item.status === 'online'">在线</Tag>
                <Tag color="error" style="float:right" v-else>下线</Tag>
              </Option>
            </Select> -->
            <Select v-model="task.host" placeholder="请选择目标主机">
              <Option 
                v-for="item in hostOptions" 
                :value="item.value" 
                :key="item.value"
                :label="item.label"
              >
                <div style="display: flex; justify-content: space-between; align-items: center;">
                  <span>{{ item.label }}</span>
                  <Tag 
                    :color="item.status === 'online' ? 'success' : 'error'"
                    style="pointer-events: none;" 
                  >
                    {{ item.status === 'online' ? '在线' : '下线' }}
                  </Tag>
                </div>
              </Option>
          </Select>
          </FormItem>
          <FormItem label="目标路径" prop="targetPath">
            <Input v-model="task.targetPath" placeholder="请输入目标路径"></Input>
          </FormItem>
          <FormItem label="后置操作" prop="postOperation">
            <Input type="textarea" v-model="task.postOperation" :rows="4" placeholder="请输入后置操作命令"></Input>
          </FormItem>
          <FormItem>
          <div class="button-group">
            <Button type="primary" @click="handleSave" icon="md-refresh">
              保存
              <!-- <Icon type="" /> -->
            </Button>
            <Button type="success" @click="handleExecute" style="margin-left: 10px;" icon="ios-arrow-forward">
              执行
              <!-- <Icon type="ios-arrow-forward" /> -->
            </Button>
          </div>
          </FormItem>
        </Form>
      </div>
      <div class="right-column">
        <!-- <h2>任务执行日志</h2> -->
        <Divider orientation="center">任务执行日志</Divider>
        <div class="log-container">
          <p v-for="(log, index) in task.logs" :key="index">{{ log }}</p>
        </div>
      </div>
    </div>
    <div class="history-table">
      <Divider orientation="left">执行历史</Divider>
      <!-- <Table :columns="historyColumns" :data="executionHistory" border></Table> -->
       <List>
        <ListItem>
            <ListItemMeta avatar="https://dev-file.iviewui.com/userinfoPDvn9gKWYihR24SpgC319vXY8qniCqj4/avatar" title="het-system-1.0.0.RELEASE.jar" description="执行时间: 2023-11-15 10:02:30 | 执行结果: 成功" />
        </ListItem>
        <ListItem>
            <ListItemMeta avatar="https://dev-file.iviewui.com/userinfoPDvn9gKWYihR24SpgC319vXY8qniCqj4/avatar" title="het-system-1.0.0.RELEASE.jar" description="执行时间: 2023-11-15 10:02:30 | 执行结果: 成功" />
        </ListItem>
        <!-- <ListItem>
            <ListItemMeta avatar="https://dev-file.iviewui.com/userinfoPDvn9gKWYihR24SpgC319vXY8qniCqj4/avatar" title="This is title" description="This is description, this is description." />
            <template #action>
                <li>
                    <a href="">Edit</a>
                </li>
                <li>
                    <a href="">More</a>
                </li>
            </template>
        </ListItem>
        <ListItem>
            <ListItemMeta avatar="https://dev-file.iviewui.com/userinfoPDvn9gKWYihR24SpgC319vXY8qniCqj4/avatar" title="This is title" description="This is description, this is description." />
            <template #action>
                <li>
                    <a href="">Edit</a>
                </li>
                <li>
                    <a href="">More</a>
                </li>
            </template>
        </ListItem> -->
    </List>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Input, Upload, Button, Icon, Message as ElMessage, Form, FormItem, Divider, Tag } from 'view-ui-plus'
import { list } from '@/api/host'
import { onMounted } from 'vue'

export default {
  name: 'TaskDetail',
  components: {
    Input, Upload, Button, Icon, Form, FormItem, Divider, Tag
  },
  setup() {
    const route = useRoute()
    const task = ref({
      name: '',
      type: 'JAR',
      host: '',
      targetPath: '',
      postOperation: '',
      status: '',
      duration: '',
      logs: []
    })
    const hostOptions = ref([])
    onMounted(async () => {
      try {
        // TODO 从路由参数获取project_id
        // const projectId = route.params.projectId;
        const projectId = 1
        if (!projectId) {
          ElMessage.warning('缺少项目ID，无法获取主机列表');
          return;
        }
        const response = await list(projectId);
        hostOptions.value = response.data.map(item => ({
          value: item.ip,
          label: `${item.ip} (${item.name})`,
          status: item.status
        }));
      } catch (error) {
        ElMessage.error('获取主机列表失败');
        console.error('获取主机列表错误:', error);
      }
    })
    const executionHistory = ref([
      { name: task.value.name, time: '2023-11-15 10:02:30', status: '成功', duration: '2分30秒' },
      { name: task.value.name, time: '2023-11-14 16:45:12', status: '失败', duration: '1分15秒' },
      { name: task.value.name, time: '2023-11-14 14:20:05', status: '成功', duration: '3分40秒' }
    ])
    const historyColumns = ref([
      { title: '任务名称', key: 'name', width: 180 },
      { title: '执行时间', key: 'time', width: 200 },
      { title: '状态', key: 'status', width: 100, render: (h, params) => {
        return h('Tag', {
          props: {
            type: params.row.status === '成功' ? 'success' : 'error'
          }
        }, params.row.status)
      }},
      { title: '持续时间', key: 'duration', width: 120 }
    ])
    const statusColor = ref('')
    const errorMessage = ref('')

    watch(
      () => route.params.name,
      (newName) => {
        if (!newName) {
          errorMessage.value = '未找到任务名称参数'
          task.value = { ...task.value, name: '' }
          return
        }
        errorMessage.value = ''
        // 在实际应用中，这里应该通过API获取任务详情
        // 这里使用模拟数据
        task.value = {
          name: newName,
          type: 'JAR',
          host: '192.168.1.100',
          status: '成功',
          duration: '2分30秒',
          logs: [
            '2023-11-15 10:00:00 - 开始部署',
            '2023-11-15 10:00:05 - 正在传输文件',
            '2023-11-15 10:01:20 - 文件传输完成',
            '2023-11-15 10:01:25 - 正在启动服务',
            '2023-11-15 10:02:30 - 服务启动成功'
          ]
        }
        // 根据状态设置标签颜色
        statusColor.value = task.value.status === '成功' ? 'success' : 'error'
      },
      { immediate: true }
    )

    const handleUploadSuccess = (response) => {
      // 处理文件上传成功逻辑
      console.log('文件上传成功', response)
    }

    const handleSave = () => {
      // 处理保存逻辑
      console.log('保存任务配置', task.value)
      // 在实际应用中，这里应该通过API保存配置
      ElMessage.success('任务配置保存成功')
    }

    const handleExecute = () => {
      // 处理执行逻辑
      console.log('执行任务', task.value)
      // 在实际应用中，这里应该通过API执行任务
      // 模拟任务执行
      task.value.status = '执行中'
      statusColor.value = 'processing'
      // 模拟日志更新
      setTimeout(() => {
        task.value.logs = [
          '2023-11-15 10:00:00 - 开始部署',
          '2023-11-15 10:00:05 - 正在传输文件',
          '2023-11-15 10:01:20 - 文件传输完成',
          '2023-11-15 10:01:25 - 正在启动服务',
          '2023-11-15 10:02:30 - 服务启动成功'
        ]
        task.value.status = '成功'
        task.value.duration = '2分30秒'
        statusColor.value = 'success'
        ElMessage.success('任务执行成功')
      }, 3000)
    }

    return {
      task,
      hostOptions,
      statusColor,
      executionHistory,
      historyColumns,
      handleUploadSuccess,
      handleSave,
      handleExecute
    }
  }
}
</script>

<style scoped>
.task-detail-container {
  padding: 20px;
}

.layout-row {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.left-column, .right-column {
  flex: 1;
  min-width: 0;
  padding: 20px;
  border: 1px solid #e8e8e8;
  border-radius: 4px;
}

.ivu-form-item {
  margin-bottom: 16px;
}

.ivu-form-item-content {
  display: inline-block;
  width: calc(100% - 110px);
}

.ivu-upload {
  width: 100%;
}

.button-group {
  margin-top: 0;
  padding-top: 0;
  border-top: none;
}

.button-group {
  /* margin-top: 20px; */
  /* padding-top: 20px; */
  /* border-top: 1px solid #e8e8e8; */
  display: flex;
  justify-content: center;
}

.ivu-input,
.ivu-textarea,
.ivu-upload {
  width: calc(100% - 110px);
  display: inline-block;
}

.log-container {
  margin-top: 16px;
  padding: 16px;
  background-color: #f5f5f5;
  border-radius: 4px;
  height: 300px;
  overflow-y: auto;
}

.log-container p {
  margin: 4px 0;
  font-family: monospace;
  font-size: 14px;
}

::v-deep .ivu-select-item {
  text-align: left !important;
}

::v-deep .ivu-select-selection {
  text-align: left !important;
}

.history-table {
  margin-top: 20px;
}

.history-table h3 {
  margin-bottom: 16px;
}

::v-deep .ivu-table {
  width: 100%;
}

.history-table ::v-deep .ivu-list-item-meta {
  text-align: left;
}

.history-table ::v-deep .ivu-list-item-meta-title {
  text-align: left;
}

.history-table ::v-deep .ivu-list-item-meta-description {
  text-align: left;
}
</style>
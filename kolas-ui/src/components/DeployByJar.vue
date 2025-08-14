<template>
  <div class="deploy-by-jar-container">
    <h2>部署任务列表</h2>
    <Table border :columns="columns" :data="taskList" class="task-table"></Table>
  </div>
</template>

<script>
import { Table, Tag, Icon, Button } from 'view-ui-plus'
import { RouterLink } from 'vue-router'
import { ref } from 'vue'

export default {
  name: 'DeployByJar',
  components: {
      Table
    },
  setup() {
    // const router = useRouter()
    const handleDelete = (row) => {
      console.log('删除任务:', row)
      // 这里添加删除任务的逻辑
    }

    // 定义表格列
    const columns = ref([
      {
        title: '#',
        key: 'index',
        width: 80,
        align: 'center',
        render: (h, params) => params.index + 1
      },
      {
        title: '任务名称',
        key: 'name',
        minWidth: 150,
        render: (h, params) => {
          return h(RouterLink, { to: `/task-detail/${params.row.name}` }, () => params.row.name)
        }
      },
      {
        title: '任务类型',
        key: 'type',
        minWidth: 120
      },
      {
        title: '目标主机',
        key: 'host',
        minWidth: 150
      },
      {
        title: '上次执行状态',
        key: 'status',
        minWidth: 140,
        render: (h, params) => {
          const color = params.row.status === '成功' ? 'green' : 'red'
          return h(Tag, { color }, params.row.status)
        }
      },
      {
        title: '执行耗时',
        key: 'duration',
        minWidth: 140,
        render: (h, params) => {
          return h('div', [
            h(Icon, { type: 'ios-clock-outline' }),
            h('span', ` ${params.row.duration}`)
          ])
        }
      },
      {
        title: '操作',
        key: 'action',
        width: 140,
        align: 'center',
        render: (h, params) => {
          return h('div', [
            // h(Button, { type: 'default', size: 'small', style: { marginRight: '8px' }, on: { click: () => { console.log('详情按钮点击', params.row.name); router.push(`/task-detail/${params.row.name}`); } } }, '详情'),
            h(Button, { type: 'error', size: 'small', on: { click: () => handleDelete(params.row) } }, '删除')
          ])
        }
      }
    ])

    // 模拟任务数据
    const taskList = ref([
      {
        name: 'API服务部署',
        type: 'JAR',
        host: '192.168.1.100',
        status: '成功',
        duration: '2分30秒'
      },
      {
        name: 'Web前端部署',
        type: 'JAR',
        host: '192.168.1.101',
        status: '失败',
        duration: '1分45秒'
      },
      {
        name: '数据库迁移',
        type: 'JAR',
        host: '192.168.1.102',
        status: '成功',
        duration: '3分10秒'
      }
    ])

    return {
      columns,
      taskList
    }
  }
}
</script>

<style scoped>
.deploy-by-jar-container {
  padding: 20px;
}

.task-table {
  margin-top: 20px;
  text-align: left;
}

.success-status {
  color: #52c41a;
}

.failed-status {
  color: #ff4d4f;
}
</style>
<template>
  <div class="server-detail-container">
    <!-- <Breadcrumb>
      <BreadcrumbItem><RouterLink to="/host">主机列表</RouterLink></BreadcrumbItem>
      <BreadcrumbItem>主机详情</BreadcrumbItem>
    </Breadcrumb> -->
    <Card class="detail-card">
      <Tabs v-model="activeKey" type="card">
        <TabPane label="主机详情" name="detail">
          <Spin v-if="loading" size="large"></Spin>
          <Row v-else>
            <Col span="12">
              <div class="detail-content">
                <List item-layout="horizontal" bordered>
                  <ListItem>
                    <Tag color="success">名称</Tag>{{ server.name }}
                  </ListItem>
                  <ListItem>
                    <Tag color="success">IP</Tag>{{ server.ip }}
                  </ListItem>
                  <ListItem>
                      <Tag color="success">端口</Tag>{{ server.port }}
                  </ListItem>
                  <ListItem>
                    <!-- <ListItemMeta label="状态">
                      <template #description>
                        <Tag :color="server.status === 'online' ? 'success' : 'error'">{{ server.status === 'online' ? '在线' : '下线' }}</Tag>
                      </template>
                    </ListItemMeta> -->
                       <Tag color="success">状态</Tag>{{ server.status }}
                  </ListItem>
                  <ListItem>
                    <!-- <ListItemMeta label="描述" description="{{ server.description }}"/> -->
                     <Tag color="success">描述</Tag>{{ server.description }}
                  </ListItem>
                  <!-- <ListItem>
                    <ListItemMeta label="创建时间" description="{{ server.createTime }}"/>
                  </ListItem> -->
                </List>
                <!-- <div class="detail-actions">
                  <Button type="primary" @click="goBack">返回列表</Button>
                </div> -->
              </div>
            </Col>
          </Row>
        </TabPane>
        <TabPane label="WebSSH" name="external">
          <div class="external-page-container">
            <Button v-if="!showIframe" type="primary" @click="handleConnectSSH"><img src="/img/shell.png" style="width: 24px; height: 24px; margin-right: 6px; vertical-align: middle;" /> Connect SSH</Button>
            <iframe v-else :src="externalUrl" class="external-iframe"></iframe>
          </div>
        </TabPane>
      </Tabs>
    </Card>
  </div>
</template>

<script>
/* eslint-disable */
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Card, List, ListItem, ListItemMeta, Tag, Breadcrumb, BreadcrumbItem, Button, Spin, Tabs, TabPane, Row, Col } from 'view-ui-plus';
import { get } from '@/api/host';
import { RouterLink } from 'vue-router';

export default {
  name: 'HostDetail',
  components: {
    Card,
    List,
    ListItem,
    ListItemMeta,
    Tag,
    Breadcrumb,
    BreadcrumbItem,
    Button,
    Spin,
    RouterLink,
    Tabs,
    TabPane
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const server = ref({});
    const loading = ref(true);
    const activeKey = ref('detail');
    const externalUrl = ref(''); // 用户可替换为实际URL

    const showIframe = ref(false);
    const handleConnectSSH = () => {
      showIframe.value = true;
    };

    const fetchServerDetail = async () => {
      try {
        loading.value = true;
        const response = await get(route.params.id);
        server.value = response.data;
        // 设置SSH连接URL
        externalUrl.value = `http://localhost:8888/?hostname=${server.value.ip}&username=${server.value.username}&password=${server.value.password}`;
        // 格式化日期（如果API返回的是时间戳）
        if (server.value.createTime) {
          server.value.createTime = new Date(server.value.createTime).toLocaleString();
        }
      } catch (error) {
        console.error('获取主机详情失败:', error);
        this.$Message.error('获取主机详情失败: ' + (error.response?.data?.message || '网络错误'));
      } finally {
        loading.value = false;
      }
    };

    const goBack = () => {
      router.push('/host');
    };

    onMounted(() => {
      fetchServerDetail();
    });

    return {
      server,
      loading,
      goBack,
      activeKey,
      externalUrl,
      showIframe,
      handleConnectSSH
    };
  }
};
</script>

<style scoped>
.server-detail-container {
  padding: 0;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.detail-card {
  padding-top: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  height: 100vh;
  box-sizing: border-box;
}

.detail-content {
  margin-top: 20px;
}

.detail-actions {
  margin-top: 30px;
  text-align: right;
}

.ivu-form-item {
  margin-bottom: 20px;
}

.external-page-container {
  width: 100%;
  height: 100%;
  text-align: left;
  box-sizing: border-box;
}
.external-iframe {
  width: 100%;
  height: 100%;
  min-height: calc(100vh - 60px);
  border: none;
  box-sizing: border-box;
}

::v-deep .ivu-tabs {
  height: 100%;
}

::v-deep .ivu-tabs-content {
  height: 100%;
  min-height: calc(100vh - 60px);
}

::v-deep .ivu-tabs-pane {
  height: 100%;
}

.detail-content .ivu-list-item {
  padding: 16px 24px;
}

.detail-content .ivu-list-item-meta-label {
  font-weight: 500;
  width: 100px;
  text-align: left;
}

.detail-content .ivu-list-item-meta-description {
  color: #333;
  text-align: left;
}

.detail-card {
  width: 100%;
}

::v-deep .ivu-tag {
  width: 40px;
  text-align: center;
}

@media (min-width: 768px) {
  .detail-card {
    padding-left: 20px;
  }
}
</style>
//import { createApp } from 'vue'
//import App from './App.vue'
//
//createApp(App).mount('#app')

import { createApp } from 'vue'
import ViewUIPlus from 'view-ui-plus'
import App from './App.vue'
import router from './router'
//import store from './store'
import 'view-ui-plus/dist/styles/viewuiplus.css'
import { Message } from 'view-ui-plus'
import axios from './utils/axios'

const app = createApp(App)

// 注册全局组件和指令
app.use(ViewUIPlus)
//app.use(store)
  .use(router)

// 全局配置
app.config.globalProperties.$Message = Message
// 全局注册 axios
app.config.globalProperties.$axios = axios

app.mount('#app')
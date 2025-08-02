//import { createApp } from 'vue'
//import App from './App.vue'
//
//createApp(App).mount('#app')

import { createApp } from 'vue'
import ViewUIPlus from 'view-ui-plus'
import App from './App.vue'
//import router from './router'
//import store from './store'
import 'view-ui-plus/dist/styles/viewuiplus.css'

const app = createApp(App)

//app.use(store)
//  .use(router)
  app.use(ViewUIPlus)
  .mount('#app')
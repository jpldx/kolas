<template>
  <div class="deploy-to-host">
    <h2>Deploy to Host</h2>
    <div class="path-selector-container">
      <Input type="text" v-model="selectedPath" placeholder="选择目录路径" readonly />
      <Button @click="selectDirectory" type="primary" style="margin-left: 10px;">浏览...</Button>
    </div>
  </div>
</template>

<script>
import { Input, Button,  } from 'view-ui-plus'

export default {
  name: 'DeployToHost',
  components: {
    Input,
    Button
  },
  data() {
    return {
      selectedPath: ''
    }
  },
  methods: {
    selectDirectory() {
      // 这里使用Electron的dialog模块来选择目录
      // 注意：在浏览器环境中无法直接访问文件系统
      // 实际应用中，这部分代码需要在Electron主进程中实现
      try {
        // 检测是否在Electron环境中
        if (window.require) {
          const { dialog } = window.require('electron')
          dialog.showOpenDialog({
            properties: ['openDirectory']
          }).then(result => {
            if (!result.canceled && result.filePaths.length > 0) {
              this.selectedPath = result.filePaths[0]
              this.$Message.success('已选择目录: ' + this.selectedPath)
            }
          })
        } else {
          // 浏览器环境下的模拟行为
          this.selectedPath = '/Users/example/deploy-directory'
          this.$Message.success('浏览器环境下模拟选择目录: ' + this.selectedPath)
          this.$Message.info('提示: 在Electron环境中才能真正访问文件系统')
        }
      } catch (error) {
        this.$Message.error('选择目录失败: ' + error.message)
      }
    }
  }
}
</script>

<style scoped>
.deploy-to-host {
  padding: 20px;
}

.path-selector-container {
  display: flex;
  align-items: center;
  margin-top: 20px;
}
</style>
<template>
  <div class="deploy-to-host">
    <h2>Deploy to Host</h2>
    <div class="path-selector-container">
      <Input type="text" v-model="selectedPath" placeholder="选择文件路径" readonly />
      <!-- <Button @click="selectDirectory" type="primary" style="margin-left: 10px;">浏览...</Button> -->
        <Upload action="//jsonplaceholder.typicode.com/posts/" :on-success="handleUploadSuccess">
        <Button icon="ios-cloud-upload-outline" @click="selectDirectory" type="primary" style="margin-left: 10px;">选择</Button>
    </Upload>
    </div>
  </div>
</template>

<script>
import { Input, Upload } from 'view-ui-plus'

export default {
  name: 'DeployToHost',
  components: {
    Input,
    Upload
  },
  data() {
    return {
      selectedPath: ''
    }
  },
  methods: {
    handleUploadSuccess(response, file) {
      // 获取文件全路径
      let fullFilePath = '';
      
      // 检测是否在Electron环境中
      if (window.require) {
        const path = window.require('path');
        // 结合选择的目录路径和文件名
        if (this.selectedPath && file.name) {
          fullFilePath = path.join(this.selectedPath, file.name);
          this.$Message.success('文件全路径: ' + fullFilePath);
        } else {
          this.$Message.warning('请先选择目录');
        }
      } else {
        // 浏览器环境下无法获取完整路径
        fullFilePath = '浏览器环境下无法获取完整路径，文件名: ' + file.name;
        this.$Message.info(fullFilePath);
      }
      
      console.log('上传响应:', response);
      console.log('上传文件:', file);
      console.log('文件全路径:', fullFilePath);
    },
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
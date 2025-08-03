<template>
  <div class="settings-container">
    <h2>系统设置</h2>
    <div class="settings-form">
      <Form ref="formInline" :model="formInline" :rules="ruleInline" inline>
        <FormItem prop="username">
          <Input v-model="formInline.username" placeholder="用户名"></Input>
        </FormItem>
        <FormItem prop="password">
          <Input v-model="formInline.password" type="password" placeholder="密码"></Input>
        </FormItem>
        <FormItem>
          <Button type="primary" @click="handleSubmit('formInline')">提交</Button>
        </FormItem>
      </Form>
    </div>
  </div>
</template>

<script>
import { Form, FormItem, Input, Button } from 'view-ui-plus'

export default {
  name: 'SettingsPage',
  components: {
    Form,
    FormItem,
    Input,
    Button
  },
  data() {
    return {
      formInline: {
        username: '',
        password: ''
      },
      ruleInline: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { type: 'string', min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    handleSubmit(name) {
      this.$refs[name].validate(valid => {
        if (valid) {
          this.$Message.success('提交成功!');
        } else {
          this.$Message.error('表单验证失败!');
        }
      });
    }
  }
}
</script>

<style scoped>
.settings-container {
  padding: 20px;
}

.settings-form {
  margin-top: 20px;
}
</style>
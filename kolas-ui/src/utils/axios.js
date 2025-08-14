import axios from 'axios'
// import { Message } from 'view-ui-plus' 
import { useRouter } from 'vue-router'

// 创建 axios 实例
const service = axios.create({
//   baseURL: import.meta.env.VITE_API_BASE_URL, // 从环境变量获取基础 URL
  baseURL: 'http://localhost:8020/api', // 从环境变量获取基础 URL
  timeout: 10000, // 请求超时时间
  headers: {
    'Content-Type': 'application/json;charset=utf-8'
  }
})

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    // 在请求发送前做些什么，例如添加 token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    // 处理请求错误
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response) => {
    // 处理成功响应
    const res = response.data
    
    // 根据后端约定的状态码处理
    if (res.code !== 0) {
      this.$Message.error(res.msg || '操作失败')
      return Promise.reject(new Error(res.msg || 'Error'))
    }
    return res
  },
  (error) => {
    // 处理响应错误
    console.error('响应错误:', error)
    
    // 处理 401 未授权错误
    if (error.response && error.response.status === 401) {
      this.$Message.error('登录已过期，请重新登录')
      localStorage.removeItem('token')
      const router = useRouter()
      router.push('/login')
    } else {
      this.$Message.error(error.message || '网络错误')
    }
    return Promise.reject(error)
  }
)

export default service

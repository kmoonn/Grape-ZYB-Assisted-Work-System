import axios from 'axios'
import config from '@/config'
import { ElMessage } from 'element-plus'
import router from '@/router'

// 创建 axios 实例
const service = axios.create({
  // 根据环境使用不同的baseURL
  baseURL: import.meta.env.VITE_APP_API_URL,
  timeout: config.api.timeout,
  withCredentials: config.api.withCredentials
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 从 localStorage 获取 token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('请求错误：', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    
    // 这里可以根据后端的响应结构进行调整
    if (res.code && res.code !== 200) {
      ElMessage({
        message: res.message || '请求失败',
        type: 'error',
        duration: 5 * 1000
      })
      
      // 处理特定错误码
      if (res.code === 401) {
        // token 过期或无效
        localStorage.removeItem('token')
        router.push('/login')
      }
      
      return Promise.reject(res)
    }
    return res
  },
  error => {
    console.error('响应错误：', error)
    ElMessage({
      message: error.message || '网络错误',
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

// 添加开发环境调试信息
if (import.meta.env.DEV) {
  service.interceptors.request.use(config => {
    console.log('Request:', config)
    return config
  })
  
  service.interceptors.response.use(response => {
    console.log('Response:', response)
    return response
  })
}

export default service
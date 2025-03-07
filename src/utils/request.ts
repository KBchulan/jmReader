import axios from 'axios'
import type { AxiosRequestConfig, AxiosResponse } from 'axios'
// @ts-ignore
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

// 创建axios实例
const service = axios.create({
  // @ts-ignore
  baseURL: import.meta.env.VITE_API_BASE_URL as string,
  timeout: 15000
})

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    NProgress.start()
    // 可以在这里设置token等请求头
    // const token = localStorage.getItem('token')
    // if (token) {
    //   config.headers['Authorization'] = `Bearer ${token}`
    // }
    return config
  },
  (error) => {
    NProgress.done()
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    NProgress.done()
    return response.data
  },
  (error) => {
    NProgress.done()
    return Promise.reject(error)
  }
)

// 封装GET请求
export function get<T = any>(url: string, params?: any, config?: AxiosRequestConfig): Promise<T> {
  return service.get<T>(url, { params, ...config }).then(res => res as T)
}

// 封装POST请求
export function post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
  return service.post<T>(url, data, config).then(res => res as T)
}

// 封装PUT请求
export function put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
  return service.put<T>(url, data, config).then(res => res as T)
}

// 封装DELETE请求
export function del<T = any>(url: string, params?: any, config?: AxiosRequestConfig): Promise<T> {
  return service.delete<T>(url, { params, ...config }).then(res => res as T)
}

export default service 
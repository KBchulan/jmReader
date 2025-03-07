import { ElNotification, ElMessage } from 'element-plus'
import type { NotificationParams } from 'element-plus'

export function useNotification() {
  /**
   * 显示成功通知
   * @param message 消息内容
   * @param title 标题，可选
   */
  function success(message: string, title = '成功') {
    ElNotification({
      title,
      message,
      type: 'success',
      duration: 3000
    })
  }

  /**
   * 显示错误通知
   * @param message 消息内容
   * @param title 标题，可选
   */
  function error(message: string, title = '错误') {
    ElNotification({
      title,
      message,
      type: 'error',
      duration: 5000
    })
  }

  /**
   * 显示警告通知
   * @param message 消息内容
   * @param title 标题，可选
   */
  function warning(message: string, title = '警告') {
    ElNotification({
      title,
      message,
      type: 'warning',
      duration: 4000
    })
  }

  /**
   * 显示信息通知
   * @param message 消息内容
   * @param title 标题，可选
   */
  function info(message: string, title = '提示') {
    ElNotification({
      title,
      message,
      type: 'info',
      duration: 3000
    })
  }

  /**
   * 显示自定义通知
   * @param options 通知配置
   */
  function notify(options: NotificationParams) {
    ElNotification(options)
  }

  /**
   * 显示简短消息
   * @param message 消息内容
   * @param type 消息类型
   */
  function message(message: string, type: 'success' | 'warning' | 'info' | 'error' = 'info') {
    ElMessage({
      message,
      type,
      duration: type === 'error' ? 5000 : 3000
    })
  }

  return {
    success,
    error,
    warning,
    info,
    notify,
    message
  }
}

// 导出单例，便于在组件外使用
export const notify = useNotification() 
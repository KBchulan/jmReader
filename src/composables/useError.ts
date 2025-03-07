import { ref } from 'vue'
import { ElMessage } from 'element-plus'

// 全局错误状态
const error = ref<Error | null>(null)
const lastError = ref<Error | null>(null)
const errorCount = ref(0)

export function useError() {
  /**
   * 处理错误
   * @param err 错误对象或错误信息
   * @param showMessage 是否显示消息提示，默认为true
   */
  function handleError(err: unknown, showMessage = true) {
    let errorObj: Error

    if (err instanceof Error) {
      errorObj = err
    } else if (typeof err === 'string') {
      errorObj = new Error(err)
    } else {
      errorObj = new Error('发生未知错误')
    }

    // 设置错误状态
    error.value = errorObj
    lastError.value = errorObj
    errorCount.value++

    // 是否显示消息提示
    if (showMessage) {
      ElMessage.error({
        message: errorObj.message || '操作失败',
        duration: 3000
      })
    }

    // 打印错误到控制台
    console.error('[Error]', errorObj)

    return errorObj
  }

  /**
   * 清除当前错误
   */
  function clearError() {
    error.value = null
  }

  return {
    error,
    lastError,
    errorCount,
    handleError,
    clearError
  }
}

// 导出单例，便于在组件外使用
export const globalError = useError() 
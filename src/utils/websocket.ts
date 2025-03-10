import { ref } from 'vue'

// WebSocket连接状态
export const wsConnected = ref(false)

// 消息处理回调函数
type MessageHandler = (data: any) => void
const messageHandlers: Record<string, MessageHandler[]> = {}

// WebSocket实例
let ws: WebSocket | null = null

/**
 * 初始化WebSocket连接
 */
export function initWebSocket() {
  // 如果已经连接，先关闭
  if (ws) {
    ws.close()
  }

  // 创建WebSocket连接
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const baseUrl = import.meta.env.VITE_API_BASE_URL as string || ''
  let host = window.location.host
  
  // 从baseUrl中提取主机名
  if (baseUrl) {
    try {
      const url = new URL(baseUrl)
      host = url.host
    } catch (e) {
      console.error('解析API基础URL时出错:', e)
    }
  }
  
  const wsUrl = `${protocol}//${host}/ws`
  console.log('WebSocket连接URL:', wsUrl)
  
  try {
    ws = new WebSocket(wsUrl)

    // 连接打开
    ws.onopen = () => {
      console.log('WebSocket连接已建立')
      wsConnected.value = true
    }

    // 接收消息
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        console.log('收到WebSocket消息:', data)
        
        // 如果有action字段，触发对应的处理函数
        if (data.action && messageHandlers[data.action]) {
          messageHandlers[data.action].forEach(handler => handler(data))
        }
      } catch (error) {
        console.error('处理WebSocket消息时出错:', error)
      }
    }

    // 连接关闭
    ws.onclose = () => {
      console.log('WebSocket连接已关闭')
      wsConnected.value = false
      
      // 尝试重新连接
      setTimeout(() => {
        initWebSocket()
      }, 5000)
    }

    // 连接错误
    ws.onerror = (error) => {
      console.error('WebSocket连接错误:', error)
      wsConnected.value = false
    }
  } catch (error) {
    console.error('创建WebSocket连接时出错:', error)
  }
}

/**
 * 注册消息处理函数
 * @param action 消息类型
 * @param handler 处理函数
 */
export function onMessage(action: string, handler: MessageHandler) {
  if (!messageHandlers[action]) {
    messageHandlers[action] = []
  }
  messageHandlers[action].push(handler)
}

/**
 * 移除消息处理函数
 * @param action 消息类型
 * @param handler 处理函数
 */
export function offMessage(action: string, handler: MessageHandler) {
  if (messageHandlers[action]) {
    const index = messageHandlers[action].indexOf(handler)
    if (index !== -1) {
      messageHandlers[action].splice(index, 1)
    }
  }
}

/**
 * 关闭WebSocket连接
 */
export function closeWebSocket() {
  if (ws) {
    ws.close()
    ws = null
  }
} 
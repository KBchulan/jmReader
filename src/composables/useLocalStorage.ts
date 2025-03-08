import { ref, watch } from 'vue'

/**
 * 本地存储组合式函数
 * @param key 存储键名
 * @param initialValue 初始值
 * @param storage 存储对象，默认为localStorage
 */
export function useLocalStorage<T>(
  key: string,
  initialValue: T,
  storage: Storage = localStorage
) {
  // 创建响应式数据
  const storedValue = ref<T>(initialValue)

  try {
    // 尝试从存储中获取数据
    const item = storage.getItem(key)

    if (item) {
      storedValue.value = JSON.parse(item)
    } else {
      // 如果存储中没有数据，则存入初始值
      storage.setItem(key, JSON.stringify(initialValue))
    }
  } catch (error) {
    console.error(`Error reading ${key} from storage:`, error)
    // 出错时使用初始值
    storage.setItem(key, JSON.stringify(initialValue))
  }

  // 监听值变化，同步到存储
  watch(
    storedValue,
    (newValue) => {
      try {
        if (newValue === undefined) {
          storage.removeItem(key)
        } else {
          storage.setItem(key, JSON.stringify(newValue))
        }
      } catch (error) {
        console.error(`Error writing ${key} to storage:`, error)
      }
    },
    { deep: true }
  )

  // 返回响应式数据和函数
  return storedValue
} 
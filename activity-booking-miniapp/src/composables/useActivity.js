/**
 * 活动相关的组合式 API
 */
import { ref, computed } from 'vue'
import { useActivityStore } from '@/store/activity'
import { showToast } from '@/utils'

export function useActivity() {
  const activityStore = useActivityStore()
  
  // 活动列表
  const activityList = computed(() => activityStore.list)
  const activityDetail = computed(() => activityStore.detail)
  const loading = computed(() => activityStore.loading)
  
  // 分页状态
  const page = ref(1)
  const pageSize = ref(10)
  const hasMore = ref(true)
  
  /**
   * 获取活动列表
   */
  const fetchActivityList = async (params = {}) => {
    try {
      const res = await activityStore.fetchList({
        page: page.value,
        pageSize: pageSize.value,  // 改为驼峰命名
        ...params
      })
      
      if (res && res.items) {
        if (page.value === 1) {
          // 刷新
          activityStore.list = res.items
        } else {
          // 加载更多
          activityStore.list = [...activityStore.list, ...res.items]
        }
        
        hasMore.value = res.items.length === pageSize.value
      }
      
      return res
    } catch (error) {
      console.error('获取活动列表失败:', error)
      showToast('获取活动列表失败', 'error')
      return null
    }
  }
  
  /**
   * 获取活动详情
   */
  const fetchActivityDetail = async (id) => {
    try {
      const res = await activityStore.fetchDetail(id)
      return res
    } catch (error) {
      console.error('获取活动详情失败:', error)
      showToast('获取活动详情失败', 'error')
      return null
    }
  }
  
  /**
   * 刷新列表
   */
  const refreshList = async (params = {}) => {
    page.value = 1
    hasMore.value = true
    return await fetchActivityList(params)
  }
  
  /**
   * 加载更多
   */
  const loadMore = async (params = {}) => {
    if (!hasMore.value || loading.value) return
    
    page.value++
    return await fetchActivityList(params)
  }
  
  /**
   * 搜索活动
   */
  const searchActivities = async (keyword) => {
    if (!keyword.trim()) {
      showToast('请输入搜索关键词')
      return
    }
    
    return await refreshList({ keyword: keyword.trim() })
  }
  
  return {
    activityList,
    activityDetail,
    loading,
    page,
    pageSize,
    hasMore,
    fetchActivityList,
    fetchActivityDetail,
    refreshList,
    loadMore,
    searchActivities
  }
}

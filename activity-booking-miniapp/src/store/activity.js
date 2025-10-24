import { defineStore } from 'pinia'
import { getActivityList, getActivityDetail } from '@/api/activity'
import { handleApiResponse } from '@/utils/response'

export const useActivityStore = defineStore('activity', {
  state: () => ({
    list: [],
    detail: null,
    loading: false
  }),

  actions: {
    /**
     * 获取活动列表
     */
    async fetchList(params = {}) {
      try {
        this.loading = true
        const res = await getActivityList(params)
        // 现在 res 已经是处理后的数据（response.data）
        this.list = res.items || []
        return res
      } catch (error) {
        console.error('获取活动列表失败:', error)
        this.list = []
        return null
      } finally {
        this.loading = false
      }
    },

    /**
     * 获取活动详情
     */
    async fetchDetail(id) {
      try {
        this.loading = true
        const res = await getActivityDetail(id)
        // 现在 res 已经是处理后的数据（response.data）
        this.detail = res
        return res
      } catch (error) {
        console.error('获取活动详情失败:', error)
        this.detail = null
        return null
      } finally {
        this.loading = false
      }
    }
  }
})


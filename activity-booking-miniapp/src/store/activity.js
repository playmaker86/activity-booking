import { defineStore } from 'pinia'
import { getActivityList, getActivityDetail } from '@/api/activity'

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
        this.list = res.items || []
        return res
      } catch (error) {
        console.error('获取活动列表失败:', error)
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
        this.detail = res
        return res
      } catch (error) {
        console.error('获取活动详情失败:', error)
        return null
      } finally {
        this.loading = false
      }
    }
  }
})


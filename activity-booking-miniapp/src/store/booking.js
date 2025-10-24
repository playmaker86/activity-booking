import { defineStore } from 'pinia'
import { createBooking, getMyBookings, getBookingDetail, cancelBooking, checkIn } from '@/api/booking'
import { handleApiResponse } from '@/utils/response'

export const useBookingStore = defineStore('booking', {
  state: () => ({
    list: [],
    detail: null,
    loading: false
  }),

  actions: {
    /**
     * 创建预约
     */
    async createBooking(data) {
      try {
        this.loading = true
        const res = await createBooking(data)
        // 现在 res 已经是处理后的数据（response.data）
        return res
      } catch (error) {
        console.error('创建预约失败:', error)
        return null
      } finally {
        this.loading = false
      }
    },

    /**
     * 获取我的预约列表
     */
    async fetchMyBookings(params = {}) {
      try {
        this.loading = true
        const res = await getMyBookings(params)
        // 现在 res 已经是处理后的数据（response.data）
        this.list = res.items || []
        return res
      } catch (error) {
        console.error('获取预约列表失败:', error)
        this.list = []
        return null
      } finally {
        this.loading = false
      }
    },

    /**
     * 获取预约详情
     */
    async fetchDetail(id) {
      try {
        this.loading = true
        const res = await getBookingDetail(id)
        // 现在 res 已经是处理后的数据（response.data）
        this.detail = res
        return res
      } catch (error) {
        console.error('获取预约详情失败:', error)
        this.detail = null
        return null
      } finally {
        this.loading = false
      }
    },

    /**
     * 取消预约
     */
    async cancelBooking(id) {
      try {
        this.loading = true
        const res = await cancelBooking(id)
        // 现在 res 已经是处理后的数据（response.data）
        return res
      } catch (error) {
        console.error('取消预约失败:', error)
        return null
      } finally {
        this.loading = false
      }
    },

    /**
     * 签到
     */
    async checkIn(id) {
      try {
        this.loading = true
        const res = await checkIn(id)
        // 现在 res 已经是处理后的数据（response.data）
        return res
      } catch (error) {
        console.error('签到失败:', error)
        return null
      } finally {
        this.loading = false
      }
    }
  }
})

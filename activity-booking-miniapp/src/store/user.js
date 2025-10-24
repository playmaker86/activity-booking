import { defineStore } from 'pinia'
import { wxLogin, getUserInfo } from '@/api/user'
import storage from '@/utils/storage'
import { handleApiResponse } from '@/utils/response'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: storage.get('token') || '',
    userInfo: storage.get('userInfo') || null
  }),

  getters: {
    isLogin: (state) => !!state.token
  },

  actions: {
    /**
     * 微信授权登录
     */
    async login() {
      try {
        // 获取用户授权
        const authResult = await this.getUserProfile()
        if (!authResult) {
          return false
        }

        const { code } = await uni.login({ provider: 'weixin' })
        const res = await wxLogin(code)
        // 现在 res 已经是处理后的数据（response.data）
        this.token = res.token
        storage.set('token', res.token)
        await this.fetchUserInfo()
        return true
      } catch (error) {
        console.error('登录失败:', error)
        return false
      }
    },

    /**
     * 获取用户授权信息
     */
    async getUserProfile() {
      try {
        const res = await uni.getUserProfile({
          desc: '用于完善用户资料'
        })
        return res
      } catch (error) {
        console.error('获取用户授权失败:', error)
        // 如果用户拒绝授权，提示用户
        uni.showModal({
          title: '提示',
          content: '需要您的授权才能登录',
          showCancel: false
        })
        return null
      }
    },

    /**
     * 获取用户信息
     */
    async fetchUserInfo() {
      try {
        const userInfo = await getUserInfo()
        // 现在 userInfo 已经是处理后的数据（response.data）
        this.userInfo = userInfo
        storage.set('userInfo', userInfo)
      } catch (error) {
        console.error('获取用户信息失败:', error)
        this.userInfo = null
      }
    },

    /**
     * 退出登录
     */
    logout() {
      this.token = ''
      this.userInfo = null
      storage.remove('token')
      storage.remove('userInfo')
    }
  }
})


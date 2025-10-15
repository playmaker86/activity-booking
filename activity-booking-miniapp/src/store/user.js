import { defineStore } from 'pinia'
import { wxLogin, getUserInfo } from '@/api/user'
import storage from '@/utils/storage'

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
     * 登录
     */
    async login() {
      try {
        const { code } = await uni.login({ provider: 'weixin' })
        const res = await wxLogin(code)
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
     * 获取用户信息
     */
    async fetchUserInfo() {
      try {
        const userInfo = await getUserInfo()
        this.userInfo = userInfo
        storage.set('userInfo', userInfo)
      } catch (error) {
        console.error('获取用户信息失败:', error)
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


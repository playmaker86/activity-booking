/**
 * 用户相关的组合式 API
 */
import { ref, computed } from 'vue'
import { useUserStore } from '@/store/user'
import { showToast } from '@/utils'

export function useUser() {
  const userStore = useUserStore()
  
  // 用户信息
  const userInfo = computed(() => userStore.userInfo)
  const isLogin = computed(() => userStore.isLogin)
  
  // 登录状态
  const loginLoading = ref(false)
  
  /**
   * 登录
   */
  const login = async () => {
    if (loginLoading.value) return false
    
    try {
      loginLoading.value = true
      const success = await userStore.login()
      
      if (success) {
        showToast('登录成功', 'success')
        return true
      } else {
        showToast('登录失败', 'error')
        return false
      }
    } catch (error) {
      console.error('登录错误:', error)
      showToast('登录失败', 'error')
      return false
    } finally {
      loginLoading.value = false
    }
  }
  
  /**
   * 退出登录
   */
  const logout = () => {
    userStore.logout()
    showToast('已退出登录', 'success')
  }
  
  /**
   * 更新用户信息
   */
  const updateUserInfo = async () => {
    try {
      await userStore.fetchUserInfo()
    } catch (error) {
      console.error('更新用户信息失败:', error)
    }
  }
  
  /**
   * 检查登录状态
   */
  const checkLogin = () => {
    if (!isLogin.value) {
      showToast('请先登录')
      return false
    }
    return true
  }
  
  return {
    userInfo,
    isLogin,
    loginLoading,
    login,
    logout,
    updateUserInfo,
    checkLogin
  }
}

import request from '@/utils/request'

/**
 * 微信登录
 */
export function wxLogin(code) {
  return request.post('/auth/wx-login', { code })
}

/**
 * 获取用户信息
 */
export function getUserInfo() {
  return request.get('/users/me')
}

/**
 * 更新用户信息
 */
export function updateUserInfo(data) {
  return request.put('/users/me', data)
}


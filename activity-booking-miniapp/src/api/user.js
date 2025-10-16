import request from '@/utils/request'

/**
 * 微信小程序登录
 */
export function wxLogin(code) {
  return request.post('/auth/wx-login', { code })
}

/**
 * 微信网页授权登录
 */
export function wxWebLogin(code, state) {
  return request.post('/auth/wx-web-login', { code, state })
}

/**
 * 获取微信网页授权登录URL
 */
export function getWxWebLoginUrl(redirectUri) {
  return request.get('/auth/wx-web-login-url', { 
    params: { redirect_uri: redirectUri }
  })
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


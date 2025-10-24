/**
 * 统一响应处理工具
 */

/**
 * 处理 API 响应
 * @param {Object} response - API 响应对象
 * @param {number} response.code - 业务状态码
 * @param {string} response.message - 响应消息
 * @param {any} response.data - 响应数据
 * @param {string} response.error - 错误信息
 * @returns {Promise} 处理后的数据或错误
 */
export function handleApiResponse(response) {
  const { code, message, data, error } = response
  
  if (code === 200 || code === 201) {
    // 成功响应
    return Promise.resolve(data)
  } else {
    // 错误响应
    const errorMessage = message || '请求失败'
    
    // 根据状态码进行不同处理
    switch (code) {
      case 400:
        // 参数错误
        uni.showToast({
          title: errorMessage,
          icon: 'none',
          duration: 3000
        })
        break
      case 401:
        // 未授权，跳转到登录页
        uni.removeStorageSync('token')
        uni.removeStorageSync('userInfo')
        uni.navigateTo({
          url: '/pages/login/login'
        })
        break
      case 403:
        // 禁止访问
        uni.showToast({
          title: '权限不足',
          icon: 'none'
        })
        break
      case 404:
        // 资源不存在
        uni.showToast({
          title: errorMessage,
          icon: 'none'
        })
        break
      case 409:
        // 冲突
        uni.showToast({
          title: errorMessage,
          icon: 'none'
        })
        break
      case 500:
        // 服务器错误
        uni.showToast({
          title: '服务器错误，请稍后重试',
          icon: 'none'
        })
        break
      default:
        uni.showToast({
          title: errorMessage,
          icon: 'none'
        })
    }
    
    return Promise.reject(new Error(errorMessage))
  }
}

/**
 * 检查响应是否成功
 * @param {Object} response - API 响应对象
 * @returns {boolean} 是否成功
 */
export function isSuccessResponse(response) {
  return response && (response.code === 200 || response.code === 201)
}

/**
 * 获取响应数据
 * @param {Object} response - API 响应对象
 * @returns {any} 响应数据
 */
export function getResponseData(response) {
  return response && response.data
}

/**
 * 获取错误信息
 * @param {Object} response - API 响应对象
 * @returns {string} 错误信息
 */
export function getErrorMessage(response) {
  return response && (response.message || response.error || '未知错误')
}

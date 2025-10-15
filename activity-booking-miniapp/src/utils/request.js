import config from '@/config/index'

/**
 * HTTP请求封装
 */
class Request {
  constructor() {
    this.baseURL = config.baseURL
    this.timeout = config.timeout
  }

  /**
   * 请求拦截器
   */
  interceptRequest(options) {
    // 获取token
    const token = uni.getStorageSync('token')
    if (token) {
      options.header = {
        ...options.header,
        'Authorization': `Bearer ${token}`
      }
    }
    return options
  }

  /**
   * 响应拦截器
   */
  interceptResponse(response) {
    const { data, statusCode } = response
    
    if (statusCode === 200) {
      return Promise.resolve(data)
    } else if (statusCode === 401) {
      // token失效，跳转登录
      uni.removeStorageSync('token')
      uni.navigateTo({
        url: '/pages/login/login'
      })
      return Promise.reject(new Error('未授权，请重新登录'))
    } else {
      const error = data.message || '请求失败'
      uni.showToast({
        title: error,
        icon: 'none'
      })
      return Promise.reject(new Error(error))
    }
  }

  /**
   * 通用请求方法
   */
  request(options) {
    options.url = this.baseURL + options.url
    options.timeout = this.timeout
    options.header = {
      'Content-Type': 'application/json',
      ...options.header
    }

    // 请求拦截
    options = this.interceptRequest(options)

    return new Promise((resolve, reject) => {
      uni.request({
        ...options,
        success: (res) => {
          this.interceptResponse(res).then(resolve).catch(reject)
        },
        fail: (err) => {
          uni.showToast({
            title: '网络请求失败',
            icon: 'none'
          })
          reject(err)
        }
      })
    })
  }

  get(url, data = {}, options = {}) {
    return this.request({
      url,
      data,
      method: 'GET',
      ...options
    })
  }

  post(url, data = {}, options = {}) {
    return this.request({
      url,
      data,
      method: 'POST',
      ...options
    })
  }

  put(url, data = {}, options = {}) {
    return this.request({
      url,
      data,
      method: 'PUT',
      ...options
    })
  }

  delete(url, data = {}, options = {}) {
    return this.request({
      url,
      data,
      method: 'DELETE',
      ...options
    })
  }
}

export default new Request()


import request from '@/utils/request'

/**
 * 创建预约
 */
export function createBooking(data) {
  return request.post('/bookings', data)
}

/**
 * 获取我的预约列表
 */
export function getMyBookings(params) {
  return request.get('/bookings/my', params)
}

/**
 * 获取预约详情
 */
export function getBookingDetail(id) {
  return request.get(`/bookings/${id}`)
}

/**
 * 取消预约
 */
export function cancelBooking(id) {
  return request.put(`/bookings/${id}/cancel`)
}

/**
 * 签到
 */
export function checkIn(id) {
  return request.put(`/bookings/${id}/checkin`)
}


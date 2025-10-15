import request from '@/utils/request'

/**
 * 获取活动列表
 */
export function getActivityList(params) {
    console.log("getActivityList")
    return request.get('/activities', params)
}

/**
 * 获取活动详情
 */
export function getActivityDetail(id) {
    return request.get(`/activities/${id}`)
}

/**
 * 搜索活动
 */
export function searchActivities(keyword) {
    return request.get('/activities/search', {keyword})
}

/**
 * 获取热门活动
 */
export function getHotActivities() {
    return request.get('/activities/hot')
}


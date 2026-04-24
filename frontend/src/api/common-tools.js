import request from '@/utils/api'

// 首页聚合数据
export function getDashboard() {
  return request({ url: '/common-tools/resources/dashboard/', method: 'get' })
}

// 资源列表
export function getResourceList(params) {
  return request({ url: '/common-tools/resources/', method: 'get', params })
}

// 资源详情
export function getResourceDetail(id) {
  return request({ url: `/common-tools/resources/${id}/`, method: 'get' })
}

// 记录访问
export function recordAccess(id, data = {}) {
  return request({ url: `/common-tools/resources/${id}/access/`, method: 'post', data })
}

// 分类列表
export function getCategories(params) {
  return request({ url: '/common-tools/categories/', method: 'get', params })
}

// 标签列表
export function getTags(params) {
  return request({ url: '/common-tools/tags/', method: 'get', params })
}

// 统计数据
export function getStats() {
  return request({ url: '/common-tools/resources/stats/', method: 'get' })
}

// CRUD
export function createResource(data) {
  return request({ url: '/common-tools/resources/', method: 'post', data })
}

export function updateResource(id, data) {
  return request({ url: `/common-tools/resources/${id}/`, method: 'put', data })
}

export function deleteResource(id) {
  return request({ url: `/common-tools/resources/${id}/`, method: 'delete' })
}

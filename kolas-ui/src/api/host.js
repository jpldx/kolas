// 主机管理
import request from '@/utils/axios'

// 保存
export const save = (data) => {
  return request({
    url: '/host/save',
    method: 'post',
    data
  })
}

// 列表
export const list = (project_id) => {
  return request({
    url: '/host/list/' + project_id,
    method: 'get'
  })
}

// 详情
export const get = (id) => {
  return request({
    url: '/host/get/' + id,
    method: 'get'
  })
}

// 测试连接
export const testConnection = (data) => {
  return request({
    url: '/host/test_connection',
    method: 'post',
    data
  })
}

// 删除
export const del = (id) => {
  return request({
    url: '/host/delete/' + id,
    method: 'delete'
  })
}
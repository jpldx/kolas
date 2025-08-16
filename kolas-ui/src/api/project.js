// 主机管理
import request from '@/utils/axios'

// 保存
export const save = (data) => {
  return request({
    url: '/project/save',
    method: 'post',
    data
  })
}

// 列表
export const list = () => {
  return request({
    url: '/project/list',
    method: 'get'
  })
}

// 详情
export const get = (id) => {
  return request({
    url: '/project/get/' + id,
    method: 'get'
  })
}

// 删除
export const del = (id) => {
  return request({
    url: '/project/delete/' + id,
    method: 'delete'
  })
}
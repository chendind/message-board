import request from '@/api/request'
// 登录接口
export function signIn(data) {
  return request({
    url: '/api/user/signIn',
    method: 'post',
    data: data
  })
}
// 登出接口
export function signOut(data) {
  return request({
    url: '/api/user/signOut',
    method: 'post',
    data: data
  })
}
// 注册接口
export function signUp(data) {
  return request({
    url: '/api/user/signUp',
    method: 'post',
    data: data
  })
}
// 提交留言
export function postComment(data) {
  return request({
    url: '/api/comment',
    method: 'post',
    data: data
  })
}
// 查看所有留言
export function getComments(data) {
  return request({
    url: '/api/comment/tree',
    method: 'get',
    data: data
  })
}
// 获得个人资料
export function getSelf(data) {
  return request({
    url: '/api/user/self',
    method: 'get',
    data: data
  })
}
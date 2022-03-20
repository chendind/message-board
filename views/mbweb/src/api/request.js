import axios from 'axios'
import qs from 'qs'
import VueApp from '@/main.js'

// 创建axios实例
const service = axios.create({
})

// request拦截器
service.interceptors.request.use(
  config => {
    config.transformRequest = [
      function(data) {
        return qs.stringify(data, { arrayFormat: 'repeat' })
      }
    ]
    return config
  },
  error => {
    // Do something with request error
    Promise.reject(error)
  }
)

// respone拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    if (res.code !== 0) {
      if (res.code === 2) {
        if (response.request.responseURL.indexOf('/api/user/self') === -1) {
          VueApp.$store.commit('app/setSignInDialogShow', true)
        }
      } else {
        VueApp.$toast(res.message)
      }
      return Promise.reject(res)
    } else {
      return res
    }
  },
  error => {
    console.log(error.response) // for debug
    const res = error.response.data
    if (res.code !== 0) {
      if (res.code === 2) {
        if (response.request.responseURL.indexOf('/api/user/self') === -1) {
          VueApp.$store.commit('app/setSignInDialogShow', true)
        }
      } else {
        VueApp.$toast(res.message)
      }
      return Promise.reject(res)
    } else {
      return response.data
    }
  }
)

export default service

import { getSelf, signIn, signOut, signUp, getComments } from '@/api'
import VueApp from '@/main.js'
const module = {
  namespaced: true,
  state: {
    user: {},
    signInDialogShow: false,
    signUpDialogShow: false,
    comments: []
  },
  getters: {},
  mutations: {
    setUser(state, data) {
      state.user = data
    },
    setSignInDialogShow(state, data) {
      state.signInDialogShow = data
      if (data) {
        state.signUpDialogShow = false
      }
    },
    setSignUpDialogShow(state, data) {
      state.signUpDialogShow = data
      if (data) {
        state.signInDialogShow = false
      }
    },
    setComments(state, data) {
      state.comments = data
    }
  },
  actions: {
    getSelf({commit}) {
      return getSelf().then(res => {
        commit('setUser', res.data)
      }).catch(res => {
        commit('setUser', null)
      })
    },
    signIn({commit, dispatch}, data) {
      return signIn(data).then(res => {
        dispatch('getSelf')
        commit('setSignInDialogShow', false)
        VueApp.$toast(res.message)
        return res
      })
    },
    signOut({commit, dispatch}, data) {
      return signOut(data).then(res => {
        commit('setUser', null)
        return res
      })
    },
    signUp({commit, dispatch}, data) {
      return signUp(data).then(res => {
        dispatch('getSelf')
        commit('setSignInDialogShow', true)
        VueApp.$toast('注册成功，请您登录')
        return res
      })
    },
    getComments({commit}) {
      return getComments().then(res => {
        commit('setComments', res.data)
        return res
      })
    }
  },
}
export default module
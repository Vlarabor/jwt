import { createStore } from 'vuex'

export default createStore({
  state: {
    "accessToken": "invalid token",
    "refreshToken": "invalid token",
    "loggedIn": false,
  },
  mutations: {
    setAccessToken(state, token) {
      state.accessToken = token
    },
    setRefreshToken(state, token) {
      state.refreshToken = token
    },
    setLoggedIn(state, value) {
      state.loggedIn = value
    }
  },
  actions: {
    loginUser(context, {accessToken, refreshToken}) {
      context.commit('setLoggedIn', true)
      context.commit('setAccessToken', accessToken)
      context.commit('setRefreshToken', refreshToken)
    },
    logoutUser(context) {
      context.commit('setLoggedIn', false)
      context.commit('setAccessToken', "invalid token")
      context.commit('setRefreshToken', "invalid token")
    },
  },
  modules: {
  }
})

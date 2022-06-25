import { createStore } from 'vuex'

export default createStore({
  state: { token: '' },
  getters: { },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem('token')) {
        state.token = localStore.getItem('token')
      } else { state.token = '' }
    },

    setToken(state, token) { state.token = token },

    removeToken(state) { state.token = '' }
  },
  actions: { },
  modules: { }
})

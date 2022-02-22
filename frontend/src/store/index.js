import { createStore } from 'vuex'

const store = createStore({
    state () {
        return {
            mainLoading: true,
        }
    },
    mutations: {
        setMainLoading (state, payload) {
            state.mainLoading = payload
        },
    },
    actions: {
        setMainLoading ({ commit }, payload) {
            if (payload) {
                commit('setMainLoading', true)
            } else {
                setTimeout(() => {
                    commit('setMainLoading', status)
                }, 600)
            }
        },
    }
})

export default store

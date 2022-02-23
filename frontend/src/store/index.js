import { createStore } from 'vuex'
import { getUserInfoAPI } from '../api/user'

const store = createStore({
    state() {
        return {
            mainLoading: true,
            user: {
                username: ''
            }
        }
    },
    mutations: {
        setMainLoading(state, payload) {
            state.mainLoading = payload
        },
        setUser(state, payload) {
            state.user = payload
        }
    },
    actions: {
        setMainLoading({ commit }, payload) {
            if (payload) {
                commit('setMainLoading', true)
            } else {
                setTimeout(() => {
                    commit('setMainLoading', false)
                }, 600)
            }
        },
        getUserInfo({ commit, dispatch }) {
            getUserInfoAPI().then(
                res => commit('setUser', res.data.data)
            ).finally(
                () => dispatch('setMainLoading', false)
            )
        }
    }
})

export default store

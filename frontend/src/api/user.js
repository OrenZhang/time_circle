import http from './index'

export const getUserInfoAPI = () => new Promise((resolve, reject) => {
    http.get(
        '/account/user_info/'
    ).then(res => resolve(res), err => reject(err))
})

export const loginAPI = (data) => new Promise((resolve, reject) => {
    http.post(
        '/account/sign_in/', data
    ).then(res => resolve(res), err => reject(err))
})

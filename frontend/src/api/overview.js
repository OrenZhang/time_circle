import http from './index'

export const overviewCommonAPI = (data) => new Promise((resolve, reject) => {
    http.post(
        '/circle/overview/common/', data
    ).then(res => resolve(res), err => reject(err))
})

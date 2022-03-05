import http from './index'

export const overviewCommonAPI = (data) => new Promise((resolve, reject) => {
    http.post(
        '/circle/overview/common/', data
    ).then(res => resolve(res), err => reject(err))
})

export const overviewDetailAPI = (data) => new Promise((resolve, reject) => {
    http.post(
        '/circle/overview/details/', data
    ).then(res => resolve(res), err => reject(err))
})

export const overviewChartAPI = (data) => new Promise((resolve, reject) => {
    http.post(
        '/circle/overview/chart/', data
    ).then(res => resolve(res), err => reject(err))
})

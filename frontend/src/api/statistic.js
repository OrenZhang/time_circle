import http from './index'

export const yearOptionsAPI = () => new Promise((resolve, reject) => {
    http.get(
        '/circle/statistic/get_valid_year/'
    ).then(res => resolve(res), err => reject(err))
})

export const getStatisticDataAPI = (year) => new Promise((resolve, reject) => {
    http.post(
        '/circle/statistic/info/', { 'year': year }
    ).then(res => resolve(res), err => reject(err))
})


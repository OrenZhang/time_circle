import http from './index'


export const loadLevelDataAPI = (parent_id) => new Promise((resolve, reject) => {
    http.get(
        '/circle/category/' + parent_id + '/level/'
    ).then(res => resolve(res), err => reject(err))
})

export const getCurrentCategoryAPI = (id) => new Promise((resolve, reject) => {
    http.get(
        '/circle/category/' + id + '/'
    ).then(res => resolve(res), err => reject(err))
})

export const createCategoryAPI = (data) => new Promise((resolve, reject) => {
    http.post(
        '/circle/category/', data
    ).then(res => resolve(res), err => reject(err))
})

export const deleteCategoryAPI = (id) => new Promise((resolve, reject) => {
    http.delete(
        '/circle/category/' + id + '/'
    ).then(res => resolve(res), err => reject(err))
})

export const loadCategoriesAPI = () => new Promise((resolve, reject) => {
    http.get(
        '/circle/category/'
    ).then(res => resolve(res), err => reject(err))
})

export const startItemAPI = (data) => new Promise((resolve, reject) => {
    http.post(
        '/circle/item/start/', data
    ).then(res => resolve(res), err => reject(err))
})

export const stopItemAPI = (id, data) => new Promise((resolve, reject) => {
    http.post(
        '/circle/item/' + id + '/stop/', data
    ).then(res => resolve(res), err => reject(err))
})

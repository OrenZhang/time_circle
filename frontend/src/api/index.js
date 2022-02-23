import axios from 'axios'
import globalContext from '../context'
import router from '../router'

const http = axios

http.defaults.timeout = 10000
http.defaults.baseURL = globalContext.backEndUrl
http.defaults.withCredentials = true

http.interceptors.response.use(res => {
    return Promise.resolve(res)
}, err => {
    err = err.response
    if (err.status === 401) {
        router.push({ name: 'Login' })
    }
    return Promise.reject(err)
})

export default http

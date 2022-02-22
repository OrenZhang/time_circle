import axios from 'axios'
import globalContext from '../context'
import store from '../store'

const http = axios

http.defaults.timeout = 10000
http.defaults.baseURL = globalContext.backEndUrl
http.defaults.withCredentials = true

http.interceptors.response.use(res => {
    return Promise.resolve(res)
}, err => {
    err = err.response
    return Promise.reject(err)
})

export default http

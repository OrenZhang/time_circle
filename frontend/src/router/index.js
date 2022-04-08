import * as vueRouter from 'vue-router'
import store from '../store'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('../views/Home.vue')
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/Login.vue')
    },
    {
        path: '/category',
        name: 'Admin',
        component: () => import('../views/Admin.vue')
    },
    {
        path: '/time',
        name: 'Time',
        component: () => import('../views/Time.vue')
    },
    {
        path: '/overview',
        name: 'Overview',
        component: () => import('../views/Overview.vue')
    },
    {
        path: '/statistic',
        name: 'Statistic',
        component: () => import('../views/Statistic.vue')
    },
    {
        path: '/json',
        name: 'Json',
        component: () => import('../views/Json.vue')
    },
    {
        path: '/:pathMatch(.*)*',
        name: '404',
        component: () => import('../components/ErrorPage.vue')
    }
]

const router = vueRouter.createRouter({
    history: vueRouter.createWebHistory(),
    routes
})

router.beforeEach(() => {
    store.dispatch('setMainLoading', true)
})

router.afterEach(() => {
    store.dispatch('setMainLoading', false)
})

export default router

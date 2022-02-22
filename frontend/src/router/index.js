import * as vueRouter from 'vue-router'
import store from '../store'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('../views/Home.vue')
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

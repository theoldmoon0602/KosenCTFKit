import Vue from 'vue/dist/vue.js'
import Router from 'vue-router/dist/vue-router.js'

import index from './pages/index.vue'
import login from './pages/login.vue'
import register from './pages/register.vue'
import challenges from './pages/challenges.vue'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            component: index
        },
        {
            path: '/login',
            component: login
        },
        {
            path: '/register',
            component: register
        },
        {
            path: '/challenges',
            component: challenges
        },
    ]
})

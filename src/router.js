import Vue from 'vue/dist/vue.js'
import Router from 'vue-router/dist/vue-router.js'

import index from './pages/index.vue'
import login from './pages/login.vue'

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
    ]
})

import Vue from 'vue/dist/vue.js'
import Router from 'vue-router/dist/vue-router.js'

import index from './pages/index.vue'
import login from './pages/login.vue'
import register from './pages/register.vue'
import challenges from './pages/challenges.vue'
import scoreboard from './pages/scoreboard.vue'
import user from './pages/user.vue'

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
        {
            path: '/scoreboard',
            component: scoreboard
        },
        {
            path: '/user/:user_id',
            component: user,
            name: 'user'
        },
    ]
})

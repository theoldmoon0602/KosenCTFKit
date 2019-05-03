import Vue from 'vue/dist/vue.js'
import App from './app.vue'
import router from './router.js'
import store from './store'
import axios from 'axios'


import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.css'


let vue = new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
})

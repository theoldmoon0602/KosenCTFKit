import Vue from 'vue/dist/vue.js'
import App from './app.vue'
import router from './router.js'
import store from './store'
import axios from 'axios'

import BootstrapVue from 'bootstrap-vue'

Vue.use(BootstrapVue)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'



let vue = new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
})

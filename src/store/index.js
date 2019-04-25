import Vue from 'vue/dist/vue.js'
import Vuex from 'vuex'

import user from './user.js'
import team from './team.js'
import messages from './messages.js'

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        messages,
        user,
        team,
    }
})

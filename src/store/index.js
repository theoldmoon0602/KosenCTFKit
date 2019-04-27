import Vue from 'vue/dist/vue.js'
import Vuex from 'vuex'
import axios from 'axios'

import user from './user.js'
import team from './team.js'
import messages from './messages.js'
import challenges from './challenges.js'

Vue.use(Vuex)

export default new Vuex.Store({
    actions: {
        update(context) {
            return axios.get('/update')
                .then(r => {
                    if (r.data['is_login']) {
                        context.commit('setUser', r.data['user'])
                        context.commit('setTeam', r.data['team'])
                        context.commit('setChallenges', r.data['challenges'])
                    } else {
                    }
                })
        },
    },
    modules: {
        messages,
        user,
        team,
        challenges,
    }
})

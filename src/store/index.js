import Vue from 'vue/dist/vue.js'
import Vuex from 'vuex'
import axios from 'axios'

import user from './user.js'
import team from './team.js'
import messages from './messages.js'
import challenges from './challenges.js'
import ctf from './ctf.js'

Vue.use(Vuex)

export default new Vuex.Store({
    actions: {
        update(context) {
            return axios.get('/update')
                .then(r => {
                    if (r.data['is_login']) {
                        context.commit('setUser', r.data['user'])
                        context.commit('setTeam', r.data['team'])
                    }
                    context.commit('setUsers', r.data['users'])
                    context.commit('setTeams', r.data['teams'])
                    context.commit('setScoreboard', r.data['scoreboard'])
                    context.commit('setChallenges', r.data['challenges'])
                    context.commit('setCTFInfo', {
                        name: r.data['ctf_name'],
                        ctf_open: r.data['ctf_open'],
                        ctf_frozen: r.data['ctf_frozen'],
                        register_open: r.data['register_open'],
                    })
                })
        },
    },
    modules: {
        ctf,
        messages,
        user,
        team,
        challenges,
    }
})

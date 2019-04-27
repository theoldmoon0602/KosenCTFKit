import axios from 'axios'
import Vue from 'vue/dist/vue.js'

export default {
    state: {
        challenges: []
    },
    getters: {
        getChallenges(state) {
            return state.challenges
        },
        getChallengesWithCategory(state) {
            let cs = {};
            for (let c of state.challenges) {
                if (! cs[c.category]) {
                    cs[c.category] = []
                }
                cs[c.category].push(c)
            }
            for (let i = 0; i < cs.length; i++) {
                cs[i].sort()
            }
            return cs
        },
    },
    mutations: {
        setChallenges(state, challenges) {
            Vue.set(state, 'challenges', challenges)
        },
    },
    actions: {
        submit(context, submitinfo) {
            return axios.post('/submit', submitinfo, {
                withCredentials: true
            })
                .then(r => {
                    context.dispatch('addMessage', r.data['message'])
                    context.dispatch('update')
                    return r
                })
                .catch(e => {
                    context.dispatch('addError', e.response.data['message'])
                    return false
                })
        }
    }
}


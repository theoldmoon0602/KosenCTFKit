import axios from 'axios'
import Vue from 'vue'

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
            for (let c of Object.values(state.challenges)) {
                if (! cs[c.category]) {
                    cs[c.category] = []
                }
                cs[c.category].push(c)
            }
            for (let k of Object.keys(cs)) {
                cs[k].sort((a,b) => {
                    return a.score - b.score
                })
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
                    context.dispatch('setMessage', r.data['message'])
                    context.dispatch('update')
                    return r
                })
                .catch(e => {
                    context.dispatch('setError', e.response.data['message'])
                    return false
                })
        }
    }
}


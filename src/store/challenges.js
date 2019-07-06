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


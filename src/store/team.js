import axios from 'axios';

export default {
    state: {
        id: undefined,
        name: '',
        token: '',
        members: [],
        score: 0,
        solved: [],
    },
    getters: {
        getTeam(state) {
            return state
        },
        getTeamSolved(state) {
            return state.solved
        },
    },
    mutations: {
        setTeam(state, team) {
            Object.assign(state, team)
        }
    },
    actions: {
        regenerate(context) {
            return axios.post('/regenerate', {}, {
                withCredentials: true
            }).then(r => {
                context.dispatch('addMessage', 'Teamtoken is regenerated')
                context.dispatch('update')
            })
        }
    }
}

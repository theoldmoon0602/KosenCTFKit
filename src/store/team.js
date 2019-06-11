import axios from 'axios';

export default {
    state: {
        id: undefined,
        name: '',
        token: '',
    },
    getters: {
        getTeam(state) {
            return state
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
                context.dispatch('setMessage', 'Teamtoken is re-generated')
                context.dispatch('update')
            })
        }
    }
}

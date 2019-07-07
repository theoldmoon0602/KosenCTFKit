import axios from 'axios'

export default {
    state: {
        name: undefined,
        ctf_open: false,
        ctf_frozen: false,
        start_at: 0,
        end_at: 0,
        register_open: false,
        users: [],
        teams: [],
        submissions: [],
    },
    getters: {
        getCTFName(state) {
            return state.name
        },
        getUsers(state) {
            return state.users
        },
        getCTFStart(state) {
            return state.start_at
        },
        getCTFEnd(state) {
            return state.end_at
        },
        getTeams(state) {
            return state.teams
        },
        isFrozen(state) {
            return state.ctf_frozen;
        },
        isOpen(state) {
            return state.ctf_open;
        },
        registerOpen(state) {
            return state.register_open;
        },
        getSubmissions(state, submissions) {
            return state.submissions
        }
    },
    mutations: {
        setCTFInfo(state, info) {
            state.name = info.name
            document.title = state.name
            state.ctf_open = info.ctf_open
            state.ctf_frozen = info.ctf_frozen
            state.register_open = info.register_open
            state.start_at = new Date(info.start_at)
            state.end_at = new Date(info.end_at)
        },
        setUsers(state, users) {
            Object.assign(state.users, users)
        },
        setTeams(state, teams) {
            Object.assign(state.teams, teams)
        },
        setSubmissions(state, submissions) {
            Object.assign(state.submissions, submissions)
        }
    },
    actions: {
        getSubmissions(context) {
            return axios.get('/submissions')
                .then(r => {
                    context.commit('setSubmissions', r.data)
                    return r
                })
                .catch(e => {
                    context.dispatch('setError', e.response.data['message'])
                    return false
                })
        }
    }
}

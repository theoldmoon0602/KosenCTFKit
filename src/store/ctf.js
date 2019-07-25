import axios from 'axios'
import Vue from 'vue'

export default {
    state: {
        name: undefined,
        flag_format: "",
        ctf_open: false,
        ctf_frozen: false,
        score_expr: "",
        start_at: 0,
        end_at: 0,
        register_open: false,
        users: {},
        teams: {},
        submissions: {},
    },
    getters: {
        getCTFName(state) {
            return state.name
        },
        getFlagFormat(state){
            return state.flag_format
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
        getScoreExpr(state) {
            return state.score_expr
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
        getSubmissions(state) {
            return state.submissions
        }
    },
    mutations: {
        setCTFInfo(state, info) {
            state.name = info.name
            state.flag_format = info.flag_format
            document.title = state.name
            state.ctf_open = info.ctf_open
            state.ctf_frozen = info.ctf_frozen
            state.score_expr = info.score_expr
            state.register_open = info.register_open
            state.start_at = new Date(info.start_at)
            state.end_at = new Date(info.end_at)
        },
        setUsers(state, users) {
            Vue.set(state, 'users', users)
        },
        setTeams(state, teams) {
            Vue.set(state, 'teams', teams)
        },
        setSubmissions(state, submissions) {
            Vue.set(state, 'submissions', submissions)
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

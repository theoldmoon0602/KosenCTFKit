import axios from 'axios'

export default {
    state: {
        id: null,
        name: null,
        team: null,
        score: 0,
        solved: [],
    },
    getters: {
        isLogin(state) {
            return state.id >= 0
        }
    },
    mutations: {
        setUser(state, user) {
            Object.assign(state, user)
        },
        logout(state) {
            state.id = undefined
            state.name = ''
        }
    },
    actions: {
        login(context, userinfo) {
            return axios.post('/login', userinfo)
                .then(r => {
                    context.dispatch('addMessage', 'Login Succeeded')
                    context.dispatch('update')
                    return r
                })
                .catch(e => {
                    context.dispatch('addError', e.response.data['message'])
                    return false
                })
        },
        register(context, userinfo) {
            return axios.post('/register', userinfo)
                .then(r => {
                    context.dispatch('addMessage', 'The user "'+ r.data['name'] + '" has just registered.')
                    return r
                })
                .catch(e => {
                    context.dispatch('addError', e.response.data['message'])
                    return false
                })
        },
        registerTeam(context, teaminfo) {
            return axios.post('/register-team', teaminfo)
                .then(r => {
                    context.dispatch('addMessage', 'The team "'+ teaminfo.teamname +'" has just registered. Next, register as an user')
                    return r
                })
                .catch(e => {
                    context.dispatch('addError', e.response.data['message'])
                    return false
                })
        },
        logout(context) {
            return axios.get('/logout').then(r => {
                context.commit('logout')
                context.dispatch('addMessage', 'Logged out')
                return true
            })
        },
    }
}

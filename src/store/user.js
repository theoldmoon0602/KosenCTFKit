import axios from 'axios'

export default {
    state: {
        id: undefined,
        name: '',
        score: 0,
        validScore: 0,
        solved: [],
        validSolved: [],
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
        getMe(context) {
            return axios.get('/me', {withCredentials: true})
                .then(r => {
                    if (r.data) {
                        context.commit('setUser', r.data['user'])
                        if (r.data['user']['team']) {
                            context.commit('setTeam', r.data['team'])
                        }
                    }
                })
        },
        login(context, userinfo) {
            return axios.post('/login', userinfo)
                .then(r => {
                    context.dispatch('addMessage', 'Login Succeeded')
                    context.dispatch('getMe')
                })
                .catch(e => {
                    if (e.response.data) {
                        context.dispatch('addError', e.response.data['message'])
                    }
                })
        },
        register(context, userinfo) {
            return axios.post('/register', userinfo)
                .then(r => {
                    if (r.data) {
                        context.dispatch('addMessage', 'The user "'+ r.data['name'] + '" has just registered.')
                    }
                })
                .catch(e => {
                    if (e.response.data) {
                        context.dispatch('addError', e.response.data['message'])
                    }
                })
        },
        registerTeam(context, teaminfo) {
            return axios.post('/register-team', teaminfo)
                .then(r => {
                    if (r.data) {
                        context.dispatch('addMessage', 'The team "'+ teaminfo.teamname +'" has just registered. Next, register as an user')
                    }
                })
                .catch(e => {
                    if (e.response.data) {
                        context.dispatch('addError', e.response.data['message'])
                    }
                })
        },
        logout(context) {
            return axios.get('/logout').then(r => {
                context.commit('logout')
                context.dispatch('addMessage', 'Logged out')
            })
        },
    }
}

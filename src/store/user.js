import axios from 'axios'

export default {
    state: {
        id: null,
        name: null,
        team: null,
        team_id: null,
    },
    getters: {
        isLogin(state) {
            return Number.isInteger(state.id)
        },
        getCurrentUser(state) {
            return state
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
                    context.dispatch('setMessage', 'Login Succeeded')
                    context.dispatch('update')
                    return r
                })
                .catch(e => {
                    context.dispatch('setError', e.response.data['message'])
                    return false
                })
        },
        register(context, userinfo) {
            return axios.post('/register', userinfo)
                .then(r => {
                    context.dispatch('setMessage', 'The user "'+ r.data['name'] + '" has just registered.')
                    return r
                })
                .catch(e => {
                    context.dispatch('setError', e.response.data['message'])
                    return false
                })
        },
        registerTeam(context, teaminfo) {
            return axios.post('/register-team', teaminfo)
                .then(r => {
                    context.dispatch('setMessage', 'The team "'+ teaminfo.teamname +'" has just registered. Next, register as an user')
                    return r
                })
                .catch(e => {
                    context.dispatch('setError', e.response.data['message'])
                    return false
                })
        },
        updatePassword(context, passwordinfo) {
            return axios.post('/password-update', passwordinfo, {
                withCredentials: true
            }).then(r => {
                context.dispatch('setMessage', 'Password Updated')
                return r
            }).catch(e => {
                context.dispatch('setError', e.response.data['message'])
                return false
            })
        },
        uploadIcon(context, icon) {
            return axios.post('/upload-icon', {
                icon: icon
            }, {
                withCredentials: true
            }).then(r => {
                context.dispatch('setMessage', 'Your Icon Uploaded Successfully')
                context.dispatch('update')
                return r
            }).catch(e => {
                context.dispatch('setError', e.response.data['message'])
                return false
            })
        },
        logout(context) {
            return axios.get('/logout').then(r => {
                context.commit('logout')
                context.dispatch('setMessage', 'Logged out')
                return true
            })
        },
    }
}

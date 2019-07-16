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
                    context.dispatch('setMessage', 'Successfully logged in')
                    context.dispatch('update')
                    return r
                })
                .catch(e => {
                    context.dispatch('setError', e.response.data['message'])
                    return false
                })
        },
        register(context, userninfo) {
            return axios.post('/register', userninfo)
                .then(r => {
                    context.dispatch('setMessage', 'You has just registered. Please check your e-mail box to confirm')
                    return r
                })
                .catch(e => {
                    context.dispatch('setError', e.response.data['message'])
                    return false
                })
        },
        confirm(context, token) {
            return axios.post('/confirm', token)
                .then(r => {
                    context.dispatch('setMessage', 'Confirmed')
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

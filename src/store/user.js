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
        }
    },
    actions: {
    }
}

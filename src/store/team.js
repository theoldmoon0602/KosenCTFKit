export default {
    state: {
        id: undefined,
        name: '',
        members: [],
        score: 0,
        validScore: 0,
        solved: [],
        validSolved: [],
    },
    getters: {
    },
    mutations: {
        setTeam(state, team) {
            Object.assign(state, team)
        }
    },
    actions: {
    }
}

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
        getTeamSolved(state) {
            return state.solved
        }
    },
    mutations: {
        setTeam(state, team) {
            Object.assign(state, team)
        }
    },
    actions: {
    }
}

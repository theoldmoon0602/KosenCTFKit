import Vue from 'vue';

export default {
    state: {
        name: undefined,
        ctf_open: false,
        ctf_frozen: false,
        register_open: false,
        users: [],
        teams: [],
        scoreboard: []
    },
    getters: {
        getScoreboard(state) {
            return state.scoreboard;
        },
        getCTFName(state) {
            return state.name
        },
        getUsers(state) {
            return state.users
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
        }
    },
    mutations: {
        setCTFInfo(state, info) {
            state.name = info.name
            document.title = state.name
            state.ctf_open = info.ctf_open
            state.ctf_frozen = info.ctf_frozen
            state.register_open = info.register_open
        },
        setUsers(state, users) {
            Object.assign(state.users, [])
            for (let [i, user] in users) {
                Vue.set(state.users, i, user);
            }
        },
        setTeams(state, teams) {
            Object.assign(state.users, [])
            Object.assign(state.teams, teams)
        },
        setScoreboard(state, scoreboard) {
            Object.assign(state.scoreboard, scoreboard)
        },
    },
    actions: {
    }
}

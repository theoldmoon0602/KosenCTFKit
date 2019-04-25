import Vue from 'vue/dist/vue.js'
import Vuex from 'vuex'

Vue.use(Vuex)

const messages = {
    state: {
        messages: [],
        errors: []
    },
    mutations: {
        addMessage(state, message) {
            state.messages.push(message)
        },
        deleteMessage(state, message) {
            state.messages = state.messages.filter(m => m != message)
        },
        addError(state, error) {
            state.errors.push(error)
        },
        deleteError(state, error) {
            state.errors = state.errors.filter(e => e != error)
        },
    },
    actions: {
        addMessage(context, message) {
            context.commit('addMessage', message);
            setTimeout(() => {
                context.commit('deleteMessage', message)
            }, 10000);
        },
    },
}

export default new Vuex.Store({
    modules: {
        messages
    }
})

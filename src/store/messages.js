export default {
    state: {
        messages: [],
        errors: []
    },
    getters: {
        getMessages(state) {
            return state.messages
        },
        getErrors(state) {
            return state.errors
        },
    },
    mutations: {
        addMessage(state, message) {
            if (!state.messages.includes(message)) {
                state.messages.push(message)
            }
        },
        deleteMessage(state, message) {
            state.messages = state.messages.filter(m => m != message)
        },
        addError(state, error) {
            if (!state.errors.includes(error)) {
                state.errors.push(error)
            }
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
        addError(context, error) {
            context.commit('addError', error);
            setTimeout(() => {
                context.commit('deleteError', error)
            }, 10000);
        },
    },
}

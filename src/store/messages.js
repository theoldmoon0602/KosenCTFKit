export default {
    state: {
        message: '',
        is_error: false
    },
    getters: {
        getMessage(state) {
            return {
                content: state.message,
                is_error: state.is_error
            }
        },
    },
    mutations: {
        setMessage(state, m) {
            state.message = m.message;
            state.is_error = m.is_error;
        },
        deleteMessage(state, message) {
            if (state.message == message) {
                state.message = '';
            }
        }
    },
    actions: {
        setMessage(context, message) {
            context.commit('setMessage', {message: message, is_error: false});
            setTimeout(() => {
                context.commit('deleteMessage', message)
            }, 10000);
        },
        setError(context, message) {
            context.commit('setMessage', {message: message, is_error: true});
            setTimeout(() => {
                context.commit('deleteMessage', message)
            }, 10000);
        }
    },
}

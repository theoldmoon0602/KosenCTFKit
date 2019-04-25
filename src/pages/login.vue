<template lang="pug">
    .rows
        form.col-12.col-lg-8.offset-lg-2(@submit.prevent="login")
            .form-group
                label.d-block(for="username") username
                input#username(type=text, v-model="username", required, placeholder="MAKABEE", class="form-control")
            .form-group
                label.d-block(for="password") password
                input#password(type="password", v-model="password", required, class="form-control")
            button.btn.btn-primary(type="submit") Login


</template>

<script>
import Vue from 'vue/dist/vue.js'
import axios from 'axios'
export default Vue.extend({
    data() {
        return {
            username: '',
            password: ''
        }
    },
    methods: {
        login() {
            axios.post('/login', {
                username: this.username,
                password: this.password
            })
                .then(r => {
                    this.$store.dispatch('addMessage', 'Login Succeeded')
                    this.$store.commit('setUser', r.data['user'])
                    if (r.data['user']['team']) {
                        this.$store.commit('setTeam', r.data['team'])
                    }
                    this.$router.push('/')
                })
                .catch(e => {
                    if (e.response.data) {
                        this.$store.dispatch('addError', e.response.data['message'])
                    }
                })

        }
    },
})
</script>


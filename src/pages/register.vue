<template lang="pug">
    .rows.col-12.col-lg-8.offset-lg-2
        h3.h3 Team Registration
        form(@submit.prevent="registerTeam")
            .form-group
                label.d-block(for="teamname") teamname
                input#teamname(type="text", v-model="teamname", required, placeholder="ESCape", class="form-control")
            button.btn.btn-primary(type="submit") Register Team

        h3.h3 User Registration
        form(@submit.prevent="registerUser")
            .form-group
                label.d-block(for="teamtoken") teamtoken
                input#teamtoken(type="text", v-model="teamtoken", required, class="form-control")
            .form-group
                label.d-block(for="username") username
                input#username(type=text, v-model="username", required, placeholder="MAKABEE", class="form-control")
            .form-group
                label.d-block(for="password") password
                input#password(type="password", v-model="password", required, class="form-control")
            button.btn.btn-primary(type="submit") Register User

</template>

<script>
import Vue from 'vue/dist/vue.js'
import axios from 'axios'
export default Vue.extend({
    data() {
        return {
            teamname: '',
            teamtoken: '',
            username: '',
            password: '',
        }
    },
    methods: {
        registerTeam() {
            axios.post('/register-team', {
                teamname: this.teamname,
            })
                .then(r => {
                    if (r.data) {
                        this.teamtoken = r.data['token']
                        this.$store.dispatch('addMessage', 'The team "'+ this.teamname +'" has just registered. Next, register as an user')
                    }
                })
                .catch(e => {
                    if (e.response.data) {
                        this.$store.dispatch('addError', e.response.data['message'])
                    }
                })
        },
        registerUser() {
            axios.post('/register', {
                username: this.username,
                token: this.teamtoken,
                password: this.password,
            })
                .then(r => {
                    if (r.data) {
                        this.$store.dispatch('addMessage', 'The user "'+ r.data['name'] + '" has just registered.')
                        this.$router.push('/login')
                    }
                })
                .catch(e => {
                    console.log(e)
                    if (e.response.data) {
                        this.$store.dispatch('addError', e.response.data['message'])
                    }
                })
        },
    },
})
</script>


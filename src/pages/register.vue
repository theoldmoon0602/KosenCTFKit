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
            console.log(this.teamname)
            this.$store.dispatch('registerTeam', {
                teamname: this.teamname
            }).then(r => {
                if (r.data) {
                    this.teamtoken = r.data['token']
                }
            })
        },
        registerUser() {
            this.$store.dispatch('register', {
                username: this.username,
                password: this.password,
                token: this.teamtoken,
            })
                .then(r => {
                    if (r) {
                        this.$router.push('/login')
                    }
                })
        },
    },
})
</script>


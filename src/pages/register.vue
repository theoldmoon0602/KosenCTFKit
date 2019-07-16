<template lang="pug">
    .rows.col-12.col-lg-8.offset-lg-2
        h3 Registration
        form(@submit.prevent="register")
            .form-group
                label.d-block(for="username") username
                input#username(type="text" v-model="username" required placeholder="username" class="form-control")
            .form-group
                label.d-block(for="email") email
                input#email(type="email" v-model="email" required placeholder="email" class="form-control")
            .form-group
                label.d-block(for="password") password
                input#password(type="password" v-model="password" required class="form-control" placeholder="password")
            .row
                .col-6
                    h4 Create a new team
                    .form-group
                        label.d-block(for="teamname") teamname
                        input#teamname(type="text" v-model="teamname" class="form-control" placeholder="teamname")
                .col-6
                    h4 Join to the existing team
                    .form-group
                        label.d-block(for="teamtoken") teamtoken
                        input#teamtoken(type="text" v-model="teamtoken" class="form-control" placeholder="teamtoken")

            button.btn.btn-primary.float-right(type="submit") Register

</template>

<script>
import Vue from 'vue'
import axios from 'axios'
export default Vue.extend({
    data() {
        return {
            teamname: '',
            teamtoken: '',
            email: '',
            username: '',
            password: '',
        }
    },
    methods: {
        register() {
            if ((this.teamname.length > 0 && this.teamtoken.length > 0) ||
            (this.teamname.length == 0 && this.teamtoken.length == 0)) {
                this.$store.dispatch('setError', 'You should enter either teamname or teamtoken')
                return
            }

            this.$store.dispatch('register', {
                teamname: this.teamname,
                teamtoken: this.teamtoken,
                username: this.username,
                email: this.email,
                password: this.password,
            }).then(r => {
            })
        }
    },
})
</script>


<template lang="pug">
    .rows
        form.col-12.col-lg-8.offset-lg-2(@submit.prevent="login")
            .form-group
                label.d-block(for="username") username
                input#username(type="text" v-model="username" required placeholder="username" class="form-control")
            .form-group
                label.d-block(for="password") password
                input#password(type="password" v-model="password" required class="form-control" placeholder="password")
            button.btn.btn-primary(type="submit") Login


</template>

<script>
import Vue from 'vue'
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
            this.$store.dispatch('login', {
                username: this.username,
                password: this.password
            }).then(r => {
                if (r) {
                    this.$router.push('/')
                }
            })
        }
    },
})
</script>


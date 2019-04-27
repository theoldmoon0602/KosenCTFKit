<template lang="pug">
    .container
        h1.display-4.text-center
            router-link(to="/") KosenCTFKit
        ul.nav.nav-pills.nav-justified
            li.nav-item
                router-link(to="/") About
            li.nav-item
                router-link(to="/") Scoreboard
            template(v-if="login")
                li.nav-item
                    router-link(to="/challenges") Challenges
                li.nav-item
                    router-link(to="/") {{ user.name }}
                li.nav-item
                    a(href="#", @click="logout") Logout
            template(v-else)
                li.nav-item
                    router-link(to="/login") Login
                li.nav-item
                    router-link(to="/register") Register
        div.alert.alert-dismissible.alert-info(v-for="m in messages") {{ m }}
        div.alert.alert-dismissible.alert-danger(v-for="e in errors") {{ e }}
        router-view
</template>

<script>
import Vue from 'vue/dist/vue.js'
import axios from 'axios'
export default Vue.extend({
    mounted() {
        this.$store.dispatch('update')

        // polling
        this.$store.dispatch('update')
        setInterval(() => {
            this.$store.dispatch('update')
        }, 1000 * 30)
    },
    methods: {
        logout() {
            this.$store.dispatch('logout')
                .then(r => {
                    this.$router.push('/')
                })
        }
    },
    computed: {
        messages() {
            return this.$store.getters.getMessages;
        },
        errors() {
            return this.$store.getters.getErrors;
        },
        login() {
            return this.$store.getters.isLogin;
        },
        user() {
            return this.$store.state.user;
        }
    },
})
</script>


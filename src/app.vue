<template lang="pug">
    .container
        h1.display-4.text-center
            router-link(to="/") {{ ctfname }}
        nav.navbar.navbar-expand-md
            button.navbar-toggler.navbar-light(type="button" data-toggle="collapse" data-target="#navbar" aria-controls="navbar" aria-expand="false")
                span.navbar-toggler-icon
            .collapse.navbar-collapse#navbar
                ul.navbar-nav.mr-auto.mt-2.mt-lg-0
                    li.nav-item
                        router-link.nav-link(to="/") About
                    li.nav-item
                        router-link.nav-link(to="/scoreboard") Scoreboard
                    li.nav-item
                        router-link.nav-link(to="/players") Players
                    template(v-if="login")
                        li.nav-item
                            router-link.nav-link(to="/challenges") Challenges
                ul.navbar-nav
                    template(v-if="login")
                        li.nav-item
                            router-link.nav-link(:to="'/user/' + user.id") {{ user.name }}
                        li.nav-item(v-if="user.team")
                            router-link.nav-link(:to="'/team/' + user.team_id") {{ user.team }}
                        li.nav-item
                            a.nav-link(href="#", @click="logout") Logout
                    template(v-else)
                        li.nav-item
                            router-link.nav-link(to="/login") Login
                        li.nav-item(v-if="registerOpen")
                            router-link.nav-link(to="/register") Register

        .alert.alert-danger(v-if="!isOpen") CTF IS CLOSED
        .alert.alert-danger(v-if="isFrozen") SCOREBOARD IS FROZEN
        .alert.alert-dismissible.alert-info(v-for="m in messages") {{ m }}
        .alert.alert-dismissible.alert-danger(v-for="e in errors") {{ e }}
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
            return this.$store.getters.getUser;
        },
        ctfname() {
            return this.$store.getters.getCTFName;
        },
        isOpen() {
            return this.$store.getters.isOpen;
        },
        isFrozen() {
            return this.$store.getters.isFrozen;
        },
        registerOpen() {
            return this.$store.getters.registerOpen;
        }
    },
})
</script>

<style lang="scss">
h1,h2,h3,h4 {
    margin-top: 20px !important;
}
.nav-link {
    font-size: 1.5rem !important;
}
.icon {
    max-width: 256px;
}
</style>

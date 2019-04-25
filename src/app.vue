<template lang="pug">
    .container
        // b-alert(variant="danger", dismissieble, v-for="e in errors") {{ e }}
        h1.display-4.text-center
            router-link(to="/") KosenCTFKit
        ul.nav.nav-pills.nav-justified
            li.nav-item
                router-link(to="/") About
            li.nav-item
                router-link(to="/") Scoreboard
            li.nav-item
                router-link(to="/") Challenges
            template(v-if="login")
                li.nav-item
                    router-link(to="/") {{ user.name }}
            template(v-else)
                li.nav-item
                    router-link(to="/login") Login
                li.nav-item
                    router-link(to="/register") Register
        div.alert.alert-info(v-for="m in messages") {{ m }}
        div.alert.alert-danger(v-for="e in errors") {{ e }}
        router-view
</template>

<script>
import Vue from 'vue/dist/vue.js'
import axios from 'axios'
export default Vue.extend({
    mounted() {
        axios.get('/me', {withCredentials: true})
            .then(r => {
                if (r.data) {
                    this.$store.commit('setUser', r.data['user'])
                    if (r.data['user']['team']) {
                        this.$store.commit('setTeam', r.data['team'])
                    }
                }
            })
            .catch(e => {
                console.log(e.response.data)
            })

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


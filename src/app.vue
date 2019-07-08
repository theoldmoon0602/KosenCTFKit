<template lang="pug">
    .container
        transition(name="fade")
            div.loading(v-if="ctfname === undefined")
                img(src="./penguin.png")
                p LOADING...
        transition(name="fade")
            div(v-if="ctfname")
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

                .alert.alert-danger(v-if="!isConnected") SERVER CONNECTION MISSING
                .alert.alert-danger(v-if="!isOpen") CTF IS CLOSED
                .alert.alert-danger(v-if="isFrozen") SCOREBOARD IS FROZEN
                transition(name="msg")
                    div.message(v-if="message.content")
                        p(v-bind:class="{error : message.is_error}") {{message.content}}
                        img(src="mouse.png")
                router-view
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
export default Vue.extend({
    mounted() {
        // polling
        this.$store.dispatch('update')
        setInterval(() => {
            this.$store.dispatch('update')
        }, 1000 * 30) // every 30 seconds

        this.$store.dispatch('getSubmissions')
        setInterval(() => {
            this.$store.dispatch('getSubmissions')
        }, 1000*60*10)  // every 10 minutes
    },
    methods: {
        hi() {
            console.log('hi')
        },
        logout() {
            this.$store.dispatch('logout')
                .then(r => {
                    this.$router.push('/')
                })
        }
    },
    computed: {
        message() {
            return this.$store.getters.getMessage;
        },
        login() {
            return this.$store.getters.isLogin;
        },
        user() {
            return this.$store.getters.getCurrentUser;
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
        },
        isConnected() {
            return this.$store.getters.isConnected;
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
input[type=text], input[type=password] {
    &:focus {
        background-color: #fff;
    }
    background-color: #fff;
    text-align: center;
    border-radius: 0;
}
</style>

<style scoped>
@media (min-width: 768px) {
    #navbar .router-link-exact-active::before {
        content: "";
        background-image: url(./penguin.png);
        background-size: cover;
        display: inline-block;
        width: 1.5em;
        height: 1.5em;
        float: left;
    }
}
.loading {
    display: flex;
    justify-content: center;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    flex-direction: column
}
.loading img {
    animation: pulse 400ms ease infinite 0s;
    display: block;
    margin: 0 auto;
    max-height: 30vh;
}
.loading p {
    text-align: center;
    font-weight: bold;
    font-size: larger;
}
@keyframes pulse {
    to {
        transform: scale(1.2);
    }
}
.fade-enter-active {
    transition: opacity 1s;
    opacity: 1;
}
.fade-leave-active {
    transition: opacity 0.4s;
    opacity: 0;
}
.msg-enter-active, .msg-leave-active {
  transform: translate(0px, 0px);
  transition: transform 225ms cubic-bezier(0, 0, 0.2, 1) 0ms;
}

.msg-enter, .msg-leave-to {
  transform: translateX(100vh);
}
.message {
    position: fixed;
    bottom: 0;
    right: 0;
    z-index: 99999;
}
.message p {
    position: relative;
    max-width: 200px;
    background: #fff;
    border: 5px solid #bbb;
    padding: 10px;
    top: 20px;
}
.message p.error {
    border-color: #f99;
}
.message img {
    max-width: 100px;
    display: block;
    margin-left: auto;
}
</style>

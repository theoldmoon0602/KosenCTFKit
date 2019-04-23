<template lang="pug">
    b-container
        h1.display-4.text-center
            b-link(to="/") KosenCTFKit
        b-nav(pills justified)
            b-nav-item(to="/") About
            b-nav-item(to="/") Scoreboard
            b-nav-item(to="/") Challenges
            b-nav-item(to="/login") Login
            b-nav-item(to="/register") Register
        router-view
</template>

<script>
import Vue from 'vue/dist/vue.js'
export default Vue.extend({})
</script>


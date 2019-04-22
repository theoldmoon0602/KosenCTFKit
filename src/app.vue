<template lang="pug">
    div
        p app.vue
        ul
            li
                router-link(to="/") index
            li
                router-link(to="/login") login
        router-view
</template>

<script>
import Vue from 'vue/dist/vue.js'
export default Vue.extend({})
</script>


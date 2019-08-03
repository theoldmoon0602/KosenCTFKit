<template lang="pug">
    div
        h1 {{ctfname}}

        div
            img(src="../neko.png" style="display: block; margin: 0 auto;")


        p.text-center.font-weight-bold
            | Join in our&nbsp;
            a(:href="invite_url") slack

        h2 Sponsors
        .row.justify-content-center
            div.col-4
                img(src="../sponserhorse.png" style="width: 100%;")
            div.col-4
                img(src="../sponserhorse256.png" style="width: 100%;")
            div.col-4
                img(src="../sponserhorse.png" style="width: 100%;")

</template>

<script>
import Vue from 'vue'
export default Vue.extend({
    computed: {
        ctfname() {
            return this.$store.getters.getCTFName
        },
        invite_url() {
            return this.$store.getters.getInviteURL
        }
    },
})
</script>

<style scoped>
</style>

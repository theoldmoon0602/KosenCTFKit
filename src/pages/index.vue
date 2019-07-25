<template lang="pug">
    div
        h1 {{ctfname}}

        div
            img(src="../neko.png" style="display: block; margin: 0 auto;")


        p.text-center.font-weight-bold
            | Join in our&nbsp;
            a(href="#") slack

        h2 Sponsors
        .row
            div.col-6
                img(src="../sponserhorse.png" style="width: 100%;")
            div.col-6
                img(src="../sponserhorse.png" style="width: 100%;")
            div.col-6
                img(src="../sponserhorse.png" style="width: 100%;")

</template>

<script>
import Vue from 'vue'
export default Vue.extend({
    computed: {
        ctfname() {
            return this.$store.getters.getCTFName
        }
    },
})
</script>

<style scoped>
</style>

<template lang="pug">
    div
        h1 KosenCTF

        div
            img(src="./neko.png" style="display: block; margin: 0 auto;")

        h2 About
        ul
            li KosenCTF is a web-based jeopardy style CTF.
            li The competition is held from 2019-01-01 00:00:00 to 2020-01-01 00:00:00 (JST).
            li The flag format is KosenCTF{[A-Za-z0-9_- !?#]+}, unless otherwise specified.
            li
                | All challenges have dynamic score value, which calculated by following formula.
                pre
                    code dynamic_score = max(200, (base_score**2) / (base_score + (base_score/10) * (0 if solve_num == 1 else solve_num)))
            li There is no limit in the number of people participating per team.
            li There is no prize.
            li
                | If you have any questions during the contest, please contact to admin from&nbsp;
                a(href="#") here
                | .

        h2 Prohibited matters
        ul
            li Don’t share flags or hints with any other teams.
            li Don’t attack our score server.
            li Do not DoS to any targets.
</template>

<script>
import Vue from 'vue'
export default Vue.extend({})
</script>

<style scoped>
</style>

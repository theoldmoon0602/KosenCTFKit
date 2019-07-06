<template lang="pug">
    div
        h1 KosenCTF

        div
            img(src="../neko.png" style="display: block; margin: 0 auto;")

        h2 About
        ul
            li KosenCTF is an online jeopardy-style CTF.
            li The competition will be held from 2019-01-01 00:00:00 to 2020-01-01 00:00:00 (JST).
            li The flag format is KosenCTF{[A-Za-z0-9_- !?#]+}, unless otherwise specified.
            li
                | The score of every challenge is calculated by the following formula:
                pre
                    code dynamic_score = max(200, (base_score**2) / (base_score + (base_score/10) * (0 if solve_count == 1 else solve_count)))
            li There is no limit in the number of your team members.
            li There is no prize.
            li
                | If you have any questions during the contest, please contact to admin&nbsp;
                a(href="#") here
                | .

        h2 Restrictions
        ul
            li Do not share flags or hints among teams.
            li Do not attempt to attack this score server.
            li Do not attempt to DoS to any challenge servers.
</template>

<script>
import Vue from 'vue'
export default Vue.extend({})
</script>

<style scoped>
</style>

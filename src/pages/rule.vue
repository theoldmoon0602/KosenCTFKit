<template lang="pug">
    div
        h2 Basics
        ul
            li {{ctfname}} is an online jeopardy-style CTF.
            li
                | The competition will be held from&nbsp;
                code {{start_at}}
                | &nbsp;to&nbsp;
                code {{end_at}}
                | .
            li The flag format is {{ flag_format }}, unless otherwise specified.
            li
                | The score of every challenge is calculated by the following formula:
                pre
                    code dynamic_score = {{ scoreexpr }}
            li If multiple teams get the same score, the team which solved their last challenge (except for Survey) earlier will be ranked higher.
            li There is no limit in the number of your team members.
            li There is no prize.
            li
                | If you have any questions during the contest, please contact to admin&nbsp;
                a(:href="invite_url") here
                | .

        h2 Restrictions
        ul
            li Do not share flags or hints among teams.
            li Do not attempt to attack this score server.
            li Do not attempt to DoS to any challenge servers.
</template>

<script>
import Vue from 'vue'
import moment from 'moment'
export default Vue.extend({
    computed: {
        ctfname() {
            return this.$store.getters.getCTFName
        },
        invite_url() {
            return this.$store.getters.getInviteURL
        },
        scoreexpr() {
            return this.$store.getters.getScoreExpr
        },
        start_at() {
            return this.$store.getters.getCTFStart.toString()
        },
        end_at() {
            return this.$store.getters.getCTFEnd.toString()
        },
        flag_format() {
            return this.$store.getters.getFlagFormat
        }
    },

})
</script>

<style scoped>
</style>

<template lang="pug">
    div
        h2 Players
        table.table
            thead
                tr
                    th(scope="col") Name
                    th(scope="col") Team
                    th(score="col") Score
            tbody
                tr(v-for="u in ranking")
                    td
                        router-link(:to="'/user/'+u.id") {{ u.name }}
                    td
                        router-link(:to="'/team/'+u.team_id" v-if="u.team") {{ u.team }}
                    td {{ u.score }}
</template>

<script>
import Vue from 'vue/dist/vue.js'
import axios from 'axios'
export default Vue.extend({
    computed: {
        ranking() {
            let ranking = Object.values(this.$store.getters.getUsers);
            ranking.sort((a, b) => {
                if (a.score == b.score) {
                    return a.last_submission - b.last_submission;
                }
                return b.score - a.score
            })
            let rank = 1;
            if (ranking.length > 0) {
                ranking[0].rank = rank;
            }
            for (let i = 1; i < ranking.length; i++) {
                if (ranking[i-1].score == ranking[i].score && ranking[i-1].last_submission == ranking[i].last_submission) {
                    ranking[i].rank = rank;
                }
                else {
                    rank += 1;
                    ranking[i].rank = rank;
                }
            }
            return ranking;
        }
    }
})
</script>


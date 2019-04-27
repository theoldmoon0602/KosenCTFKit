<template lang="pug">
    div
        h2 Scoreboard
        .alert.alert-info(v-if="isFrozen") SCOREBORED HAS BEEN FROZEN
        table.table
            thead
                tr
                    th(scope="col") Rank
                    th(scope="col") Team
                    th(score="col") Score
            tbody
                tr(v-for="t in scoreboard")
                    td {{ t.rank }}
                    td
                        router-link(:to="'/team/'+t.id") {{ t.name }}
                    td {{ t.score }}
</template>

<script>
import Vue from 'vue/dist/vue.js'
import axios from 'axios'
export default Vue.extend({
    computed: {
        scoreboard() {
            let board = Object.values(this.$store.getters.getScoreboard);
            board.sort((a, b) => {
                if (a.score == b.score) {
                    return a.last_submission - b.last_submission;
                }
                return b.score - a.score
            })
            let rank = 1;
            if (board.length > 0) {
                board[0].rank = rank;
            }
            for (let i = 1; i < board.length; i++) {
                if (board[i-1].score == board[i].score && board[i-1].last_submission == board[i].last_submission) {
                    board[i].rank = rank;
                }
                else {
                    rank += 1;
                    board[i].rank = rank;
                }
            }
            return board;
        },
        isFrozen() {
            return this.$store.getters.isFrozen;
        }
    }
})
</script>


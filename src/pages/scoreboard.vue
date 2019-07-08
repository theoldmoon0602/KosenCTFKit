<template lang="pug">
    div
        h2 Scoreboard
        .alert.alert-info(v-if="isFrozen") SCOREBORED HAS BEEN FROZEN
        p
            button.btn.btn-primary(@click="update_graph") update
            canvas(ref="chart")
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
import 'chart.js/dist/Chart.js'
import {chart_options, colorhash} from '../lib/chart_options.js'

import Vue from 'vue'
import axios from 'axios'
export default Vue.extend({
    data() {
        return {
            chart: null
        }
    },
    mounted() {
        let ctx = this.$refs.chart.getContext('2d');
        this.chart = new Chart(ctx, chart_options);
        this.update_graph();
    },
    methods: {
        update_graph() {
            this.$store.dispatch('getSubmissions');
        },
        draw_graph() {
            let topteams = this.scoreboard.slice(0, 10);
            let challenges = this.$store.getters.getChallenges;
            let submissions = this.submissions;
            let graph_data = [];
            for (let t of topteams) {
              let current_score = 0;
              graph_data.push({
                label: t.name,
                lineTension: 0,
                borderColor: colorhash(t.name),
                backgroundColor: colorhash(t.name),
                fill: false,
                data: submissions.filter(s => s.team_id == t.id).sort((a, b) => a.created_at - b.created_at).map(s => {
                  current_score += challenges[s.challenge_id].score
                  return {
                    t: new Date(s.timestring),
                    y: current_score,
                    name: challenges[s.challenge_id].name,
                    score: challenges[s.challenge_id].score,
                  }
                })
              })
            }
            for (let i = 0; i < graph_data.length; i++) {
              graph_data[i].data.unshift({
                t: this.$store.getters.getCTFStart,
                y: 0,
                name: "CTF START"
              })
            }
            this.chart.data.datasets = graph_data
            this.chart.update();

        },
    },
    computed: {
        submissions() {
            return this.$store.getters.getSubmissions
        },
        scoreboard() {
            let board = Object.values(this.$store.getters.getTeams);
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
        },
    },
    watch: {
        submissions() { this.draw_graph() },
    }
})
</script>



<template lang="pug">
    div
        h2 Players
        p
            button.btn.btn-primary(@click="update_graph") update
            canvas(ref="pchart")
        table.table
            thead
                tr
                    th(scope="col") Name
                    th(scope="col") Team
                    th(score="col") Score
            tbody
                tr(v-for="u in ranking")
                    td
                        router-link(:to="'/user/'+u.id" v-if="u.icon")
                            img(:src="u.icon")
                            | {{ u.name }}
                        router-link(:to="'/user/'+u.id" v-else) {{ u.name }}
                    td
                        router-link(:to="'/team/'+u.team_id" v-if="u.team") {{ u.team }}
                    td {{ u.score }}
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
        let ctx = this.$refs.pchart.getContext('2d');
        this.chart = new Chart(ctx, chart_options);
        this.update_graph();
    },
    methods: {
        update_graph() {
            this.$store.dispatch('getSubmissions');
        },
        draw_graph() {
            let topusers = this.ranking.slice(0, 10);
            let challenges = this.$store.getters.getChallenges;
            let submissions = this.submissions;
            let graph_data = [];
            for (let u of topusers) {
              let current_score = 0;
              graph_data.push({
                label: u.name,
                lineTension: 0,
                borderColor: colorhash(u.name),
                backgroundColor: colorhash(u.name),
                fill: false,
                data: submissions.filter(s => s.user_id == u.id).sort((a, b) => a.created_at - b.created_at).map(s => {
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
    },
    watch: {
        submissions() { this.draw_graph() },
    }
})
</script>

<style scoped>
img {
    height: 1.2em;
    width: 1.2em;
    vertical-align: middle;
}
</style>

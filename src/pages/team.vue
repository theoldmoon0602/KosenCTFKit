<template lang="pug">
    .col-12.col-lg-8.offset-lg-2
        h3.h3 {{team.name}}[{{ team.score }}points]

        div(v-if="loginTeam && team.id == loginTeam.id")
            .input-group.mb-3
                input.form-control(type="text" readonly :value="loginTeam.token")
                .input-group-append
                    button.btn.btn-primary(type="button" @click="regenerate") Regenerate

        h4.h4 Members
            .row
                .card.col-12.col-md-6(v-for="m in team.members")
                    .card-body
                        .card-title
                            router-link(:to="'/user/'+m") {{ user(m).name }}
                        img.icon(v-if="user(m).icon" :src="user(m).icon" :alt="user(m).name")
        h4.h4 Solved Challenges
            .row
                .card.col-12.col-md-6(v-for="cid in team.solved" v-if="challenge(cid)")
                    .card-body
                        .card-title {{ challenge(cid).name }}
                        .card-text {{ challenge(cid).category }} [{{challenge(cid).score}}points]


</template>

<script>
import Vue from 'vue'
import axios from 'axios'
export default Vue.extend({
    methods: {
        regenerate() {
            this.$store.dispatch('regenerate')
        },
        challenge(cid) {
            let challenges = this.$store.getters.getChallenges;
            return challenges[cid];
        },
        user(uid) {
            return this.$store.getters.getUsers[uid];
        }
    },
    computed: {
        team() {
            let teams = this.$store.getters.getTeams;
            let team_id = this.$route.params['team_id'];
            return teams[team_id];
        },
        loginTeam() {
            return this.$store.getters.getTeam;
        }
    }
})
</script>


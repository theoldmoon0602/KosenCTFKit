<template lang="pug">
    div(style="margin-bottom: 100px;")
        .form-group
            label.d-block(for="filter") filter challenges by name, difficulty, tags
            input.form-control#filter(type="text" v-model="filter")
        .card(v-for="chal in challenges()" v-bind:class="{'border-success' : is_solved(chal.id)}")
            h5.card-header(v-bind:class="{'bg-success': is_solved(chal.id)}")
                a.trigger(data-toggle="collapse"  aria-expanded="true" :data-target="'#chal-' + chal.id" :aria-controls="'chal-'+chal.id")
                    |{{ chal.name }}
                    small.small [{{ chal.score }}] - {{ chal.solved }} solved
                    span.float-right
                        span.badge.badge-info {{difficulty(chal.difficulty)}}
                        span.badge.badge-primary(v-for="tag in chal.tags") {{ tag }}
            .collapse(:id="'chal-'+chal.id")
                .card-body.col-12.col-md-8.mx-auto
                    .card-text
                        p(v-html="chal.description")
                        p.text-right {{chal.author}}
                        p(v-if="chal.attachments" v-for="a in chal.attachments")
                            a.btn.btn-primary(target="_blank" :href='a') {{ basename(a) }}
                    form(@submit.prevent="submit")
                        input(type="hidden" name="id" :value="chal.id")
                        .input-group.mb-3
                            input.form-control(type="text" name="flag" required :placeholder="flag_format")
                            .input-group-append
                                button.btn.btn-primary(type="submit") Submit

</template>

<script>
import Vue from 'vue'
import axios from 'axios'
export default Vue.extend({
    data() {
        return {
            filter: ''
        }
    },
    methods: {
        difficulty(d) {
            let difficulties = ["warmup", "easy", "medium", "hard", "lunatic"];
            let index = Math.max(0, Math.min(difficulties.length - 1, d | 0))
            return difficulties[index]
        },
        submit(e) {
            let data = new FormData(e.target)
            let json = {}
            data.forEach((v, k) => {json[k] = v})
            this.$store.dispatch('submit', json)
        },
        basename(p) {
            return p.split('/').pop()
        },
        is_solved(challenge_id) {
            let user = this.$store.getters.getCurrentUser
            let team_id = user.team_id;
            if (team_id) {
                let teams = this.$store.getters.getTeams;
                return teams[team_id].solved.includes(challenge_id);
            }
            return false
        },
        challenges() {
            let filtered = [];
            let challenges = this.$store.getters.getChallenges;
            if (this.filter) {
                for (let i of Object.keys(challenges)) {
                    let challenge = challenges[i]
                    if (challenge.name.includes(this.filter)) {
                        filtered.push(challenge)
                        continue;
                    }
                    if (this.difficulty(challenge.difficulty).includes(this.filter)) {
                        filtered.push(challenge)
                        continue;
                    }
                    for (let tag of challenge.tags) {
                        if (tag.includes(this.filter)) {
                            filtered.push(challenge)
                            break;
                        }
                    }
                }
            } else {
                for (let i of Object.keys(challenges)) {
                    filtered.push(challenges[i]);
                }
            }
            return filtered.sort((a, b) => {
                let tagA = "", tagB = "";
                if (a.tags.length > 0) {
                    tagA = a.tags[0];
                }
                if (b.tags.length > 0) {
                    tagB = b.tags[0];
                }
                if (tagA < tagB) {
                    return -1;
                }
                else if (tagA > tagB) {
                    return 1;
                }
                else {
                    return a.difficulty-b.difficulty;
                }
            })
        },
    },
    computed: {
        flag_format() {
            return this.$store.getters.getFlagFormat
        }
    }
})
</script>

<style scoped lang="scss">
.trigger {
    display: block;
    &:hover {
        cursor: pointer;
    }
    padding: 0.75rem 1.25rem;
}
.card-header {
    padding: 0;
}
.solved {
    box-shadow: 0 0 5px lime;
}
.badge {
    margin-right: 0.2em;
}
</style>

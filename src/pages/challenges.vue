<template lang="pug">
    div
        .rows(v-for="c in categories")
            h1 {{ c[0].category }}
            .card(v-for="chal in c" v-bind:class="{'solved' : solved.includes(chal.id)}")
                h5.card-header
                    a.trigger(data-toggle="collapse"  aria-expanded="true" :data-target="'#chal-' + chal.id" :aria-controls="'chal-'+chal.id")
                        |{{ chal.name }}
                        small.small [{{ chal.score }}] - {{ chal.solved }} solved
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
                                input.form-control(type="text" name="flag" required placeholder="KosenCTF{.+}")
                                .input-group-append
                                    button.btn.btn-primary(type="submit") Submit

</template>

<script>
import Vue from 'vue/dist/vue.js'
import axios from 'axios'
export default Vue.extend({
    methods: {
        submit(e) {
            let data = new FormData(e.target)
            let json = {}
            data.forEach((v, k) => {json[k] = v})
            this.$store.dispatch('submit', json)
        },
        basename(p) {
            return p.split('/').pop()
        },
    },
    computed: {
        categories() {
            return this.$store.getters.getChallengesWithCategory;
        },
        solved() {
            let team_id = this.$store.getters.getUser.team_id;
            let teams = this.$store.getters.getTeams;
            return teams[team_id].solved
        },
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
</style>

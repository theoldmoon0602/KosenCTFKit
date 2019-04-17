let challenges = Vue.component("challenges", {
    template: `
    <div>
        <h3>Challenges</h3>

        <div v-for="(c, idx) in challenges" class="accordion">
            <input type="checkbox" :id="'accordion-'+idx" name="accordion-checkbox" hidden>
            <label class="accordion-header" :for="'accordion-'+idx">[{{c.category}} {{c.score}}]{{ c.name }}</label>
            <div class="accordion-body">{{ c.description }}</div>
        </div>
    </div>
    `,
    mounted() {
        api.get('/challenges')
            .then(r => {
                if (r.data) {
                    this.$store.commit('setChallenges', r.data)
                }
            })
            .catch(e => {
                if (e.response.status == 403) {
                    this.$route.push('/login')
                } else {
                    this.$store.commit('setErrors', e.response.data['error'])
                }
            })
    },
    computed: {
        challenges() {
            return this.$store.state.challenges ? this.$store.state.challenges : []
        }
    }
});

let challenges = Vue.component("challenges", {
    template: `
    <div>
        <h3>Challenges</h3>

        <div v-for="(c, idx) in challenges" class="accordion" :class="{'bg-secondary':c.solved}">
            <input type="checkbox" :id="'accordion-'+idx" name="accordion-checkbox" hidden>
            <label class="accordion-header text-center" :for="'accordion-'+idx">[{{c.category}} {{c.score}}]{{ c.name }}</label>
            <div class="accordion-body">
                <div class="column col-6 col-mx-auto" style="border: 2px solid #302ecd; padding: 1rem;">
                    <div>{{ c.description }}</div>
                    <div class="text-right" style="margin-top: 0.5rem;">{{ c.author }}</div>
                </div>

                <form class="input-group column col-8 col-mx-auto my-2" @submit.prevent="submitFlag">
                    <input type="text" class="form-input" name="flag" placeholder="KosenCTF{35c4p3_fr0m_u_top14}">
                    <input type="hidden" name="challenge_id" :value="c.id">
                    <input type="submit" class="btn btn-primary input-group-btn" value="Submit"/>
                </form>
            </div>
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
    methods: {
        submitFlag(e) {
            const form_data = new FormData(e.target)
            api.post('/submit', {
                flag: form_data.get('flag'),
                challenge_id: form_data.get('challenge_id'),
            })
                .then(r => {
                    if (r.data) {
                        if (r.data['solved']) {
                            this.$store.commit('setMessages', [r.data['status']])
                            this.$store.commit('setSolved', challenge_id)
                        } else {
                            this.$store.commit('setErrors', [r.data['status']])
                        }
                    }
                })
                .catch(e => {
                    this.$store.commit('setErrors', e.response.data['error'])
                })
        }
    },
    computed: {
        challenges() {
            return this.$store.state.challenges ? this.$store.state.challenges : []
        }
    }
});

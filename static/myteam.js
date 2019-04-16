let myteam = Vue.component("myteam", {
    template: `
    <div>
        <h3>{{ team }}</h3>
        <div class="input-group">
            <span class="input-group-addon">Team Token</span>
            <input type="text" class="form-input" v-model="token" readonly>
            <button class="btn btn-primary input-group-btn" @click="regenerate">Regenerate</button>
        </div>

        <h4>Members</h4>
        <div class="card" v-for="m in members">
            <div class="card-header">
                <div class="card-title">{{ m.name }}</div>
            </div>
        </div>
    </div>
    `,
    data() {
        return {
            members: [],
            token: ''
        }
    },
    mounted() {
        api.get('myteam')
            .then(r => {
                this.members = r.data['members']
                this.token = r.data['token']
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
        regenerate() {
            api.post('regenerate')
                .then(r => {
                    this.token = r.data['token']
                })
                .catch(e => {
                    if (e.response.status == 403) {
                        this.$route.push('/login')
                    } else {
                        this.$store.commit('setErrors', e.response.data['error'])
                    }
                })
        }
    },
    computed: {
        team() {
            return this.$store.state.user.team
        }
    }
});

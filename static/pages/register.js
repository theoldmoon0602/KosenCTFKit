let register = Vue.component("register", {
    template: `
    <div class="column col-8 col-mx-auto my-2">
        <form @submit.prevent="register_user">
            <div class="form-group">
              <label class="form-label" for="teamtoken">team token</label>
              <input class="form-input" type="text" id="teamtoken" v-model="teamtoken" placeholder="xxxxxxxxxxxxxxxxxxxxxxxx" required>
            </div>
            <div class="form-group">
              <label class="form-label" for="username">username</label>
              <input class="form-input" type="text" id="username" v-model="username" placeholder="MIZUKI MAKABE" required>
            </div>
            <div class="form-group">
              <label class="form-label" for="password">password</label>
              <input class="form-input" type="password" id="password" v-model="password" placeholder="Melty Fantasia" required>
            </div>
            <div class="form-group">
                <button class="btn btn">Register User</button>
            </div>
        </form>

        <form @submit.prevent="register_team">
            <div class="form-group">
              <label class="form-label" for="teamname">team name</label>
              <input class="form-input" type="text" id="teamname" v-model="teamname" placeholder="EScape" required>
            </div>
            <div class="form-group">
                <button class="btn btn">Register Team</button>
            </div>
        </form>
    </div>
    `,
    data() {
        return {
            teamtoken: '',
            username: '',
            password: '',
            teamname: '',
        }
    },
    methods: {
        register_user() {
            api.post('register-user', {
                teamtoken: this.teamtoken,
                username: this.username,
                password: this.password,
            })
                .then(r => {
                    this.$store.commit('setMessages', ['The user has been registered.']);
                    this.$router.push('/login')
                })
                .catch(e => {
                    this.$store.commit('setErrors', e.response.data['error'])
                })
        },
        register_team() {
            api.post('register-team', {
                teamname: this.teamname,
            })
                .then(r => {
                    this.teamtoken = r.data['token']
                    this.$store.commit('setMessages', ['The team has been temporality registered. Please register as user next.'])
                })
                .catch(e => {
                    this.$store.commit('setErrors', e.response.data['error'])
                })
        }
    }
});

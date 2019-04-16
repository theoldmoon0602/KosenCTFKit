let login = Vue.component("login", {
    template: `
    <div class="column col-8 col-mx-auto my-2">
        <form @submit.prevent="login">
            <div class="form-group">
              <label class="form-label" for="username">username</label>
              <input class="form-input" type="text" id="username" v-model="username" placeholder="MIZUKI MAKABE" required>
            </div>
            <div class="form-group">
              <label class="form-label" for="password">password</label>
              <input class="form-input" type="password" id="password" v-model="password" placeholder="Melty Fantasia" required>
            </div>
            <div class="form-group">
                <button class="btn btn">Login</button>
            </div>
        </form>
    </div>
    `,
    data() {
        return {
            username: '',
            password: '',
        }
    },
    methods: {
        login() {
            api.post('login', {
                username: this.username,
                password: this.password,
            })
                .then(r => {
                    document.cookie = 'user=' + r.data['cookie-user']
                    this.$store.commit('setLogin', true)
                    this.$store.commit('setUser', r.data['user'])
                    this.$router.push('/')
                })
                .catch(e => {
                    this.$store.commit('setErrors', e.response.data['error'])
                })
        }
    }
});

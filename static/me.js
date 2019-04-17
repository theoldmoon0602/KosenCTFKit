let me = Vue.component("me", {
    template: `
    <div>
        <h3>{{username }}</h3>

        <form @submit.prevent="set_password" class="column col-8 col-mx-auto my-2">
            <h4>Password Update</h4>
            <div class="form-group">
              <label class="form-label" for="current_password">current password</label>
              <input class="form-input" type="password" id="current_password" v-model="current_password" placeholder="Melty Fantasia" required>
            </div>

            <div class="form-group">
              <label class="form-label" for="new_password">new password</label>
              <input class="form-input" type="password" id="new_password" v-model="new_password" placeholder="Melty Fantasia" required>
            </div>
            <div class="form-group">
                <button class="btn btn">Update</button>
            </div>
        </form>

    </div>
    `,
    data() {
        return {
            current_password: '',
            new_password: '',
        }
    },
    methods: {
        set_password() {
            api.post('set_password', {
                current_password: this.current_password,
                new_password: this.new_password,
            })
                .then(r => {
                    this.$store.commit('setMessages', ['Password is updated sucessfully'])
                })
                .catch(e => {
                    if (e.response.status == 403) {
                        this.$route.push('/login')
                    } else {
                        this.$store.commit('setErrors', e.response.data['error'])
                    }
                })
                .finally(_ => {
                    this.current_password = ''
                    this.new_password = ''
                })
        }
    },
    computed: {
        username() {
            return this.$store.state.user ? this.$store.state.user.name : ""
        }
    }
});

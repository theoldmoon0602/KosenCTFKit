<template lang="pug">
    .rows
        form.col-12.col-lg-8.offset-lg-2(@submit.prevent="reset")
            .form-group
                label.d-block(for="password") password
                input#password(type="password" v-model="password" required class="form-control" placeholder="password")
            button.btn.btn-primary.float-right(type="submit") Reset

</template>

<script>
import Vue from 'vue'

export default Vue.extend({
    data() {
        return {
            password: '',
        }
    },
    methods: {
        reset() {
            let token = this.$route.params['token'];
            this.$store.dispatch('reset', {
                password: this.password,
                token: token,
            }).then(r => {
                if (r) {
                    this.$router.push('/login')
                }
            })
        },
    },
})
</script>

<template lang="pug">
    .rows
        form.col-12.col-lg-8.offset-lg-2(@submit.prevent="resetRequest")
            .form-group
                label.d-block(for="username") username
                input#username(type="text" v-model="username" required placeholder="username" class="form-control")
            .form-group
                label.d-block(for="email") email
                input#email(type="email" v-model="email" required class="form-control" placeholder="email")
            button.btn.btn-primary.float-right(type="submit") Password Reset

</template>

<script>
import Vue from 'vue'

export default Vue.extend({
    data() {
        return {
            email: '',
            username: '',
        }
    },
    methods: {
        resetRequest() {
            this.$store.dispatch('resetRequest', {
                email: this.email,
                username: this.username,
            }).then(r => {
                if (r) {
                    this.$router.push('/login')
                }
            })
        },
    },
})
</script>

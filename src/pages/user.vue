<template lang="pug">
    .col-12.col-lg-8.offset-lg-2
        h3.h3
            img.icon(:src="user.icon" :alt="user.name" v-if="user.icon")
            |{{ user.name }}
            template(v-if="user.team")
                |@
                router-link(:to="'/team/'+user.team_id") {{user.team}}
            | [{{user.score}}points]



        template(v-if="loginUser && user.id == loginUser.id")
            .custom-file
                input.custom-file-input#icon(type="file" accept="image/png" required @change="selectIcon")
                label.custom-file-label(for="icon") Upload Icon
            form(@submit.prevent="updatePassword")
                .form-group
                    label.d-block(for="current_password") current password
                    input.form-control(type="password" name="current_password" required)
                .form-group
                    label.d-block(for="new_password") new password
                    input.form-control#new_password(type="password" name="new_password" required)
                button.btn.btn-primary.float-right(type="submit") Update Password

            div(v-if="loginUser.verified")
                label this address is verified
                .form-group
                    input.form-control(type="email" :value="loginUser.email" disabled)
            form(@submit.prevent="resendVerificationMail" v-else)
                .form-group
                    label.d-block(for="email") email
                    input.form-control#email(type="email" v-model="email" :placeholder="loginUser.email" name="email" required)
                button.btn.btn-primary.float-right(type="submit") Resend Verification Mail

        h4.h4 Solved Challenges
            .row
                .card.col-12.col-md-6(v-for="cid in user.solved" v-if="challenge(cid)")
                    .card-body
                        .card-title {{ challenge(cid).name }}
                        .card-text [{{challenge(cid).score}}points]

</template>

<script>
import Vue from 'vue'
import axios from 'axios'
export default Vue.extend({
    data() {
        return {
            email: ''
        }
    },
    methods: {
        challenge(cid) {
            let challenges = this.$store.getters.getChallenges;
            return challenges[cid];
        },
        updatePassword(e) {
            let data = new FormData(e.target);
            let json = {};
            data.forEach((v, k) => {json[k] = v});
            this.$store.dispatch('updatePassword', json);
        },
        selectIcon(e) {
            let files = e.target.files;
            let f = files[0];

            if (! f.type.match('image/*')) {
                this.$store.dispatch('setError', 'Not an Image file')
                return
            }
            let fileReader = new FileReader();
            fileReader.addEventListener("load", () => {
                let icon = fileReader.result;
                this.$store.dispatch('uploadIcon', icon.split(',')[1])
            }, false)
            fileReader.readAsDataURL(f);
        },
        resendVerificationMail() {
            this.$store.dispatch('resendVerificationMail', {
                email: this.email
            })
        },
    },
    computed: {
        user() {
            let user_id = this.$route.params['user_id']
            let user = this.$store.getters.getUsers[user_id]
            return user;
        },
        loginUser() {
            return this.$store.getters.getCurrentUser;
        }
    },
})
</script>

<style scoped>
img {
    height: 1.2em;
    width: 1.2em;
    vertical-align: middle;
}
</style>

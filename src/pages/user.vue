<template lang="pug">
    .col-12.col-lg-8.offset-lg-2
        h3.h3
            |{{ user.name }}
            template(v-if="user.team")
                |@
                router-link(:to="'/team/'+user.team_id") {{user.team}}
            | [{{user.score}}points]

        div(v-if="user.icon")
            img.icon(:src="user.icon" :alt="user.name")

        div(v-if="loginUser && user.id == loginUser.id")
            h5.h5 Update Password
            form(@submit.prevent="updatePassword")
                .form-group
                    label.d-block(for="current_password") current password
                    input#current_password(type="password" name="current_password" required class="form-control")
                .form-group
                    label.d-block(for="new_password") new password
                    input#new_password(type="password" name="new_password" required class="form-control")
                button.btn.btn-primary(type="submit") Update Password

            h5.h5 Upload Icon
            .custom-file
                input.custom-file-input#icon(type="file" accept="image/*" required @change="selectIcon")
                label.custom-file-label(for="icon") Upload Icon


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


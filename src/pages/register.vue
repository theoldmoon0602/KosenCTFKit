<template lang="pug">
    .rows
        b-form.col-12.col-lg-8.offset-lg-2(@submit.prevent="registerTeam")
            b-form-group(label="teamname", label-for="teamname", description="unique teamname")
                input#teamname(type="text", v-model="teamname", required, placeholder="ESCape", class="form-control")
            b-button(variant="primary", type="submit") Register Team

        b-form.col-12.col-lg-8.offset-lg-2
            b-form-group(label="teamtoken", label-for="teamtoken", description="your team's token")
                input#teamtoken(type="text", v-model="teamtoken", required, class="form-control")
            b-form-group(label="username", label-for="username", description="unique username")
                input#username(type=text, required, placeholder="MAKABEE", class="form-control")
            b-form-group(label="password", label-for="password", description="password")
                input#password(type="password", required, class="form-control")
            b-button(variant="primary", type="submit") Register User

</template>

<script>
import Vue from 'vue/dist/vue.js'
import axios from 'axios'
export default Vue.extend({
    data() {
        return {
            teamname: '',
            teamtoken: ''
        }
    },
    methods: {
        registerTeam() {
            axios.post('/register-team', {
                teamname: this.teamname,
            })
                .then(r => console.log(r))
                .then(e => console.log(e))
        }
    },
})
</script>


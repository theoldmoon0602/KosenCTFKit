<template lang="pug">
    .rows
        b-form.col-12.col-lg-8.offset-lg-2
            b-form-group(label="teamname", label-for="teamname", description="unique teamname")
                b-form-input#username(type=text, required, placeholder="EScape")
            b-button(variant="primary", type="submit") Register Team

        b-form.col-12.col-lg-8.offset-lg-2
            b-form-group(label="teamtoken", label-for="teamtoken", description="your team's token")
                b-form-input#teamtoken(type=text, required)
            b-form-group(label="username", label-for="username", description="unique username")
                b-form-input#username(type=text, required, placeholder="MAKABEE")
            b-form-group(label="password", label-for="password", description="password")
                b-form-input#password(type="password", required)
            b-button(variant="primary", type="submit") Register User

</template>

<script>
import Vue from 'vue/dist/vue.js'
export default Vue.extend({})
</script>


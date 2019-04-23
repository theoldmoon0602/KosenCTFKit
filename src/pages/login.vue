<template lang="pug">
    .rows
        b-form.col-12.col-lg-8.offset-lg-2
            b-form-group(label="username", label-for="username", description="unique username")
                b-form-input#username(type=text, required, placeholder="MAKABEE")
            b-form-group(label="password", label-for="password", description="password")
                b-form-input#password(type="password", required)
            b-button(variant="primary", type="submit") Login

</template>

<script>
import Vue from 'vue/dist/vue.js'
export default Vue.extend({})
</script>


<template lang="pug">
    div
        h3 confirmation
</template>

<script>
import Vue from 'vue'

export default Vue.extend({
    mounted() {
        let token = this.$route.params['token'];
        this.$store.dispatch('confirm', {
            token: token
        })
            .then(r => {
                if (r) {
                    this.$router.push('/login')
                }
            })
    }
})
</script>

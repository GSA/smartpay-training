<script setup>
    import { onMounted } from 'vue'
    import { userFlowStore } from '@/stores/userFlow'

    const props = defineProps({
        'token': String
    })
    const store = userFlowStore()
    onMounted(() => {store.getUserFromToken(props.token)})

</script>

<template>
    <h3>Hello {{ store.user.first_name }} from {{ store.user.agency }}</h3>

    [To start the quiz]
    [for devs: the server sent a jwt: {{ store.jwt }}]

</template>
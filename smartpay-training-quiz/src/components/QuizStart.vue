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
    <div v-if="store.jwt">
        <h3>Hello {{ store.user.first_name }} from {{ store.user.agency }}</h3>

        [Link To start the quiz goes here]
    </div>
    <div v-else>
        <h3>Not Found</h3>
        We were not able to locate this link. Some helpful user instructions go here.
    </div>

</template>
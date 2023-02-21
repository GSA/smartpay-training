<script setup>
    import { onMounted } from 'vue'
    import Alert from "@/components/uswds/Alert.vue"
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
        <Alert heading="Not Found" status="warning">
            <span>
                We were not able to locate this link. Some helpful user instructions go here.
            </span>
        </Alert>
    </div>

</template>
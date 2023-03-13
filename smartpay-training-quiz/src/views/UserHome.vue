<script setup>
  import { onMounted } from 'vue'
  import Alert from "@/components/uswds/Alert.vue"
  import { userFlowStore } from '@/stores/userFlow'
  import Hero from '@/components/smartpay/Hero.vue'
  import hero_image from '@/assets/images/Training_TravelAH_Hero.jpg'

  const props = defineProps({
    'token': String
  })
  const store = userFlowStore()
  onMounted(() => store.getUserFromToken(props.token))
</script>

<template>
  <Hero :hero_image="hero_image">
    <template #default>
    Travel Training for Card / Account Holders and Approving officials
    </template>
  </Hero>

  <div v-if="store.jwt" class="grid-container">
    <h3>Hello {{ store.user.first_name }} from {{ store.user.agency }}</h3>
    <p>
      [Tables of past certificates goes here (maybe behind an accodian)]
    </p>
    <p>
      [Link To start the quiz goes here]
    </p>
  </div>
  <div v-else-if="store.loading == false">
    <Alert heading="Not Found" status="warning">
        <span>
            We were not able to locate this link. Some helpful user instructions go here.
        </span>
    </Alert>
  </div>

</template>
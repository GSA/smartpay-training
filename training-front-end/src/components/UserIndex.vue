<script setup>
  import { onMounted, ref } from 'vue'
  import { profile, getUserFromToken } from '../stores/user'
  import { useStore } from '@nanostores/vue'
  import Alert from '../components/Alert.vue'
  import Verify from '../components/Verify.vue'
  import UserHome from '../components/UserHome.vue'
  import Loginless from '../components/Loginless.vue';

  const user = useStore(profile)
  const base_url = import.meta.env.PUBLIC_API_BASE_URL
  const loaded = ref(false)
  const invalidToken = ref(false)

  onMounted(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('t')

    if (token) {
        try {
            await getUserFromToken(base_url, token)
        } catch(e) {
            console.log("error", e)
            invalidToken.value = true
        }
    } 
    loaded.value = true
  })

  function formsubmitted() {
    invalidToken.value = false
  }

</script>

<template>
  <div  class="grid-container" data-test="post-submit">
    <div v-if="loaded" class="grid-container">
      <UserHome  v-if="user.jwt"/>
      <div v-else>
          <Alert v-if="invalidToken" class="tablet:grid-col-8" status="warning" heading="Invalid Link">
            This link is either expired or is invalid. Links to training are only valid for 24 hours.
            Please request a new link with the form below.
          </Alert>
          <Loginless @submitted="formsubmitted"/>
      </div>
    </div>
  </div>
</template>